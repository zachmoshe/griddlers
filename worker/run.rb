#! /usr/bin/env ruby

require 'aws-sdk'
require_relative 'griddlers_solver_worker'

if ENV['GRIDDLERS_WORKER_DEVELOPMENT']
  sts = Aws::STS::Client.new( credentials: Aws::SharedCredentials.new( profile_name: 'admin' ) )
  creds = Aws::AssumeRoleCredentials.new \
    client: sts,
    role_arn: 'arn:aws:iam::591152932423:role/dev_griddlers_worker',
    role_session_name: 'zach'
else 
  creds = Aws::InstanceProfileCredentials.new
end

Aws.config[:credentials] = creds


queue_url = ENV['SQS_WORK_QUEUE_URL']
new_work_topic_arn = ENV['SNS_NEW_WORK_TOPIC_ARN']
GriddlersSolverWorker.new(queue_url, new_work_topic_arn).poll
