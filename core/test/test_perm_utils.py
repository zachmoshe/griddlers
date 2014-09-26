import pytest
from griddlers.strategies.perms_utils import all_perms, all_perms_gen
import numpy as np

def assert_perms(l, seqs, expected):
	actual = list(map(list, all_perms(l, seqs)))
	actual.sort()
	expected.sort()
	assert actual == expected

	actual = list(map(list, all_perms_gen(l, seqs)))
	actual.sort()
	expected.sort()
	assert actual == expected

def test_impossible_too_small():
	assert_perms(3, [4], [])
	assert_perms(3, [1,2], [])

def test_empty_seqs():
	assert_perms(0, [], [])
	assert_perms(1, [], [ [0] ])
	assert_perms(2, [], [ [0,0] ])
	assert_perms(3, [], [ [0,0,0] ])

def test_exactly_one_solution():
	assert_perms(1, [1], [ [1] ])
	assert_perms(3, [1,1], [[1,0,1]])
	assert_perms(4, [1,2], [ [1,0,1,1]])

def test_symmetrical_options():
	assert_perms(2,[1], [ [0,1], [1,0] ])
	assert_perms(4, [1,1], [ [1,0,1,0], [0,1,0,1], [1,0,0,1] ])

def test_multiple_solutions():
	assert_perms(3, [1], [ [0,0,1], [0,1,0], [1,0,0]])
	assert_perms(3, [2], [ [1,1,0], [0,1,1]])
	assert_perms(4, [2], [ [1,1,0,0], [0,1,1,0], [0,0,1,1]])
	assert_perms(5, [1,2], [ [1,0,1,1,0], [1,0,0,1,1], [0,1,0,1,1] ])
