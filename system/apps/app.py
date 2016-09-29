#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division, print_function # python2.7 compatibility
# import exceptions as ex # in python3, we don't need to explicit import exceptions
import threading as th
# from comms import # TODO: import the communications systems here s.t. we can get its data
import sys, os
sys.path.insert(0, os.path.abspath('..')) # TODO: is there a better way to do this?
from src.main import Main

class App:
	def __init__(self):
		self.page = Main()
		self.page.start_server()

if __name__ == '__main__':
	App()