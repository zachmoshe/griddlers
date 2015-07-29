require 'net/http'
require 'open4'

class GriddlersSolverWorker
	attr_reader :queue_url, :new_work_topic_arn, :poller, :s3, :sns, :logger

	def initialize(sqs_queue_url, new_work_topic_arn)
		raise ArgumentError, "invalid SQS queue URL" unless sqs_queue_url
		@queue_url = sqs_queue_url
		@new_work_topic_arn = new_work_topic_arn

		@poller = Aws::SQS::QueuePoller.new(queue_url)
		@s3 = Aws::S3::Client.new
		@sns = Aws::SNS::Client.new 
		@logger = Logger.new 'worker.log'
	end  

	def poll
		# visibility_timeout = 4 hours, idle_timeout = 10 minutes
		poller.poll(visibility_timeout: 4*60*60, idle_timeout: 10*60) do |msg|
			begin 
				logger.info "waiting for message..."
				handle_message msg

			rescue Exception => ex
				logger.error "Error while handling message: #{ex.message}"
				logger.error ex.backtrace.join "\n"
				poller.change_message_visibility_timeout msg, 5  # return message to the queue (almost) immediately
				throw :skip_delete
			end
		end
		logger.info "Idle timeout passed. Quitting"
	end


	protected
	def periodically_check_termination_time
		loop do
			sleep(5)
			begin
				resp = Net::HTTP.get_response URI.parse('http://169.254.169.254/latest/meta-data/spot/termination-time')

				if resp.code == '404'
					logger.debug "Checking if we were terminated... not yet."
				else 
					logger.debug "Checking if we were terminated... YES! Termination scheduled"
					return
				end
			rescue Exception => ex
				logger.error "Can't poll for termination-time: #{ex.message}"
			end
		end
	end



	def handle_message(msg)
		s3Location = JSON.parse(JSON.parse(msg.body)['Message'])
		logger.info "got S3 location: #{s3Location}"

		termination_check_thread = Thread.new do
			# this will return if termination was enforced (with ~2 minutes warning)
			periodically_check_termination_time
			logger.debug "should terminate."
			logger.info "submitting #{s3Location} to new-work-queue again"
			sns.publish topic_arn: new_work_topic_arn, message: s3Location.to_json
			logger.info "work re-submitted to queue"
		end


		bucket, key = s3Location['Bucket'], s3Location['Key']
		work_id = key.split('/')[0]
		logger.info "handling workId: #{work_id}"

		request = s3.get_object( bucket: bucket, key: key).body.read
		strategy, request_params, board = request.split("\n")


		# Send the python job
		result = nil
		error = nil
		output = nil

		core_path = "#{File.dirname(__FILE__)}/../core"
		begin
			status = Open4::popen4("#{core_path}/env/bin/python #{core_path}/bin/board_solver.py") do |pid, stdin, stdout, stderr|
				logger.info "Starting board_solver.py for request #{work_id} [PID=#{pid}]"

				stdin.puts(strategy)
				stdin.puts(request_params)
				stdin.puts(board)
				stdin.close

				result = stdout.read.strip
				error = stderr.read.strip
			end

			logger.info "board_solver.py [PID=#{status.pid}] ended. <exitstatus=#{status.exitstatus}> , <error=#{error}>"

			if [0,250].include? status.exitstatus  # 0 for successful run and 250 for regular error (normal output of the script)
				output = JSON.load(result)
			else
				# handle fatal errors (where we couldn't even run the solver script in a similar way to "regular" errors)
				error_message = error.split(/[:\n]/).last.strip
				logger.error "Fatal error: #{error_message}"
				logger.error "STDOUT - #{output}"
				logger.error "STDERR - #{error}"
				output = { 'status' => 'fatal-error', 'message' => error_message }
			end

		rescue Exception => ex
			logger.error "Fatal error: #{ex.message}"
			logger.error "STDOUT - #{output}"
			logger.error "STDERR - #{error}"
			logger.error ex.backtrace.join "\n"
			output = { 'status' => 'fatal-error', 'message' => ex.message }
		end

		logger.info "Uploading response for #{work_id} to #{bucket}. status is #{output['status']}"
		s3.put_object( bucket: bucket, key: "#{work_id}/response", body: output.to_json )

		termination_check_thread.raise 'stop:work_done'

		logger.info "Done"
	end

end
