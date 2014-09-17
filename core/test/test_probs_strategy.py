import pytest
import test_utils
import griddlers 
import numpy as np

class TestProbsStrategy:

	def test_simple_board(self):
		b = griddlers.Board(3,3,[[1,1],[1,1],[1,1]], [[3],[],[3]])
		st = griddlers.strategies.ProbsStrategy(b)

		st.advance()
		assert np.all(b.matrix == [[1,0,1], [1,0,1], [1,0,1]])
		assert b.is_completed() == True
		assert b.is_legal() == True

	def test_simple_board_2(self):
		b = griddlers.Board(3,3,[[1],[2],[3]], [[3],[2],[1]])
		st = griddlers.strategies.ProbsStrategy(b)

		st.advance()
		assert np.all(b.matrix == [[1,0,0], [1,1,0], [1,1,1]])
		assert b.is_completed() == True
		assert b.is_legal() == True
		
	def test_simple_board_3(self):
		b = griddlers.Board(3,3,[[2],[1],[1]], [[1],[1],[1,1]])
		st = griddlers.strategies.ProbsStrategy(b)

		st.advance()
		assert test_utils.float_equals(b.matrix, [[3./7,1,1], [2./7,0,0], [2./7,0,1]])
		assert b.is_completed() == False
		assert b.is_legal() == True

		st.advance()
		assert test_utils.float_equals(b.matrix, [[0,1,1], [1,0,0], [0,0,1]])
		assert b.is_completed() == True
		assert b.is_legal() == True



	def test_impossible_board(self):
		b = griddlers.Board(3,3,[[1],[1],[2]], [[1],[2],[1]])
		st = griddlers.strategies.ProbsStrategy(b)

		st.advance()
		assert test_utils.float_equals(b.matrix,  [[6./21,0,6./21], [6./21,1,6./21], [9./21,1,9./21]])
		assert b.is_completed() == False
		assert b.is_legal() == True

		for i in range(5):
			st.advance()
			assert test_utils.float_equals(b.matrix,  [[0.5,0,0.5], [0,1,0], [0.5,1,0.5]])
			assert b.is_completed() == False
			assert b.is_legal() == True


	def test_impossible_board_2(self):
		b = griddlers.Board(3,3,[[1],[1],[1]], [[1],[2],[]])
		st = griddlers.strategies.ProbsStrategy(b)

		st.advance()
		assert test_utils.float_equals(b.matrix, [[1./3,1./2,0], [1./3,1,0], [1./3,1./2,0]])
		assert b.is_completed() == False
		assert b.is_legal() == True

		for i in range(5):
			st.advance()
			assert test_utils.float_equals(b.matrix, [[0.5,0.5,0],[0,1,0],[0.5,0.5,0]])
			assert b.is_completed() == False
			assert b.is_legal() == True
