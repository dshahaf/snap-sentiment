#!/usr/bin/env python

import os, sys

############
# Helpers
############
def console(s):
	sys.stdout.write(">> %s" % s)

def error(s):
	sys.stderr.write(">> [ERROR] %s" % s)

def getLessPaths():
	ret = []
	ret.append('sentiment/static/style.less')
	return ret

################
# Major Methods
################
def compileLess():
	lessPaths = getLessPaths()
	for lessPath in lessPaths:
		newPath = lessPath[:-4] + 'css'
		os.system("lessc %s %s" % (lessPath, newPath))
		console("Compiled %s" % newPath)
	return

def main():
	compileLess()
	return

if __name__ == "__main__":
	main()