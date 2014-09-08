from . import *
import re

def read_url( url ):
	f = urlopen(url)
	myfile = f.read()
	return myfile


def parse(url):
	url_str = read_url(url).decode("utf-8")   # notice that in python3 read_url returns a 'bytes' object and in python2 it's 'str'

	w = re.search( 'width (\d+)', url_str).group(1)
	h = re.search( 'height (\d+)', url_str).group(1)
	rows = [ [ int(z) for z in x.split(',') ] for x in re.search( 'rows\n([\d,\n]+)', url_str ).group(1).split('\n') if len(x)>0]
	cols = [ [ int(z) for z in x.split(',') ] for x in re.search( 'columns\n([\d,\n]+)', url_str ).group(1).split('\n') if len(x)>0]
	 
	return Board(int(h), int(w), rows, cols)
