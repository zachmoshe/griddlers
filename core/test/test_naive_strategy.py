import pytest
import test_utils
import griddlers 
import numpy as np
from griddlers.strategies import ImpossibleBoardException

class TestNaiveStrategy:

	def test_simple_board(self):
		b = griddlers.Board(4, 4, [ [3], [1,1], [2], [1] ], [ [2], [1], [3], [2] ] )
		st = griddlers.strategies.NaiveStrategy(b)

		st.advance()
		exp1 = test_utils.build_board([ "*11*", "*01*", "*01*", "*00*" ])
		assert np.all(b.matrix == exp1.matrix)==True
		assert b.is_completed()==False
		assert b.is_legal()==True

		st.advance()
		exp2 = test_utils.build_board([ "1110", "1010", "0011", "0001" ])
		assert np.all(b.matrix == exp2.matrix)==True
		assert b.is_completed()==True
		assert b.is_legal()==True		

	def test_simple_board_2(self):
		b = griddlers.Board(3,3,[[2],[1],[1]], [[1],[1],[1,1]])
		st = griddlers.strategies.NaiveStrategy(b)

		st.advance()
		exp1 = test_utils.build_board(["*11", "*00", "*01"])
		assert np.all(b.matrix == exp1.matrix)
		assert b.is_completed() == False
		assert b.is_legal() == True

		st.advance()
		exp2 = test_utils.build_board(["011", "100", "001"])
		assert np.all(b.matrix == exp2.matrix)
		assert b.is_completed() == True
		assert b.is_legal() == True


	def test_board1(self):
		b = griddlers.Board(4,4, [[1], [], [2], []], [[], [1,1], [1], []])
		st = griddlers.strategies.NaiveStrategy(b)

		st.advance()
		exp1 = test_utils.build_board(["01*0", "0000", "01*0", "0000"])
		assert np.all(b.matrix == exp1.matrix)
		assert b.is_completed() == False
		assert b.is_legal() == True


	def test_board_without_enough_information(self):
		b = griddlers.Board(3,3, [ [1], [1], [1] ],  [ [1],[1],[1] ] )
		st = griddlers.strategies.NaiveStrategy(b)

		for i in range(5):
			st.advance()
			exp1 = test_utils.build_board([ "***", "***", "***" ])
			assert np.all(b.matrix == exp1.matrix) == True
			assert b.is_completed() == False
			assert b.is_legal() == True

	def test_impossible_board(self):
		b = test_utils.build_board([ "1**", "11*", "***"], [[1], [2], [1]], [[1],[2],[3]])
		st = griddlers.strategies.NaiveStrategy(b)

		with pytest.raises(ImpossibleBoardException):
			st.advance()

