# This is the client program

# Sequence:
#
# 1. Create a socket
# 2. Connect it to the server process. 
#	We need to know the server's hostname and port.
# 3. Send and receive data 

import socket, select, sys

# create a socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# The first argument AF_INET specifies the addressing family (IP addresses)
	# The second argument is SOCK_STREAM for TCP service
	#    and SOCK_DGRAM for UDP service


# connect to the server
host='localhost'
port=43389  # this is the server's port number, which the client needs to know
s.connect((host,port))

print("Enter your name: ")
name = input()
s.send(name.encode('utf-8'))

while True:  
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, s]
    terminate = False  
	
    """Two possible scenarios: either read or write"""
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])  
  
    for socks in read_sockets:  
        if socks == s:  
            message = socks.recv(1024)  
            print(message.decode())  
        else:  
            message = sys.stdin.readline()  
            s.send(message.encode('utf-8'))
            if(message.split('\n')[0]=='quit'):
                terminate = True
                break
    if(terminate):
        break 

# close the connection
s.close()

