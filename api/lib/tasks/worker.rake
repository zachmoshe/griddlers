namespace :worker do
  desc "Runs a Griddlers worker and "
  task run: :environment do

    sts = Aws::STS::Client.new( credentials: Aws::SharedCredentials.new( profile_name: 'admin' ) )
    
    creds = Aws::AssumeRoleCredentials.new \
      client: sts,
      role_arn: 'arn:aws:iam::591152932423:role/dev_griddlers_worker',
      role_session_name: 'zach'
    
    Aws.config[:credentials] = creds


    queue_url = ENV['SQS_WORK_QUEUE_URL']
    GriddlersSolverWorker.new(queue_url).poll
    
  end

end
