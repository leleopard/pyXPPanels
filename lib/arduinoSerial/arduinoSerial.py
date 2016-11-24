import threading
import logging
import time
import serial
from struct import *

##--------------------------------------------------------------------------------------------------------------------
# class ArduinoSerial
#
# Allows to send and receive data to an arduino over the serial port 
#
# The class is inherited from the Threading module, and will run as its own thread when started
# Simple Example:
#
# @code 
# import ArduinoSerial
# ArduinoSerial = ArduinoSerial.ArduinoSerial(("COM3",115200)
# ArduinoSerial.start()
# @endcode
#
# you should call the quit() method when exiting your main python programme
#
#--------------------------------------------------------------------------------------------------------------------

class ArduinoSerial(threading.Thread):

	##--------------------------------------------------------------------------------------------------------------------
	# constructor 
	# @param PORT: port the arduino is connected to
	# @param BAUD: BAUD setting for the serial port - needs to be the same as how the arduino is configured
	#
	#--------------------------------------------------------------------------------------------------------------------
	def __init__(self, PORT, BAUD, XPUDPServer = None):
		threading.Thread.__init__(self)
		self.running = True
		logging.info("Initialising serial Arduino connection on port: %s", PORT, "BAUD: ", BAUD)
		
		self.serialConnection = serial.Serial(PORT, BAUD)
		self.XPUDPServer = XPUDPServer
		
		# reset the arduino
		#self.serialConnection.setDTR(level=False)  
		time.sleep(0.5)  
		# ensure there is no stale data in the buffer
		self.serialConnection.flushInput()  
		#self.serialConnection.setDTR()  

		time.sleep(0.5)

		
	##--------------------------------------------------------------------------------------------------------------------
	# run. Do not call - use the start() method to start the thread, which will call run() 
	# infinite loop sending / receiving data to the arduino 
	#
	#--------------------------------------------------------------------------------------------------------------------
	def run(self):
		buffer =""
		
		while self.running:
			
			#print ("xp server atttempt to receive data...")
			bytesToRead = self.serialConnection.in_waiting
			if (bytesToRead>0):
				data = self.serialConnection.read(bytesToRead)		
				#print("Arduino data: ", data, "data length", len(data))
				buffer += data
				print(buffer)
				
				if data[len(data)-1] == '\x00':
					#print(" I contain a NULL terminator")
					commands = buffer.split('\0')
					for elem in commands:
						if len(elem) > 6:
							pass #self.processArduinoCmd(elem+'\0')  # we should now have a complete command from arduino to process
					buffer = ""	# we can now empty the buffer
				
				#print("")
					
			time.sleep(0.001)	
			
	## 
	def processArduinoCmd(self, buffer):
		if buffer [0:4] == 'CMND':
			command = buffer[5:len(buffer)-1]
			print("i see a command", command)
			
			self.XPUDPServer.sendXPCmd(command)
		
		if buffer [0:4] == 'DREF':
			dataref = buffer[5:len(buffer)-1]
						
			print("i see a dataref", dataref)
			
			self.XPUDPServer.sendXPDref(dataref)
	
	##--------------------------------------------------------------------------------------------------------------------
	# quit. Call to stop the thread 
	#
	#--------------------------------------------------------------------------------------------------------------------
	def quit(self):
		self.running = False
		self.serialConnection.close()
		logging.info("Arduino Connection stopped...")
		
