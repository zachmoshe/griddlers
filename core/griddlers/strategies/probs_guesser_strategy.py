from . import ProbsStrategy
import numpy as np  

DEFAULT_PARAMS = { 
	"board-size-threshold": 300,
	"uncertain-pct-threshold": 0.5,
	"top-dark-cells-pct-threshold": 0.03,
	"top-dark-cells-score-threshold": 0.92,
}


class ProbsGuesserStrategy(ProbsStrategy):

	def __init__(self, board, params={}):
		super().__init__(board, params)
		self.params = DEFAULT_PARAMS.copy()
		self.params.update(params)


	def advance(self):
		super().advance()

		# if board is large enough (>BOARD_SIZE_THRESHOLD) and there are enough uncertain cells (>UNCERTAIN_PCT_THRESHOLD)
		# then sort all cells by score and set value to 1 for those which (AND):
		# 1. are in the top TOP_DARK_CELLS_PCT_THRESHOLD
		# 2. their score is above TOP_DARK_CELLS_SCORE_THRESHOLD
		num_cells = self.board.num_cells()
		num_certain = self.board.num_certain()
		num_uncertain = num_cells - num_certain
		if num_cells > self.params['board-size-threshold'] and num_uncertain / num_cells > self.params['uncertain-pct-threshold']:
			all_valid_uncertain = [ ((i,j), self.board.matrix[i][j]) for i in range(self.board.num_rows()) for j in range(self.board.num_columns())  
				if self.params['top-dark-cells-score-threshold'] < self.board.matrix[i][j] < 1 ]
			all_valid_uncertain_sorted = sorted(all_valid_uncertain, key=lambda x: -x[1])
			top_cells = all_valid_uncertain_sorted[0:int(self.params['top-dark-cells-pct-threshold']*num_uncertain)]

			# set them to black - CHANGE THIS LATER
			for top_cell in top_cells:
				r,c = top_cell[0]
				if 	(sum(self.board.rows()[r] == 1) < sum(self.board.constraints.rows[r])) and \
					(sum(self.board.columns()[c] == 1) < sum(self.board.constraints.columns[c])):
					# print("changing cell {}".format(top_cell[0]))
					self.board.matrix[top_cell[0]] = 1

