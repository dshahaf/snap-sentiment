#!/usr/bin/env python

import os, sys

############
# Helpers
############
def console(s):
	sys.stdout.write(">> %s\n" % s)

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
	console('Compiling Less Files...')
	lessPaths = getLessPaths()
	for lessPath in lessPaths:
		newPath = lessPath[:-4] + 'css'
		os.system("lessc %s %s" % (lessPath, newPath))
		console("Compiled %s" % newPath)
	return

def compileCoffee():
	console('Compiling Coffeescript Files...')
	command = ""

def main():
	compileLess()
	compileCoffee()
	return

if __name__ == "__main__":
	main()