class ImpossibleBoardException(Exception):
  pass

from .naive_strategy import NaiveStrategy
from .probs_strategy import ProbsStrategy
from .probs_guesser_strategy import ProbsGuesserStrategy
