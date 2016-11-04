#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division, print_function # python2.7 compatibility
# import exceptions as ex # in python3, we don't need to explicit import exceptions
import threading as th
import sys, os
sys.path.insert(0, os.path.abspath('..')) # TODO: is there a better way to do this?
from comms import Slaves
from src.main import Console

class App:
	def __init__(self):
		self.slaves = Slaves()
		telemetry = self.slaves.telemetry
		self.page = Console(telemetry, self.getTelemetry)
		self.page.startServer()

	def getTelemetry(self, requestedTelem):
		'''
		gets the value of a telemetry variable from the Slaves and gives it to Console
		this function is called from Console
		'''
		return self.slaves.get(requestedTelem)

if __name__ == '__main__':
	App()