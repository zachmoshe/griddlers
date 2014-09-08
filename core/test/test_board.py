import pytest
import test_utils
import griddlers

class TestBoard:
	def test_ctr_illegal_board_size_rows_0(self):
		# rows = 0, cols = 0
		with pytest.raises(ValueError):
			test_utils.build_board([], [], [])

	def test_ctr_illegal_board_size_cols_0(self):
		# rows = 3, cols = 0
		with pytest.raises(ValueError):
			test_utils.build_board([[],[],[]], [[],[],[]], [])

	def test_legal_board_size_1_1(self):
		b = test_utils.build_board(["1"], [[1]], [[1]])
		assert len(b.rows()) == 1
		assert len(b.columns()) == 1
		assert b.constraints.rows == [ [1] ]
		assert b.constraints.columns == [ [1] ]
		assert b.is_legal() == True
		assert b.is_completed() == True
		assert b.shape() == (1,1)
		assert b.num_certain() == 1

	def test_legal_board_size_3_3(self):
		b = test_utils.build_board(["000","101", "111"], [[],[1,1],[3]], [[2],[1],[2]])
		assert len(b.rows()) == 3
		assert len(b.columns()) == 3
		assert b.constraints.rows == [ [], [1,1], [3] ]
		assert b.constraints.columns == [ [2], [1], [2] ]
		assert b.is_legal() == True
		assert b.is_completed() == True
		assert b.shape() == (3,3)
		assert b.num_certain() == 9

	def test_non_square_board(self):
		b = griddlers.Board(2,4, [[]]*2, [[]]*4)
		b.matrix[1,3] = 1
		b.matrix[0,3] = 0
		assert b.shape() == (2,4)
		assert b.num_certain() == 2

	def test_ctr_illegal_constraints_1(self):
		with pytest.raises(ValueError):
			test_utils.build_board([
				"101",
				"000"
				], [],[])

	def test_ctr_illegal_constraints_2(self):
		b = test_utils.build_board([
				"101",
				"000"
				], [[1], []],[[1], [], [1]])
		assert b.is_legal() == False
		assert b.is_completed() == True

	def test_ctr_illegal_constraints_3(self):
		b = test_utils.build_board([
				"101",
				"000"
				], [[1,1],[]],[[1],[1],[1]])
		assert b.is_legal() == False
		assert b.is_completed() == True

	def test_serialize_deserialize(self):
		b = test_utils.build_board([ "1"], [[]], [[]])
		b2 = griddlers.Board.deserialize(b.serialize())
		assert b==b2
		
		b = test_utils.build_board([ "000", "111"], [[1]]*2, [[]]*3)
		b2 = griddlers.Board.deserialize(b.serialize())
		assert b==b2

	def test_util_funcs(self):
		b = test_utils.build_board([ "010", "111" ], [[]]*2, [[]]*3)
		assert b.shape() == (2,3)
		assert b.num_cells() == 6
		assert b.num_certain() == 6

		b = test_utils.build_board(["000", "000", "000"], [[]]*3, [[]]*3)
		assert b.shape() == (3,3)
		assert b.num_cells() == 9
		assert b.num_certain() == 9

		b.matrix[0:2,0:2] = 0.5
		assert b.num_cells() == 9
		assert b.num_certain() == 5



