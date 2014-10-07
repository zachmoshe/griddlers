Rails.application.config.google_analytics = HashWithIndifferentAccess.new

config = YAML.load_file(Rails.root.join("config", "google_analytics.yml"))[Rails.env]
if config
  Rails.application.config.google_analytics.update(config)
end