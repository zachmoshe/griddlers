#! /usr/bin/env python

import sys
import os
sys.path.append("{}/..".format(os.path.dirname(__file__)))
import griddlers
import json 
import traceback



config = griddlers.GriddlersConfig()

try:
	strategy_params = json.loads(sys.stdin.readline())
	request_params = json.loads(sys.stdin.readline())
	board_obj = json.loads(sys.stdin.readline())
	board = griddlers.Board.deserialize(board_obj)

	# build strategy
	if not strategy_params['name']:
		raise Exception("Can't find 'name' in strategy")
	if not strategy_params['name'] in config.strategies_names:
		raise Exception("Unknown strategy {}".format(strategy_params['name']))
	strategy_class = eval("griddlers.strategies.{}".format(config.get_strategy(strategy_params['name'])['python_class']))
	strategy_allowed_params = [ p['name'] for p in config.get_strategy(strategy_params['name'])['params'] ]
	strategy_params.pop("name")

	illegal_params = [ p for p in strategy_params if p not in strategy_allowed_params ]
	if illegal_params:
		raise ValueError("illegal params - {}".format(", ".join(illegal_params)))

	solver = griddlers.Solver(strategy_class, strategy_params, request_params)
	res = solver.solve(board)

	print(json.dumps(res))
	exit(0)

except MemoryError as ex:
	sys.stderr.write("Memory Error {}".format(str(ex)))
	exit(1)

except Exception as ex:
	err = { 'status': 'error', 'message': str(ex) }
	print(json.dumps(err))
	sys.stderr.write(traceback.format_exc())
	exit(250)



