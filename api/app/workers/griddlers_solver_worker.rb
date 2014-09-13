class GriddlersSolverWorker
  include Sidekiq::Worker
  sidekiq_options :retry => false


  def perform(request_id)
    bpr = BoardProcessingRequest.find request_id

    bpr.update_attributes! started_at: Time.now

    core_path = "#{Rails.root}/../core"
    status = Open4::popen4("ulimit -v 350000 && #{core_path}/env/bin/python #{core_path}/bin/board_solver.py") do |pid, stdin, stdout, stderr|
      logger.info "Starting board_solver.py for request #{bpr.id} [PID=#{pid}]"

      stdin.puts(JSON.dump bpr.strategy)
      stdin.puts(JSON.dump bpr.request_params)
      stdin.puts(bpr.board.dump)
      stdin.close

      result = stdout.read.strip
      error = stderr.read.strip

      bpr.result = JSON.load(result)

      unless error.empty?
        # stderr has the full error
        logger.info "Error in job - #{error}"
      end
      logger.info "board_solver.py [PID=#{pid}] ended."
    end

    bpr.completed_at = Time.now
    bpr.save!

  end
end
