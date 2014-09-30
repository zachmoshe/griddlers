#! /usr/bin/env python3
import sys
import os
sys.path.append("{}/..".format(os.path.dirname(__file__)))

import griddlers
import numpy as np 
import json

def get_steps(res):
	return [ np.array(x['board']['matrix']) for x in res['iterations'] ]

def calc_for_step(step, final):
	step_pos = np.array([ ((r,c),step[(r,c)]) for r in range(len(st1)) for c in range(len(st1[r])) ])
	step_pos = [ x for x in step_pos if x[1]>0 and x[1]<1 ]
	step_sort = sorted(step_pos, key=lambda x: -x[1])
	step_sort_in_final = [ final[(x[0])] for x in step_sort ]

	# generate list of tuples with (percentile,mistake-rate (% of 0))
	out = []
	l = len(step_sort_in_final)
	cnt_0 = 0
	for i in range(l):
		if step_sort_in_final[i] == 0:
			cnt_0+=1
		out += [ (i/l , cnt_0/(i+1)) ]

	return out


if __name__ == '__main__':
	board_filename = "file:examples/2.non"
	board = griddlers.parsers.NONParser.parse(board_filename)

	solver = griddlers.Solver(griddlers.strategies.ProbsStrategy)
	res = solver.solve(board)

	steps = get_steps(res)
	final = steps[-1]
	st1 = steps[0]

	all_stats = [ calc_for_step(st, final) for st in steps ]

	cnt = 1
	for stat in all_stats:
		print("step {}".format(cnt))
		cnt+=1
		print(",".join([ str(x[0]) for x in stat ]))
		print(",".join([ str(x[1]) for x in stat ]))
