from . import ProbsStrategy
import numpy as np  


BOARD_SIZE_THRESHOLD = 500
UNCERTAIN_PCT_THRESHOLD = 0.5
TOP_DARK_CELLS_PCT_THRESHOLD = 0.015
TOP_DARK_CELLS_SCORE_THRESHOLD = 0.92

class ProbsGuesserStrategy(ProbsStrategy):

	def advance(self):
		#print("is the board legal before super()? {}".format(self.board.is_legal()))
		super().advance()

		#print("is the board legal after super()? {}".format(self.board.is_legal()))
		# if board is large enough (>BOARD_SIZE_THRESHOLD) and there are enough uncertain cells (>UNCERTAIN_PCT_THRESHOLD)
		# then sort all cells by score and set value to 1 for those which (AND):
		# 1. are in the top TOP_DARK_CELLS_PCT_THRESHOLD
		# 2. their score is above TOP_DARK_CELLS_SCORE_THRESHOLD
		num_cells = self.board.num_cells()
		num_certain = self.board.num_certain()
		num_uncertain = num_cells - num_certain
		# print("board size - {} , num_uncertain - {}".format(num_cells, num_uncertain))
		if num_cells > BOARD_SIZE_THRESHOLD and num_uncertain / num_cells > UNCERTAIN_PCT_THRESHOLD:
			all_valid_uncertain = [ ((i,j), self.board.matrix[i][j]) for i in range(self.board.num_rows()) for j in range(self.board.num_columns())  
				if TOP_DARK_CELLS_SCORE_THRESHOLD < self.board.matrix[i][j] < 1 ]
			# print("all_valid_uncertain - {}".format(all_valid_uncertain))
			all_valid_uncertain_sorted = sorted(all_valid_uncertain, key=lambda x: -x[1])
			top_cells = all_valid_uncertain_sorted[0:int(TOP_DARK_CELLS_PCT_THRESHOLD*num_uncertain)]

			# set them to black - CHANGE THIS LATER
			# print("changing these: {}".format(top_cells))
			for top_cell in top_cells:
				# print("changing cell {}".format(top_cell[0]))
				self.board.matrix[top_cell[0]] = 1
				# print("is it legal? {}".format(self.board.is_legal()))

