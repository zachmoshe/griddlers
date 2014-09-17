from . import perms_utils
import numpy as np


class NaiveStrategy(object):

	def __init__(self, board, params={}):
		self.board = board
		#self.all_perms = perms_utils.precalculate_all_perms(self.board)

		
	def advance(self):
		for idx, row in enumerate(self.board.rows()):
			self.board.matrix[idx] = self.naive_calc_probs( row, self.board.constraints.rows[idx] )

		for idx, col in enumerate(self.board.columns()):
			self.board.matrix[:,idx] = self.naive_calc_probs( col, self.board.constraints.columns[idx] ) 

		return


	def naive_calc_probs(self, curr_probs, seqs):
		l = len(curr_probs)
		p_black = np.array( [True] * l )
		p_white = np.array( [True] * l )

		#possible_perms = self.all_perms[(l, str(seqs))]
		possible_perms = perms_utils.all_perms_gen(l,seqs)

		if l-sum(seqs)-len(seqs)+1 < 0:
			return np.zeros(l)

		for perm in possible_perms:
			# check if perm is legal
			if any(  (  (perm==0) & (curr_probs==1) )  |  
				      (   (perm==1) & (curr_probs==0) ) ):
				continue
			p_white &= perm==0 
			p_black &= perm==1

		curr_probs[ p_black ] = 1
		curr_probs[ p_white ] = 0
		return curr_probs
