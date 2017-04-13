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
		self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
			
			try:
				(client_socket, client_adress) = self.listener.accept()
				
			except socket.error:
				sys.exit("Could not accept any more connections")
				
			self.client_sockets.append(client_socket)
				
			print "Starting client thread for {0}".format(client_address)
			client_thread = ClientListener(self, client_socket, client_address)
			client_thread.start()
			
			time.sleep(0.1)
			
	def echo(self, data):
		#Send a message to each socket in self.client_socket
		
		print "echoing: {0}".format(data)
		for socket in self.client_sockets:
			#Try and echo to all clients
			try:
				socket.sendall(data)
			except socket.error:
				print "Unable to send message"
				
				
	def remove_socket(self, socket):
		#Remove the specified socket from the client_sockets list
		self.client_sockets.remove(socket)
	
	def signal_handler(self, signal, frame):
		#Run when Ctrl+C is pressed
		print "Tidying up"
		#Stop listening for new connections
		self.listener.close()
		#Let each client know we are quitting
		self.echo("QUIT")
		
class ClientListener(threading.Thread):
	def __init__(self, server, socket, address):
		#Initialise the Thread base class
		super(ClientListener, self).__init__()
		
		#Store the values that have been passed to the constructor
		self.server = server
		self.address = address 
		self.socket = socket
		self.listening = True
		self.username = "No Username"
		
	def handle_msg(self, data):
		#Print and then process the message we've just recieved
		print "{0} sent: {1}".format(self.address, data)
		#Use regular expressions to test for a message like "USERNAME jarrad"
		username_result = re.search('^USERNAME (.*)$', data)
		if username_result:
			self.username = username_result.group(1)
			self.server.echo("{0} has joined.\n".format(self.username))
		
		elif data == "QUIT":
			#If the client has sent quit then close this thread
			self.quit()
		
		elif data == "":
			#The socket at the other end is probably closed
			self.quit()
			
		else:
			#It's a normal message so echo it to everyone
			self.server.echo(data) #Maybe change to self.Server.echo(data)
			
			
if __name__ == "__main__":
	#Start a server on port 59091
	server = Server(59091)
	server.run()

