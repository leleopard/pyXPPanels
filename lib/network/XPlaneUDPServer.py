import sys, threading
import socket
import logging
import time
from struct import *

## @brief Server Thread class that listens to UDP data packets from X Plane, and parses them into an internal list.
# @brief The class can also be configured to act as a relay to forward XPLane UDP packets to other devices on the network, or act as a concentrator and pass UDP packets from other network devices to XPlane 
# The IP address and UDP port the class listens on are passed in the constructor
# This same IP and port have to be configured in the 'IP for Data Output' section of the 'Data' tab in 
# XPlanes 'Net Connections' settings
#
# The class is inherited from the Threading module, and will run as its own thread when started
# Simple Example:
#
# @code
# import XPlaneUDPServer
# XPlaneDataDispatcher = XPlaneUDPServer.XPlaneUDPServer(("127.0.0.1",49005))	#create an instance of the class, listening for data on IP 127.0.0.1 and port 49005. configure the same in XPlane
# XPlaneDataDispatcher.start()
#
# value = XPlaneDataDispatcher.dataList[17][3] 	# read the value sent by XPlane for datagroup 17, position 4 (mag heading)
# @endcode
#

PYTHON_VERSION = sys.version_info[0] 

class XPlaneUDPServer(threading.Thread):

	## constructor 
	# @param Address: tuple of IP address, UDP port we are listening on
	#
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = True
		
		# socket listening to XPlane Data
		self.XplaneRCVsock = None
		self.forwardXPDataAddresses = [] # default the forward addresses to empty list
		self.XPCmd_Callback_Functions = [] # list of callback functions to be called when the class is asked to send a command to XPlane
		
		self.RDRCT_TRAFFIC = False # by default we do not redirect incoming traffic to Xplane
		self.DataRCVsock = False 
		self.XPAddress = None
						
		# socket to send data
		self.sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		self.RREF_sockets = [] # list to store RREF sockets, one for each dataref subscribed. Not very elegant, but XPlane does not seem to be able to deal with multiple RREF requests from the same socket
		
		self.dataList =[]
		self.cmddata = None
		for i in range(0,1024) :
			self.dataList.append([0,0,0,0,0,0,0,0]) # initialise the dataList with 0 values

	## Initialise the UDP sockets to communicate with XPlane
	# @param Address: tuple of IP address, UDP port we are listening on
	# @param XPAddress: tuple of IP address, UDP port for XPlane
	#
	def initialiseUDP(self, Address, XPAddress = None):
		logging.info("Initialising XPlaneUDPServer on address: %s", Address)
		# socket listening to XPlane Data
		self.XplaneRCVsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.XplaneRCVsock.setblocking(0)
		self.XplaneRCVsock.bind(Address) # bind this socket to listen to traffic from XPlane on the address passed to the constructor
		self.XPAddress = XPAddress
		
		
	## Enables the forwarding of data received from XPLane to a list of IP addresses
	# @param forwardAddresses: a list of addresses to forward to, in the format [(IP1,port1),(IP2,port2), ... ]
	#
	def enableForwardXPpackets(self,forwardAddresses):
		self.forwardXPDataAddresses = forwardAddresses

	## Returns data last received from XPlane for the key, index provided. 
	# @param key: The XPlane data group ID
	# @param index: the index in the data group
	#
	def getData(self,key,index):
		if key >= 0 and key <1024:
			return self.dataList[key][index]
		else:
			return 0
	
	## Prints data to the console for the key, index provided. 
	# @param key: The XPlane data group ID
	# 
	def printData(self,key):
		if key >= 0 and key <1024:
			print ("Data Group: ", key, " [",self.dataList[key][0],",",self.dataList[key][1],",",self.dataList[key][2],",",self.dataList[key][3],",",self.dataList[key][4],",",self.dataList[key][5],",",self.dataList[key][6],",",self.dataList[key][7],"]")
		else:
			logging.error ( "Invalid key")
			
	## send command to XPlane
	# @param string for the command to be sent to XPlane - refer to the XPlane doc for a list of available commands
	#
	def sendXPCmd(self, command):
		if self.XPAddress is not None:
			msg = 'CMND0'
			msg += command

			self.sendSock.sendto(msg.encode("latin_1"), self.XPAddress)
			
			for callback in self.XPCmd_Callback_Functions:
				callback(command)
		else:
			logging.error("XPlane IP address undefined")
			
	
	## send Dataref to XPlane
	# @param string for the dataref to be sent to XPlane - refer to the XPlane doc for a list of available datarefs
	# format of dataref string should be 4 bytes (chars) for the value to set, followed by the dataref path, then by a null character. The function will automatically pad white spaces to the length XPlane expects
	#
	def sendXPDref(self, dataref):
		if self.XPAddress is not None:
			nr_trailing_spaces = 504-len(dataref)
			
			msg = 'DREF0'+dataref
			msg += ' '*nr_trailing_spaces
			if len(msg) == 509:
				self.sendSock.sendto(msg.encode("latin_1"), self.XPAddress)
		else:
			logging.error("XPlane IP address undefined")
		
	## registers a callback function to be called if the class receives a sendXPCmd() call
	# @param callback - the callback function, it will be given the command string as parameter so your callback must handle the command string
	#
	def registerXPCmdCallback(self, callback):
		self.XPCmd_Callback_Functions.append(callback)
		
	
	## Request Dataref from XPlane
	# @param string for the dataref to be requested from XPlane - refer to the XPlane doc for a list of available datarefs
	#
	def requestXPDref(self, index, dataref):
		if self.XPAddress is not None:
			RREF_Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.RREF_sockets.append(RREF_Sock)
			
			dataref+= '\0'
			nr_trailing_spaces = 400-len(dataref)
			
			msg = "RREF"+'\0'
			packedindex = pack('<i', index)
			packedfrequency = pack('<i', 30)
			msg += packedfrequency.decode(encoding = 'latin_1')
			msg += packedindex.decode(encoding = 'latin_1')
			msg += dataref
			msg += ' '*nr_trailing_spaces
			
			logging.debug("Requesting DataRef, RREF msg: %s", msg)
			
			RREF_Sock.sendto(msg.encode('latin_1'), self.XPAddress)
			RREF_Sock.setblocking(0)
		else:
			logging.error("XPlane IP address undefined")
	
	## Enables the redirection of traffic received by the class to XPlane
	# @param myAddress: The address the class is listening for traffic on. Format: (IP,port)
	# @param XPAddress: The XP address we will be forwarding the packets to. Format: (IP, port)
	#
	def enableRedirectUDPtoXP(self, myAddress, XPAddress):
		self.RDRCT_TRAFFIC = True
		self.XPAddress = XPAddress
		self.DataRCVsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.DataRCVsock.setblocking(0)
		self.DataRCVsock.bind(myAddress)
	
	## Internal thread loop - Do not call - use the start() method to start the thread, which will call run() 
	# infinite loop listening for data from XPlane. When data is received, it is parsed and stored/updated in the 
	# dataList attribute 
	# If the instance has been configured to forward XPlane packets, it will loop through the forward addresses to do so
	# If the instance has been configured to re direct traffic to XPlane, it will forward any packets received to XP
	#
	def run(self):
		
		while self.running:
						
			try:
				#print ("xp server atttempt to receive data...")
				data, addr = self.XplaneRCVsock.recvfrom(8192) # receive data from XPlane
				
				fwddata = data
				#print(data)
				#print(data[0:4])
				if data[0:4].decode('ascii') == "DATA": 
					#print("Received XP data")					
					self.parseXplaneDataPacket(data)
					
				if len(self.forwardXPDataAddresses) > 0: # loop through forward addresses and send fwd_data packet
					for i in range(0,len(self.forwardXPDataAddresses)) :
						if self.forwardXPDataAddresses[i][1] == True:
							self.sendSock.sendto(fwddata,self.forwardXPDataAddresses[i][0])
						else :
							if data[0:5].decode('ascii') != "DATA|":
								self.sendSock.sendto(fwddata,self.forwardXPDataAddresses[i][0])
						
			except socket.error as msg: pass
				#print ("UDP Xplane receive error code ", str(msg[0]), " Message: ", str(msg[1]) )   
			
			try:
				for RREFSocket in self.RREF_sockets:
					rrefdata, rrefaddr = RREFSocket.recvfrom(8192)
					#logging.debug("RREF data:: "+ str(rrefdata))
					
					if rrefdata[0:4].decode('ascii') == 'RREF':
						index = unpack('<i', rrefdata[5:9])[0]
						value = unpack('<f', rrefdata[9:13])[0]
			
						#logging.debug("RREF index "+str(index) + ", value: "+ str(value))
						self.dataList[index][0] = value
						
			except : 
				pass
				#logging.error("Error receiving RREF data")
			
			if self.RDRCT_TRAFFIC == True:
				try:
					ardData,ardAddr = self.DataRCVsock.recvfrom(8192) # receive data from another source
					#print "Rcvd Data from ", ardAddr, "data: ", ardData[0:6]
					self.sendSock.sendto(ardData, self.XPAddress) # forward it to XPlane
				except socket.error as msg: pass
					#print "UDP ARD receive error code ", str(msg[0]), " Message: ", str(msg[1]) 
			time.sleep(0.01)
			
	## Call to stop the thread and close the UDP sockets
	#
	def quit(self):
		self.running = False
		self.XplaneRCVsock.close()
		if self.DataRCVsock != False:
			self.DataRCVsock.close()
		logging.info("UDP Server stopped...")
		
	## Internal method that parses a 'DATA' type packet received from XPlane
	# it splits the packet into each data group, and calls the parseXPlaneDataGroup method to parse the dataGroup
	# @param packet: The UDP packet to parse
	#
	def parseXplaneDataPacket(self, packet):
		indexType = "XPUDP"
		if packet[0:5].decode('ascii') == "DATA|" :
			indexType ="STUDP"
			
		dataGroups = packet[5:len(packet)]
		#print (len(dataGroups))
		if len(dataGroups)%36 != 0 :
			print ("Invalid XPlane DATA packet")
			#print "packet: ", dataGroups
			return
		else :
			nrGroups =  int(len(dataGroups)/36)
			#print ("Number of groups: ", nrGroups)	
			
			for i in range(0,nrGroups) :
				self.parseXPlaneDataGroup(dataGroups[i*36:i*36+36], indexType)

	## Internal method that parses a Data group and stores it into the dataLIst attribute
	# @param dataGroup: The data group to parse
	#
	def parseXPlaneDataGroup(self,dataGroup,indexType) :
		if indexType == "XPUDP":
			index = unpack('B',dataGroup[0:1])[0]
		if indexType == "STUDP":
			index = unpack('<i',dataGroup[0:4])[0]
		#print "UDP server - parse Group, index: ", index
		
		if (index >= 0) and (index <=1024):
			
			value1 = unpack('<f', dataGroup[4:8])[0]
			value2 = unpack('<f', dataGroup[8:12])[0]
			value3 = unpack('<f', dataGroup[12:16])[0]
			value4 = unpack('<f', dataGroup[16:20])[0]
			value5 = unpack('<f', dataGroup[20:24])[0]
			value6 = unpack('<f', dataGroup[24:28])[0]
			value7 = unpack('<f', dataGroup[28:32])[0]
			value8 = unpack('<f', dataGroup[32:36])[0]
			
			self.dataList[index] = [value1,value2,value3,value4,value5,value6,value7,value8]
		else:
			pass
			#print("Invalid data index!", index, " Data packet type: ", indexType, "Data group:", dataGroup)
			
		#logging.debug ("DATA Index: "+ str(index)+ "Value1: "+ str(value1)+ "Value2: "+ str(value2)+ "Value3: " + str(value3)+ "Value4: "+ str(value4))
	
pyXPUDPServer = XPlaneUDPServer()


