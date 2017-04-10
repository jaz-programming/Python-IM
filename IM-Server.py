#!/usr/bin/python2.7

import threading
import socket
import re
import signal
import sys
import time

class Server():
	def __init__(self, port):
		#Create a socket and bind it to a port
		self.listener = socket.socket(socket.AF-INET, socket.SOCK_STREAM)
		self.listener.bind(('', port))
		self.listener.listen(1)
		print "Listening on port {0}".format(port)
		
		#Used to store all of the client sockets we have, for echoing to them
		self.client_sockets = []
		
		#Run the function self.signal_handler when Ctrl+C is pressed
		signal.signal(signal.SIGTERM, self.signal_handler)
	
	def run(self):
		while True:
			
			#Listen for clients, and create a ClientThread for each new client
			print "Listening for more clients"  
