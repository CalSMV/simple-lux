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

class Main():
	def __init__(self, port=1234, verbose=True):
		self.port = port
		self.verbose = verbose
		self.initialized = False

		if self.verbose: print("main :: init")

	def start_server(self):
		'''
		starts the tornado webserver
		'''
		try:
			self.server = Server(self)
			ioloop.IOLoop.instance().start()
		except KeyboardInterrupt:
			print("main :: server stopped")

	def update(self):
		print("this is the function that the DataPusher calls to regularly push data to the client")

	def send_to_clients(self, data):
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
		print("main :: WebSocket opened") # TODO: how to pass main.verbose to this?
		if (self not in clients):
			print("main :: client added")
			clients.append(self)
	def on_close(self):
		'''
		handles the closing of the websocket
		removes client from list
		sets init to false
		'''
		print("main :: WebSocket closed") # TODO: how to pass main.verbose to this?
		if (self in clients):
			print("main :: client removed")
			clients.remove(self)
		self.application.data_pusher.main.initialized = False

	def on_message(self):
		'''
		handles inputs from the client
		'''
		print("main :: server received message") # TODO: how to pass main.verbose to this?
		try:
			msg = json.loads(message)
		except Exception as e:
			print("main :: exception in 'on_message'")

class DataPusher():
	def __init__(self, main):
		'''
		class responsible for regularly pushing data to the client
		'''
		self.main = main
		self.secs_per_reading = 0.0001
		self.running = False
		self.thread = None
		if self.main.verbose: print("main :: init datapusher")
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
		if self.main.verbose: print("main :: starting pushes")
		last_query = time.time()
		while (self.running):
			try:
				elapsed = time.time() - last_query
				if (elapsed > self.secs_per_reading):
					if (len(clients) > 0):
						if self.main.verbose: print("main :: push")
						self.main.update()
					last_query = time.time()
				else:
					time.sleep(0.0001)
			except Exception as e:
				print("main :: error during data push")
				print(e)

class Server():
	def __init__(self, main):
		'''
		tornado webserver
		'''
		if main.verbose: print("main :: start http & websocket server on", main.port)
		self.web_app = web.Application([
			(r'/', IndexHandler),
			(r'/ws', SocketHandler),
			(r'/(.*)', web.StaticFileHandler, {'path': '../www/'}),
			],)
		self.web_app.listen(main.port)
		data_pusher = DataPusher(main)
		self.web_app.data_pusher = data_pusher

		