import griddlers.strategies as strategies
import copy
import numpy as np
import time 
import sys
from griddlers.strategies import ImpossibleBoardException

SOLVER_DEFAULT_PARAMS = { 
	"max-iters": 100,
	"avg-change-threshold": 1e-5,
}

class Solver(object):

	def __init__(self, strategy_class, strategy_params={}, request_params={}):
		self.strategy_class = strategy_class
		self.strategy_params = strategy_params
		self.params = SOLVER_DEFAULT_PARAMS.copy()
		self.params.update(request_params)

	def solve(self, board):
		if not board.is_legal():
			raise ValueError('given board is illegal')

		strategy = self.strategy_class(board, self.strategy_params)

		# main loop
		iterations = []
		iter_num = 0
		keep_running = True
		while keep_running:
			iter_num += 1
			
			board_before = copy.deepcopy(board)
			time_before = time.time()
			try:
				strategy.advance()
			except ImpossibleBoardException:
				break  # exit the "while keep_running" loop

			time_elapsed = time.time() - time_before

			if not board.is_legal():
				raise ValueError("strategy failure. illegal board")

			# calculating some stats
			board_diff = board.matrix - board_before.matrix
			changed_values = board_diff[board_diff != 0]
			num_changed_cells = int(np.sum(board_diff!=0))
			avg_change = np.average(np.abs(changed_values)) if len(changed_values) > 0 else 0

			keep_running = not board.is_completed() and \
							 num_changed_cells > 0 and \
							 iter_num < self.params['max-iters'] and \
							 avg_change > self.params['avg-change-threshold']

			iterations += [ 
				{ 
					'iteration_number': iter_num,
					'board': board.serialize(),
					'stats': {
						'pct_certain': float(board.num_certain()) / board.num_cells(),
						'pct_change': float(num_changed_cells) / board.num_cells(),
						'avg_change': avg_change,
						'time_elapsed': time_elapsed,
					},
				}
			 ]
				
		obj = { 
			'status': (board.is_completed() and board.is_legal() and 'success') or 'partially-success',
			'iterations': iterations,
			'stats': {},
		}
		return obj



		


