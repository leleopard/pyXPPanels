import threading
import socket
from struct import *
import logging

#--------------------------------------------------------------------------------------------------------------------
# class ExtPlaneClient
#
# server class that connects to the ExtPlane plugin. Listens to registered datarefs and parses them into an internal list.
# The IP address and UDP port of the ExtPlane plugin are passed in the constructor
#
# The class is inherited from the Threading module, and will run as its own thread when started
# Simple Example:
#
#
#--------------------------------------------------------------------------------------------------------------------

class ExtPlaneClient(threading.Thread):

	#--------------------------------------------------------------------------------------------------------------------
	# constructor 
	# @arg extPlaneAddress: tuple of IP address, port of the ExtPlane plugin
	#--------------------------------------------------------------------------------------------------------------------
	def __init__(self, extPlaneAddress):
		threading.Thread.__init__(self)
		self.running = True
		self.connected = False
		self.rcvBufferSize = 4096
		self.dataList ={}
		
		self.XTPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.XTPsocket.settimeout(3)

		try:
			self.XTPsocket.connect(extPlaneAddress)
			self.connected = True
		except:
			logging.error('ExtPlane Client: unable to connect to address %s', extPlaneAddress)
			self.connected = False
			
		if self.connected == True:
			logging.info('ExtPlane Client connected to remote host %s', extPlaneAddress)
			data = self.XTPsocket.recv(self.rcvBufferSize)
			print data
			MSG = 'extplane-set update_interval 0.03'+'\n\r'
			self.XTPsocket.sendall(MSG) 
	#--------------------------------------------------------------------------------------------------------------------
	# getData. returns data for the key, index provided. 
	# @arg key: The XPlane dataref (string)
	# @arg index: the index in the dataref array. if the dataref is not an array and has only one value use 0 or omit
	#--------------------------------------------------------------------------------------------------------------------
	def getData(self,key,index=0):
		if key in self.dataList:
			return self.dataList[key][index]
		else:
			return 0
		
	#--------------------------------------------------------------------------------------------------------------------
	# subscribeDataRef. subscribe to an X Plane dataref
	# @arg DataRef: string - xplane dataref to subscribe to
	#--------------------------------------------------------------------------------------------------------------------
	def subscribeDataRef(self,DataRef):
		if self.connected == True:
			MSG = 'sub '+DataRef+'\n\r'
			logging.info('ExtPlaneClient subscribing to dataref: %s',DataRef)
			self.XTPsocket.sendall(MSG)
		else :
			logging.error('ExtPlaneClient not connected, can not subscribe to dataref')
			
	#--------------------------------------------------------------------------------------------------------------------
	# run. infinite loop listening for the data from the ExtPlane plugin. When data is received, it is parsed and stored/updated in the 
	# dataList attribute 
	#
	#--------------------------------------------------------------------------------------------------------------------
	def run(self):
		while self.running:
			if self.connected == True:
				try:
					data = self.XTPsocket.recv(self.rcvBufferSize)
					#logging.debug("ExtPlane client: data received: %s",data)
					self.parseExtPlaneDataPacket(data)
					
				except socket.error, msg: 
					logging.error("ExtPlane Client: unable to receive data")    

	#--------------------------------------------------------------------------------------------------------------------
	# quit. Call to stop the thread 
	#
	#--------------------------------------------------------------------------------------------------------------------
	def quit(self):
		self.running = False
		self.connected = False
		self.XTPsocket.close()
		
	#--------------------------------------------------------------------------------------------------------------------
	# parseExtPlaneDataPacket. Internal method that parses the packet received from the ExtPlane plugin
	# 
	# @arg packet: The TCP packet to parse
	#--------------------------------------------------------------------------------------------------------------------
	def parseExtPlaneDataPacket(self, packet):
		splits = packet.split()
		if len(splits)%3 != 0 :
			print "Invalid ExtPlane DATA packet"
			return
		else :
			nrGroups =  len(splits)/3
			#print "Number of groups: ", nrGroups
			
			for i in range(0,nrGroups) :
				dataref = splits[i*3+1]
				value = []
				if splits[i*3] == 'ui':
					value = [int(splits[i*3+2])]
				if splits[i*3] == 'uf' or splits[i*3] == 'ud':
					value = [float(splits[i*3+2])]
				if splits[i*3] == 'ub':
					value = [splits[i*3+2]]
				if splits[i*3] == 'ufa' or splits[i*3] == 'uia' :
					datastring = splits[i*3+2].strip('[]')
					val_array = datastring.split(',')
					for val in val_array:
						if splits[i*3] == 'ufa':
							value.append(float(val))
						if splits[i*3] == 'uia':
							value.append(int(val))
						
				self.dataList[dataref] = value
				
