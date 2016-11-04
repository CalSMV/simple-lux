#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division, print_function # python2.7 compatibility
# import exceptions as ex # in python3, we don't need to explicit import exceptions
import threading as th
import time
import json
from tornado import web, websocket, ioloop

# TODO: need a name for this system

QUERY_DELAY = 0.5

clients = []

class Console():
	def __init__(self, telemetry, getTelemFunc, port=1234, verbose=True):
		self.port = port
		self.verbose = verbose
		self.initialized = False
		self.telemNames = telemetry
		self.telemData = {}
		self.getTelem = getTelemFunc
		if (self.verbose): print("main :: init")

	def startServer(self):
		'''
		starts the tornado webserver
		'''
		try:
			self.server = Server(self)
			ioloop.IOLoop.instance().start()
		except KeyboardInterrupt:
			print("main :: server stopped")

	def initConfig(self):
		'''
		initial configuration for when the websocket is first opened
		'''
		if (self.verbose): print("main :: config")
		# begin default configuration
		toSend = { "spawnHomeScreen": [], "spawnMusicScreen": [], "spawnCameraScreen": [] }
		self.sendToClients(toSend)

	def update(self):
		'''
		function that regularly pushes data client
		'''
		if ((not self.initialized) and (not len(clients) == 0)):
			self.initConfig()
			self.initialized = True
		toSend = self.getTelemetryFromSlaves()
		self.sendToClients(toSend)

	def getTelemetryFromSlaves(self):
		for telemName in self.telemNames:
			self.telemData[telemName] = self.getTelem(telemName)
		data = { "drawTelemetry": [self.telemData] }
		return data

	def sendToClients(self, data):
		'''
		packages data as json objects and sends to client via websockets
		'''
		data = json.dumps(data)
		for c in clients:
			c.write_message(data)

class IndexHandler(web.RequestHandler):
	def get(self):
		print("main :: rendering index.html")
		self.render("../www/index.html")

class SocketHandler(websocket.WebSocketHandler):
	def __init__(self, *args, **kws):
		super(SocketHandler, self).__init__(*args, **kws)

	def open(self):
		'''
		opens the websockets connection between server and client
		adds client to list of clients
		'''
		print("main :: WebSocket opened") # TODO: how to pass console.verbose to this?
		if (self not in clients):
			print("main :: client added")
			clients.append(self)

	def on_close(self):
		'''
		handles the closing of the websocket
		removes client from list
		sets init to false
		'''
		print("main :: WebSocket closed") # TODO: how to pass console.verbose to this?
		if (self in clients):
			print("main :: client removed")
			clients.remove(self)
		self.application.dataPusher.console.initialized = False

	def on_message(self):
		'''
		handles inputs from the client
		'''
		print("main :: server received message") # TODO: how to pass console.verbose to this?
		try:
			msg = json.loads(message)
		except Exception as e:
			print("main :: exception in 'onMessage'")

class DataPusher():
	def __init__(self, console):
		'''
		class responsible for regularly pushing data to the client
		'''
		self.console = console
		self.secsPerReading = 0.0001
		self.running = False
		self.thread = None
		if (self.console.verbose): print("main :: init datapusher")
		self.start()

	def start(self):
		'''
		starts the datapusher
		'''
		self.running = True
		if (self.thread == None):
			self.thread = th.Thread(target=self.work)
			self.thread.setDaemon(True)
			self.thread.start()

	def work(self):
		'''
		function that constantly pushes data to clients
		'''
		if (self.console.verbose): print("main :: starting pushes")
		lastQuery = time.time()
		while (self.running):
			try:
				elapsed = time.time() - lastQuery
				if (elapsed > self.secsPerReading):
					if (len(clients) > 0):
						# if (self.console.verbose): print("main :: push")
						self.console.update()
					lastQuery = time.time()
				else:
					time.sleep(0.001)
			except Exception as e:
				print("main :: error during data push")
				print(e)

class Server():
	def __init__(self, console):
		'''
		tornado webserver
		'''
		if (console.verbose): print("main :: start http & websocket server on", console.port)
		self.webApp = web.Application([
			(r'/', IndexHandler),
			(r'/ws', SocketHandler),
			(r'/(.*)', web.StaticFileHandler, {'path': '../www/'}),
			],)
		self.webApp.listen(console.port)
		dataPusher = DataPusher(console)
		self.webApp.dataPusher = dataPusher

		