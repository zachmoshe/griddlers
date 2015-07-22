class GriddlersSolverWorker
	attr_accessor :queue_url
	attr_reader :poller, :s3, :logger

	def initialize(sqs_queue_url)
		raise ArgumentError, "invalid SQS queue URL" unless sqs_queue_url
		@queue_url = sqs_queue_url
		@poller = Aws::SQS::QueuePoller.new(queue_url)
		@s3 = Aws::S3::Client.new
		@logger = Rails.logger
	end  

	def poll
		poller.poll do |msg|
			handle_message msg
		end
	end


	protected
	def handle_message(msg)
		msg = Struct.new(:body).new( {"Bucket" => "dev-griddlers-work", "Key" => "0925c54244a5202b/request"}.to_json )

		s3Location = JSON.parse msg.body
		bucket, key = s3Location['Bucket'], s3Location['Key']
		work_id = key.split('/')[0]

		request = s3.get_object( bucket: bucket, key: key).body.read
		strategy, request_params, board = request.split("\n")


		# Send the python job
		result = nil
		error = nil
		output = nil

		core_path = "#{Rails.root}/../core"
		begin
			status = Open4::popen4("ulimit -v 400000 && #{core_path}/env/bin/python #{core_path}/bin/board_solver.py") do |pid, stdin, stdout, stderr|
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
				output = { 'status' => 'fatal-error', 'message' => error_message }
			end

		rescue Exception => ex
			output = { 'status' => 'fatal-error', 'message' => ex.message }
		end

		logger.info "Response for #{work_id} is #{output}"
		s3.put_object( bucket: bucket, key: "#{work_id}/response", body: output.to_json )
		puts "Done"
	end



end
