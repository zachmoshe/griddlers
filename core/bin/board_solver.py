#! /usr/bin/env python

import sys
import os
sys.path.append("{}/..".format(os.path.dirname(__file__)))
import griddlers
import json 

STRATEGIES = { 
	'naive': griddlers.strategies.NaiveStrategy,
	'naive-probs': griddlers.strategies.ProbsStrategy,
	'naive-probs-guesser': griddlers.strategies.ProbsGuesserStrategy,
}

try:
	strategy_params = json.loads(sys.stdin.readline())
	request_params = json.loads(sys.stdin.readline())
	board_obj = json.loads(sys.stdin.readline())
	board = griddlers.Board.deserialize(board_obj)

	# build strategy
	if not strategy_params['name']:
		raise Exception("Can't find 'name' in strategy")
	if not strategy_params['name'] in STRATEGIES:
		raise Exception("Unknown strategy {}".format(strategy_params['name']))
	strategy = STRATEGIES[strategy_params['name']]
	strategy_params.pop("name")

	solver = griddlers.Solver(strategy, strategy_params, request_params)
	res = solver.solve(board)

	print(json.dumps(res))
	exit(0)

except Exception as ex:
	err = { 'status': 'error', 'message': str(ex) }
	print(json.dumps(err))
	sys.stderr.write(str(ex))
	exit(1)



