import socket
from struct import *

IP = "127.0.0.1"
Port = 49008

XPlaneIP = "192.168.1.1"
XPlanePort = 49000

sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sendSock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


## Request Dataref from XPlane
	# @param string for the dataref to be requested from XPlane - refer to the XPlane doc for a list of available datarefs
	# 
def requestXPDref(index, dataref):
	dataref+= '\0'
	nr_trailing_spaces = 400-len(dataref)
	
	msg = "RREF"+'\0'
	packedindex = pack('<i', index)
	packedfrequency = pack('<i', 30)
	msg += packedfrequency
	msg += packedindex
	msg += dataref
	msg += ' '*nr_trailing_spaces
	
	print(msg)
	sendSock.sendto(msg, (XPlaneIP, XPlanePort))

def requestXPDref2(index, dataref):
	dataref+= '\0'
	nr_trailing_spaces = 400-len(dataref)
	
	msg = "RREF"+'\0'
	packedindex = pack('<i', index)
	packedfrequency = pack('<i', 30)
	msg += packedfrequency
	msg += packedindex
	msg += dataref
	msg += ' '*nr_trailing_spaces
	
	print(msg)
	sendSock2.sendto(msg, (XPlaneIP, XPlanePort))
		

XplaneRCVsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
XplaneRCVsock.setblocking(0)
XplaneRCVsock.bind((IP, Port)) 

requestXPDref(512, "sim/cockpit2/radios/actuators/com1_power[0]")
requestXPDref2(513, "sim/cockpit2/radios/actuators/nav1_power[0]")

while(1):
	try:
		#print "**********************************************"
		#print ("xp server atttempt to receive data...")
		#print "**********************************************"
		data, addr = XplaneRCVsock.recvfrom(8192) # receive data from XPlane
		rrefdata, rrefaddr = sendSock.recvfrom(8192)
		#print("[Data] :: Index", data[0:5])
		#print(data)
		print "RREF data:: ", rrefdata
		
		if rrefdata[0:4] == 'RREF':
			value1 = unpack('<i', rrefdata[5:9])[0]
			value2 = unpack('<f', rrefdata[9:13])[0]
			
			print "index ", value1, ", value: ", value2
		
		rrefdata2, rrefaddr2 = sendSock2.recvfrom(8192)
		#print("[Data] :: Index", data[0:5])
		#print(data)
		print "RREF data 2:: ", rrefdata2
		
		if rrefdata2[0:4] == 'RREF':
			value1 = unpack('<i', rrefdata2[5:9])[0]
			value2 = unpack('<f', rrefdata2[9:13])[0]
			
			print "index ", value1, ", value: ", value2
		
	except socket.error as msg: pass


