from . import perms_utils, ImpossibleBoardException
import numpy as np 


class ProbsStrategy(object):

	def __init__(self, board, params={}):
		self.board = board
		self.params = params

		if self.params.get('speedy'):
			self.all_perms = perms_utils.precalculate_all_perms(self.board)


	def advance(self):
		for idx, row in enumerate(self.board.rows()):
			self.board.matrix[idx] = self.calc_probs( row, self.board.constraints.rows[idx] )

		for idx, col in enumerate(self.board.columns()):
			self.board.matrix[:,idx] = self.calc_probs( col, self.board.constraints.columns[idx] ) 


	def calc_probs(self, curr_probs, seqs):
		l = len(curr_probs)
		cnts = np.zeros(l)

		if self.params.get('speedy'):
			possible_perms = self.all_perms[(l, str(seqs))]
		else: 
			possible_perms = perms_utils.all_perms_gen(l,seqs)

		if l-sum(seqs)-len(seqs)+1 < 0:
			return cnts

		had_legal_perm = False
		for perm in possible_perms:
			# check if perm is legal
			if any( ( (perm==0) & (curr_probs==1) )  |  
				      ( (perm==1) & (curr_probs==0) ) ):
				continue
			had_legal_perm = True
			total_curr_probs = sum(curr_probs[ perm == 1 ])

			cnts += perm * total_curr_probs

		if not had_legal_perm:
			raise ImpossibleBoardException()
		
		cnts[ curr_probs == 0 ] = 0
		
		# normalize - take out all 1s and split the rest according to the weights
		num_unsure = max( 0, sum(seqs) - sum(curr_probs==1) )

		num_uncertain_probs = sum(cnts[ curr_probs < 1 ])
		if num_uncertain_probs == 0:
			factor = 1
		else:
			factor = num_unsure / num_uncertain_probs

		cnts[ curr_probs >= 1 ] = 1
		cnts[ curr_probs < 1 ] *= factor
		cnts[ cnts>=0.999 ] = 1

		return cnts

