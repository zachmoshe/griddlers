class StrategiesConfig
  include ActiveModel::Model

  attr_accessor :strategies_names

  def initialize
    config_filename = Rails.root.join("..", "etc", "strategies.yml")
    config_file = YAML.load_file(config_filename.to_s)
    @config = config_file['strategies']
    raise RuntimeError, "illegal strategies config file format" unless @config

    self.strategies_names = @config.map{ |f,ss| ss.map{ |s,sc| self.class.get_strategy_name(f,s) } }.flatten
  end

  def [](strategy_name)
    strategy_name = strategy_name.to_s
    f,s = self.class.parse_strategy_name strategy_name
    begin
      conf = @config[f][s]
      raise Error unless conf
    rescue
      raise ArgumentError, "illegal strategy family #{f}" unless self.strategies_names.include? f
    end

    conf.with_indifferent_access
  end

  protected
  def self.get_strategy_name(family, st)
    st == 'default' ? family : "#{family}-#{st}"
  end

  def self.parse_strategy_name(st)
    if st.include? '-'
      return st.split('-', 2)
    else
      return st, 'default'
    end
  end
end