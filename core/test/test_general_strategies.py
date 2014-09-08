import pytest
import test_utils
import griddlers 
import numpy as np

strategies = [ griddlers.strategies.NaiveStrategy, griddlers.strategies.ProbsStrategy ]


class TestGeneralStrategies:
	def test_doesnt_change_certain(self):
		bs = [ 
			test_utils.build_board(["0**", "11*", "00*"], [[1], [2], []], [[1], [2], [1]]),
			test_utils.build_board(["000", "111", "000"], [[], [3], []], [[1], [1], [1]]),
			test_utils.build_board(["0**", "*1*", "*0*"], [[1], [2], []], [[1], [2], [1]]),
		]
		
		for b in bs:
			b_orig = np.array(b.matrix)

			for st_cls in strategies:
				st = st_cls(b)
				st.advance()

				assert np.all(b.matrix[ b_orig==1 ] == 1)
				assert np.all(b.matrix[ b_orig==0 ] == 0)
		