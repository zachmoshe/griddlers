import numpy as np
import griddlers

# builds a board from the following string representation
#build_board( 
#	"10001",
#	"00111",
#	"11100"
#	)
def value_tr(strval):
	if strval=="0": return 0
	if strval=="1": return 1
	if strval=="*": return None
	raise ValueError

def  build_board(l_str, rows_constraints=None, cols_constraints=None):
	num_rows = len(l_str)
	cols_lengths = list(map(len, l_str))
	cols_lengths.sort()
	if len(cols_lengths)>0 and cols_lengths[0] != cols_lengths[-1]:
		raise ValueError("illegal string representation of a board. columns lengths are not the same")
	num_cols = cols_lengths[0] if len(cols_lengths) else 0

	if rows_constraints==None: rows_constraints=[[]]*num_rows
	if cols_constraints==None: cols_constraints=[[]]*num_cols

	b = griddlers.Board(num_rows, num_cols, rows_constraints, cols_constraints)
	for idx, row_str in enumerate(l_str):
		row = np.array(list(map(value_tr, row_str)))
		b.rows()[idx] = row

	b.matrix[ np.isnan(b.matrix) ] = 1.0/(num_rows*num_cols)	
	return b

FLOAT_CMP_PERCISION = 1e-5
def float_equals(m1,m2):
	if len(m1) != len(m2): return False
	for i in range(len(m1)):
		if len(m1[i]) != len(m2[i]): return False
		for j in range(len(m1[i])):
			if abs(m1[i][j] - m2[i][j]) > FLOAT_CMP_PERCISION: return False
	return True
