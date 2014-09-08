import numpy as np

ALL_PERMS_MEMOIZE = {}

def all_perms(l, seqs):
	#seqs = list(seqs)

	# check cache
	cache_key = str( (l,seqs) )
	if cache_key in ALL_PERMS_MEMOIZE:
		return ALL_PERMS_MEMOIZE[cache_key]

	# handle end cases
	len_seqs = len(seqs)
	sum_seqs = sum(seqs)
	if len_seqs<=0 or l<=0: 
		return []

	if sum_seqs + len_seqs - 1 > l:
		#not enough space
		return []

	perms = []

	# iterate possible start indexes for the first block
	first, seqs = seqs[0], seqs[1:]
	max_index_for_first = l - first 

	for i in range( max_index_for_first + 1):
		curr_perm = np.zeros(l, dtype="int")
		curr_perm[i : i+first] = 1

		if len(seqs) > 0:
			remaining_length = l - i - first - 1
			remaining_perms = all_perms(remaining_length, seqs)

			for p in remaining_perms:
				new_perm = np.array(curr_perm)
				new_perm[-remaining_length : ] = p
				perms += [ new_perm ] 
		else:
			perms += [ curr_perm ]

	#add to cache and return
	ALL_PERMS_MEMOIZE[cache_key] = perms
	return perms


def precalculate_all_perms(board):
	# pre calcualte all perms
	perms_output = {}
	for idx, row in enumerate(board.rows()):
		all_perms_key = (len(row), str(board.constraints.rows[idx]))
		if all_perms_key not in perms_output:
			perms_output[all_perms_key] = all_perms(len(row), board.constraints.rows[idx])
	for idx, col in enumerate(board.columns()):
		all_perms_key = (len(col), str(board.constraints.columns[idx]))
		if all_perms_key not in perms_output:
			perms_output[all_perms_key] = all_perms(len(col), board.constraints.columns[idx])
	return perms_output

