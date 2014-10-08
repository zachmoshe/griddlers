DEFAULT_STRATEGIES_FILE_ENV_VARIABLE = "STRATEGIES_CONFIG_FILE"

import yaml
import os

def get_strategy_name(family, st):
  if st == 'default':
    return family
  else:
    return "{}-{}".format(family, st)


class GriddlersConfig(object):

  def __init__(self):
    strategies_filename = os.environ.get(DEFAULT_STRATEGIES_FILE_ENV_VARIABLE)
    self.strategies = yaml.load(open(strategies_filename, 'r'))['strategies']
    self.strategies_names = [ get_strategy_name(family, strategy) for family in self.strategies for strategy in self.strategies[family] ]

  def get_strategy(self, strategy_name):
    if '-' in strategy_name:
      strategy_family, strategy_name = strategy_name.split('-')
    else:
      strategy_family = strategy_name
      strategy_name = 'default'

    if strategy_family not in self.strategies:
      raise ValueError("can't find strategy family {} in strategies config file".format(strategy_family))
    
    if strategy_name not in self.strategies[strategy_family]:
      raise ValueError("can't find strategy {} in strategy family {}".format(strategy_name, strategy_family))
    
    strategy_conf = self.strategies[strategy_family][strategy_name]
    if 'params' not in strategy_conf:
      strategy_conf['params'] = []

    return strategy_conf    


            