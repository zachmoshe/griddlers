try:
	# For python 3
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen

from griddlers.board import Board


from . import non_parser as NONParser