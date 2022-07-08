# This is the Server program
#
# Sequence of steps:
#	1. create a "welcome" socket for listening to new connections 
#	2. bind the socket to a host and port
#	3. start listening on this socket for new connections
#	4. accept an incoming connection from the client
#   5. send and receive data over the "connection" socket


import socket
from datetime import datetime
from _thread import start_new_thread

#  create a socket for listening to new connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use SOCK_STREAM for TCP
# use SOCK_DGRAM for UDP

# bind it to a host and a port
host = 'localhost'
port = 43389  # arbitrarily chosen non-privileged port number
s.bind((host,port))
print("Server started...waiting for a connection from the client")

# start listening for TCP connections made to this socket
# the argument "10" is the max number of queued up clients allowed
s.listen(10)

clients = []
client_names = []

terminate = False
def clientthread(connection_socket, addr):
	name = connection_socket.recv(1024)
	name = name.decode()
	client_names.append(name)

	print(">" + name + " has joined!")

	time = str(datetime.time(datetime.now()))[:5]
	s_msg = "Server: time={} {} has joined. Member Count={}".format(time, name, len(clients))
	broadcast(s_msg, "--")

	while True:
		message = connection_socket.recv(1024)
		
		if(message.decode('utf-8').split('\n')[0]=='quit'):
			print(name, " requested to leave the session!")
			remove(connection_socket)
			break  
		else:
			msg = message.decode('utf-8').split('\n')[0]
			print (">" + name + ": " + msg)  

			#To send the message to all other
			message_to_send = "{}: ".format(name) + msg  
			broadcast(message_to_send, connection_socket)  



def broadcast(message, connection_socket):  
	for client in clients:  
		if client!=connection_socket:  
			client.send(message.encode('utf-8'))

def remove(connection_socket):  
	if connection_socket in clients:
		j = 0
		for i in range(1, len(clients)):
			if clients[i]==connection_socket :
				j = i
				break
		clients.remove(connection_socket)

		time = str(datetime.time(datetime.now()))[:6]
		s_msg = "Server: time={} {} has left. Member Count={}".format(time, client_names[j], len(clients))
		print(client_names[j], " has been disconnected!")
		broadcast(s_msg, "--")
		client_names.remove(client_names[j])

		if(len(clients)==0):
			print("All have been disconnected. I need a break too!")
			print("Type: Ctrl+C")


while True:

	# accept a connection
	connection_socket, addr = s.accept()  

	clients.append(connection_socket)  

	# creates and individual thread for every user  
	# that connects  
	start_new_thread(clientthread, (connection_socket, addr))      

connection_socket.close()  
s.close()  
