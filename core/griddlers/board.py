import numpy as np 
import json

class BoardConstraints(object):
	def __init__(self, rows_constraints, columns_constraints):
		self.rows = rows_constraints
		self.columns = columns_constraints

	def __eq__(self, other): 
		if isinstance(other, BoardConstraints):
			return self.rows == other.rows and self.columns == other.columns
		return False


class Board(object):

	def __init__(self, n_rows, n_columns, rows_constraints, columns_constraints):
		if n_rows > 0 and n_columns > 0:
			self.matrix = np.empty((n_rows, n_columns))
			self.matrix.fill(1.0/(n_rows*n_columns))
		else:
			raise ValueError("illegal board size")

		if len(rows_constraints) == n_rows and len(columns_constraints) == n_columns:
			self.constraints = BoardConstraints(rows_constraints, columns_constraints)
		else:
			raise ValueError("constraints don't match board size")

	def __str__(self):
		return "(%dx%d)\n%s\nrows=%s\ncolumns=%s" % (self.matrix.shape[0], self.matrix.shape[1], self.matrix, self.constraints.rows, self.constraints.columns)
	def __repr__(self):
		return self.__str__()

	def __eq__(self, other): 
		if isinstance(other, Board):
			return (self.matrix == other.matrix).all() and \
				self.constraints == other.constraints
		return False

	def serialize(self):
		obj = {
			'matrix': self.matrix.astype(float).tolist(),
			'constraints': {
				'rows': self.constraints.rows,
				'columns': self.constraints.columns,
			}
		}
		return obj

	@staticmethod
	def deserialize(obj):
		num_rows = len(obj['constraints']['rows'])
		num_columns = len(obj['constraints']['columns'])
		b = Board(num_rows, num_columns, obj['constraints']['rows'], obj['constraints']['columns'])
		b.matrix = np.array(obj['matrix'])
		return b

	def rows(self):
		return self.matrix

	def columns(self):
		return self.matrix.T

	def shape(self):
		return self.matrix.shape

	def num_rows(self):
		return self.shape()[0]

	def num_columns(self):
		return self.shape()[1]

	def num_cells(self):
		return self.shape()[0] * self.shape()[1]

	def is_completed(self):
		return np.all(np.bitwise_or(self.matrix==0, self.matrix==1))

	def is_legal(self):
		# check that constraints are possible with the given board
		for cells, constraint in zip( list(self.rows()) + list(self.columns()) , self.constraints.rows + self.constraints.columns ):
			sum_constraint = sum(constraint)
			min_possible_certain = sum(cells == 1)
			max_possible_certain = min_possible_certain + sum(np.bitwise_and(cells>0, cells<1))

			if sum_constraint<min_possible_certain or sum_constraint>max_possible_certain:
				#print("not legal because of cells - {}     and constraints - {}".format(cells, constraint))
				return False

		return True

	def num_certain(self):
		return int(np.sum((self.matrix == 0) | (self.matrix == 1)))

	