class GriddlersSolverWorker
  include Sidekiq::Worker
  sidekiq_options :retry => false


  def perform(request_id)
    bpr = BoardProcessingRequest.find request_id

    bpr.update_attributes! started_at: Time.now

    result = nil
    error = nil

    core_path = "#{Rails.root}/../core"
    status = Open4::popen4("ulimit -v 400000 && #{core_path}/env/bin/python #{core_path}/bin/board_solver.py") do |pid, stdin, stdout, stderr|
      logger.info "Starting board_solver.py for request #{bpr.id} [PID=#{pid}]"

      stdin.puts(JSON.dump bpr.strategy)
      stdin.puts(JSON.dump bpr.request_params)
      stdin.puts(bpr.board.dump)
      stdin.close

      result = stdout.read.strip
      error = stderr.read.strip
    end

    logger.info "board_solver.py [PID=#{status.pid}] ended. <exitstatus=#{status.exitstatus}> , <error=#{error}>"


    if [0,250].include? status.exitstatus  # 0 for successful run and 250 for regular error (normal output of the script)
      bpr.result = JSON.load(result)
    else
      # handle fatal errors (where we couldn't even run the solver script in a similar way to "regular" errors)
      error_message = error.split(/[:\n]/).last.strip
      bpr.result = { 'status' => 'fatal_error', 'message' => error_message }
    end

    bpr.status = bpr.result['status'] rescue nil

    bpr.completed_at = Time.now
    bpr.save!

  end
end
