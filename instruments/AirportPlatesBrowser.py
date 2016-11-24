import os
import glob
import logging
import decimal
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
D = decimal.Decimal

from lib.glfw import glfw
from lib.graphics import fonts
from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3

class AirportPlatesBrowser(graphicsGL3.Window):
	textXdispl = 0
	textYdispl = 0
	airportPlateZoom = 1.0
	previousMousePosPlateText = (0,0)
	
	def __init__(self,position, size, pyGaugesPanel, batchImageRenderer):
		
		self.titleBarFont = OpenGL3lib.GL_Font("data/fonts/Envy-Code-R.ttf", fonts.FONT_SIZE_MED, fonts.TXT_COLOR_WHITE, True, 0)
		self.batchImageRenderer = batchImageRenderer
		graphicsGL3.Window.__init__(self,position, size, pyGaugesPanel, self.titleBarFont, batchImageRenderer, 1, "Airport Plate Browser Window")
		#self.clipping = True
		self.setTitleText("Airport Plates Browser")
		
		pyGaugesPanel.registerKeyCallback(self.keyCallback)
		pyGaugesPanel.registerScrollCallback(self.scrollCallback)
		pyGaugesPanel.registerMouseCursorPosCallback(self.mouseMovePlateTextureCallback)
		self.createAirportList()
		
		self.airportPlanePanel = graphicsGL3.Container( (0,0), (self.width-4,self.height-self.titleBarHeight-4), False )
		self.airportPlanePanel.setClipping(True)
		self.addItem(self.airportPlanePanel, (2,2),False)
		
		self.plate_texture =	OpenGL3lib.GL_Texture("data/AirportPlates/FR-LFHM-MEGEVE-2.png", True)
		
		self.airportPlateImage = graphicsGL3.ImagePanel(self.plate_texture, batchImageRenderer, 1, [0,0], [self.width-4,self.height-2],	[0	,0	])
		self.airportPlateImage.resize([self.width-4,self.airportPlanePanel.height-2])
		
		self.airportPlanePanel.addItem(self.airportPlateImage, (float(self.width-4)/2,float(self.airportPlanePanel.height-2)/2),False)
		
		self.inputText = graphicsGL3.InputTextField([0,0],[self.width,20], pyGaugesPanel, "data/fonts/Envy-Code-R.ttf", fonts.FONT_SIZE_LARGE, fonts.TXT_COLOR_WHITE)
		self.inputText.addHintList(self.airportNames)
		self.addItem(self.inputText, (0,0), False)
		
		self.loadAirportPage(self.airportNames[0],0)
		self.textRotation = 0
		
	
	def createAirportList(self):
		self.airportNames =[]
		self.airportFilesDict = {}
		# so basically we want a dictionary with the country code + airport codes as key
		for imageFile in sorted(os.listdir("data/AirportPlates")):
			chunks = imageFile.split('-')
			if len(chunks)>3:
				if chunks[0][0] != ".":
					airportCode = chunks[0]+"-"+chunks[1]+"-"+chunks[2]
					logging.debug("imageFile, chunks: %s %s", imageFile, chunks)
					if not self.airportFilesDict.get(airportCode):
						self.airportFilesDict [airportCode]=[]
					
		logging.debug("airportFilesDict : %s", self.airportFilesDict )
		
		# now we have a dictionary of airports with an empty list for each airport, lets populate the lists
		for airport in self.airportFilesDict:
			self.airportNames.append(airport)
			airportTextFiles = sorted(glob.glob("data/AirportPlates/"+airport+"*"))
			self.airportFilesDict[airport] = airportTextFiles
			logging.debug("airport, airportTextFiles: %s %s", airport, airportTextFiles)
		logging.debug("airport texture files dict: %s", self.airportFilesDict)
		
	def loadAirportPage(self,airportName, pageNr):
		if pageNr < 0:
			pageNr = 0
		elif pageNr > len(self.airportFilesDict[airportName])-1:
			pageNr = len(self.airportFilesDict[airportName])-1
		self.plate_texture.loadImageToTexture(self.airportFilesDict[airportName][pageNr], True)
		self.currentAirport = airportName
		self.currentAirportPageNr = pageNr
		
	
	def keyCallback(self,key, scancode, action, mods):
		if action == glfw.GLFW_PRESS:
			if key == glfw.GLFW_KEY_F2:
				print("F2 pressed")				
				self.setVisible ( not self.visible)
			if key == glfw.GLFW_KEY_PAGE_UP and self.leftClicked == True:
				self.currentAirportPageNr -=1
				self.loadAirportPage(self.currentAirport,self.currentAirportPageNr)
			if key == glfw.GLFW_KEY_PAGE_DOWN and self.leftClicked == True:
				self.currentAirportPageNr +=1
				self.loadAirportPage(self.currentAirport,self.currentAirportPageNr)
			if (key == glfw.GLFW_KEY_ENTER or key == glfw.GLFW_KEY_KP_ENTER) and self.leftClicked == True:
				if self.inputText.entryAccepted == True:
					self.currentAirportPageNr = 0
					self.currentAirport = self.inputText.text
					self.loadAirportPage(self.currentAirport,self.currentAirportPageNr)
			if key == glfw.GLFW_KEY_HOME and self.leftClicked == True:
				logging.debug( "rotate")
				self.textRotation +=5
				self.airportPlateImage.rotateTexture(self.textRotation)
			if key == glfw.GLFW_KEY_END and self.leftClicked == True:
				logging.debug( "-rotate")
				self.textRotation -=5
				self.airportPlateImage.rotateTexture(self.textRotation)
	
	def scrollCallback(self, xoffset, yoffset):
		if (self.leftClicked == True) :
			self.airportPlateZoom -= float(yoffset)/10
			self.airportPlateImage.zoomTexture(self.airportPlateZoom) 
			logging.debug("mouse down, zoom %s", self.airportPlateZoom)
		
	def mouseMovePlateTextureCallback(self, xpos, ypos):
		mousePos = OpenGL3lib.returnOpenGLcoord((xpos,ypos))
		
		if (self.leftClicked == True) and (self.previousMouseLeftBtnState == "DOWN") and (self.MOUSE_OVER_TITLEBAR == False): 
			self.textXdispl -= mousePos[0] - self.previousMousePosPlateText[0]
			self.textYdispl -= mousePos[1] - self.previousMousePosPlateText[1]
			
			self.airportPlateImage.translateTexture(self.textXdispl,self.textYdispl)
		self.previousMousePosPlateText = mousePos
		#logging.debug("leftclicked:%s, dragged: %s, mouse move: %s, %s", self.leftClicked, self.dragged, self.textXdispl, self.textYdispl)
		
		
	def draw(self):
		super(AirportPlatesBrowser,self).draw()
		

