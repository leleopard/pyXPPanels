import socket

host = "127.0.0.1"
port = 49000

# socket to send data
sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = 'CMND0'
msg += 'sim/radios/stby_com1_coarse_up'

print msg

sendSock.sendto(msg, (host, port))