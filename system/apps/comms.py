#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division, print_function # python 2.7 compatibility

class Slaves:
	def __init__(self):
		self.telemetry = ["speedometer", "battery"]
		self.data = { "speedometer": 0, "battery": 100 }

	def get(self, requestedTelem):
		'''
		returns the value of the requested telemetry
		'''
		if (requestedTelem in self.telemetry):
			return self.data[requestedTelem]
