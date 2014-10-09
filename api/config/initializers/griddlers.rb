config = HashWithIndifferentAccess.new

config[:strategies] = StrategiesConfig.new

Rails.application.config.griddlers = config