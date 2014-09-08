import pytest
import griddlers
import json
import sys
from subprocess import Popen, PIPE
import os


def run_solver(board, strategy_params, request_params):
	path = "{}/..".format(os.path.dirname(__file__))
	proc = Popen([ "{}/env/bin/python".format(path) , "{}/bin/board_solver.py" ], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
	input_str = "{}\n{}\n{}".format( json.dumps(strategy_params), json.dumps(request_params), json.dumps(board.serialize()))
	if sys.version_info[0] == 3:
		input_str = bytes(input_str, 'UTF-8')
	proc.stdin.write(input_str)
	stdout, stderr = proc.communicate()

	if sys.version_info[0] == 3:
		out = json.loads(str(stdout, 'UTF-8"')) if stdout!=b'' else None
		err = str(stderr, "UTF-8") if stderr!=b'' else None
	else:
		out = json.loads(stdout)
		err = stderr if  stderr!="" else None
			
	return out,err



class TestPythonSolver(object):

	def test_normal_run_naive(self):
		b = griddlers.Board(4,4, [[1], [], [2], []], [[], [1,1], [1], []])
		out,err = run_solver(b, {'name': 'naive'}, {})
		assert err == None
		assert out['status'] == 'success'
		assert len(out['iterations']) == 2

	def test_normal_run_probs(self):
		b = griddlers.Board(4,4, [[1], [], [2], []], [[], [1,1], [1], []])
		out,err = run_solver(b, {'name': 'naive-probs'}, {})
		assert err == None
		assert out['status'] == 'success'
		assert len(out['iterations']) == 2

	def test_unknown_strategy(self):
		b = griddlers.Board(4,4, [[1], [], [2], []], [[], [1,1], [1], []])
		out,err = run_solver(b, {'name': 'UNKNOWN'}, {})
		assert out['status'] == 'error'
		assert "unknown strategy" in out['message'].lower()
		assert err != None

	def test_request_params(self):
		board_str = "{\"matrix\":[[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444],[0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444,0.0044444444444444444]],\"constraints\":{\"rows\":[[5],[2,2,2],[1,1,1],[2,2],[1,1,2],[1,1,1,2],[1,2,1,2],[1,2,1,1],[1,2,1,2,3],[1,2,1,1,1],[1,2,3],[9],[1,1],[2,2],[1,1]],\"columns\":[[6],[2,1],[3,4,1],[1,4,1],[1,1,1,2],[1,6,1],[3,3],[2,1],[1,2,1,1],[1,5],[2,1,1],[1,3,2],[2,1],[5],[2]]}}"

		b = griddlers.Board.deserialize(json.loads(board_str))
		out,err = run_solver(b, {'name': 'naive-probs'}, {'max-iters': 5})
		assert out['status'] == 'partially-success'
		assert len(out['iterations']) == 5
		assert err == None

