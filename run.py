#!/usr/bin/env python

import os, sys

############
# Helpers
############
def console(s):
	sys.stdout.write(">> %s" % s)

def error(s):
	sys.stderr.write(">> [ERROR] %s" % s)

################
# Major Methods
################
def runserver():
	command = 'python manage.py runserver'
	os.system(command)

def main():
	runserver()
	return

if __name__ == "__main__":
	main()