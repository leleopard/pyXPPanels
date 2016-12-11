import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind(("127.0.0.1",50000))

# Receive no more than 1024 bytes
while 1:
	msg = bytes()
	try:
		msg = sock.recv(1024)    
		print (msg.decode('ascii'))
	except:
		pass
	

sock.close()

