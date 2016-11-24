import sys, pygame
import os
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import collections
import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGLlib
from lib.graphics import fonts
from lib.network import XPlaneUDPServer
from lib.general import EventsManager


#--------------------------------------------------------------------------------------------------------------------
# TEXT FORMATTING PATTERNS
#--------------------------------------------------------------------------------------------------------------------
TXT_FMT_3DIG_PREC0_0PADDED = '{:03.0f}'
TXT_FMT_3DIG_PREC2 = '{:06.2f}'
TXT_FMT_3DIG_PREC3 = '{:07.3f}'

class Panel(object):
	x = 0
	y = 0
	orig_x = 0
	orig_y = 0
	width = 0
	height = 0

	testMode = False
	testValue = 0

	visible = True
	name = ""
	
	def __init__(self,position, size, name = "Panel"):
		logging.info("init Panel %s", name)
		self.x = position[0]
		self.y = position[1]
		self.orig_x = position[0]
		self.orig_y = position[1]
		
		self.width = size[0]
		self.height = size[1]
		self.name = name

	def setVisible(self,visible):
		self.visible = visible
	
	def setPosition(self,coordinates):
		self.x = coordinates[0]
		self.y = coordinates[1]
		self.orig_x = coordinates[0]
		self.orig_y = coordinates[1]
	
	def setTestValue(self, testValue):
		self.testValue = testValue
		
	def setTestMode (self, testMode):
		self.testMode = testMode
	
	def getName(self):
		return self.name
		
#--------------------------------------------------------------------------------------------------------------------
# class Container
# 
#--------------------------------------------------------------------------------------------------------------------
class Container(Panel):
	clipping = False
	
	previousMousePos = (0,0)
	
	previousMouseLeftBtnState = ""
	leftClicked = False
	
	previousMouseRightBtnState = ""
	rightClicked = False
	
	dragged = False
	mousedisplacement_x = 0
	mousedisplacement_y = 0
	
	border = None
	selectedBorder = None
	
	def __init__(self,position, size, name = "Container"):
		logging.info("init Container %s, position: %s, size: %s", name, position, size)
		Panel.__init__(self,position, size, name )
		self.itemList = []
		self.setSelectedBorder(1, OpenGLlib.COLOR_GREEN)

	def addItem(self,item,relativePosition=[0,0], resize = True):
		
		if resize == True:
			item.resize([self.width,self.height])
		if relativePosition == "CENTER":
			item_width = float(item.width)
			item_height = float(item.height)
			
			posx = self.x + float(self.width/2) - float(item_width/2)
			posy = self.y + float(self.height/2) - float(item_height/2)
			
			pos = [posx,posy]
		else: 
			pos = [self.x+relativePosition[0],self.y+relativePosition[1]]

			logging.info("Container: %s, adding item: %s at position: %s", self.name,item.getName(),pos)
		
		item.setPosition(pos)
		self.itemList.append(item)
	
	def resize(self,size):
		logging.info("Container: method resize not implemented yet")
	
	def setBorder(self,linewidth,color):
		self.border = OpenGLlib.GL_rectangle(self.width,self.height,linewidth,color)
	
	def setSelectedBorder(self,linewidth,color):
		self.selectedBorder = OpenGLlib.GL_rectangle(self.width,self.height,linewidth,color)
	
	def setPosition(self,coordinates):
		x_move = coordinates[0]-self.x
		y_move = coordinates[1]-self.y
		
		self.x += x_move
		self.y += y_move
		
		for image in self.itemList:
			image_newpos = (image.x+x_move,image.y+y_move)
			image.setPosition(image_newpos)
	
	def moveBy(self,x_move,y_move):
		
		self.x += x_move
		self.y += y_move
		
		for image in self.itemList:
			image_newpos = (image.x+x_move,image.y+y_move)
			image.setPosition(image_newpos)
	
	def draw(self):
		logging.debug("drawing Container: %s, width: %s, height: %s", self.name, self.width, self.height)
		if self.visible == True:
			if self.clipping == True:
				#glMatrixMode(GL_MODELVIEW)
				#glLoadIdentity()
				logging.debug("glScissor(self.x: %s, self.y: %s, self.width: %s, self.height: %s)",self.x, self.y, self.width, self.height)
				glScissor(self.x, self.y, self.width, self.height+1)
				glEnable(GL_SCISSOR_TEST)
			
			for item in self.itemList:
				logging.debug("drawing Container: %s, item: %s", self.name,item.getName())
				item.draw()
			if self.leftClicked == True:
				self.selectedBorder.draw(self.x,self.y)
			elif self.border != None:
				self.border.draw(self.x,self.y)
			
			if self.clipping == True:
				logging.debug("end glScissor")
				glDisable(GL_SCISSOR_TEST)
	
	def setClipping(self,clipping):
		self.clipping = clipping

	def setTestMode (self, testMode):
		self.testMode = testMode
		for item in self.itemList:
			item.setTestMode(testMode)
			
	def setTestValue(self, testValue):
		self.testValue = testValue
		for item in self.itemList:
			item.setTestValue(testValue)

	def isMouseOverMe(self,mouseEvent):
		mousePos = OpenGLlib.returnOpenGLcoord(mouseEvent.pos)
		
		if (mousePos[0] >= self.x) and (mousePos[0] <= (self.x+self.width)):
			if (mousePos[1] >= self.y) and (mousePos[1] <= (self.y+self.height)):
				return True
			else: 
				return False
		else:
			return False
	
	def haveIbeenLeftClicked(self, mouseEvent):
		if (mouseEvent.type == pygame.MOUSEBUTTONDOWN) and (self.isMouseOverMe(mouseEvent) == True) and (mouseEvent.button == 1) :
			self.previousMouseLeftBtnState = "DOWN"
			self.leftClicked = True
			return True
		elif (mouseEvent.type == pygame.MOUSEBUTTONDOWN) and (self.isMouseOverMe(mouseEvent) == False) and (mouseEvent.button == 1) :
			self.leftClicked = False
			return False
		else:
			return False
	
	def haveIbeenRightClicked(self, mouseEvent):
		if (mouseEvent.type == pygame.MOUSEBUTTONDOWN) and (self.isMouseOverMe(mouseEvent) == True) and (mouseEvent.button == 3) :
			self.previousMouseRightBtnState = "DOWN"
			self.rightClicked = True
			return True
		elif (mouseEvent.type == pygame.MOUSEBUTTONDOWN) and (self.isMouseOverMe(mouseEvent) == False) and (mouseEvent.button == 3) :
			self.rightClicked = False
			return False
		else:
			return False
	
	def hasMouseButtonBeenReleased(self,mouseEvent):
		if (mouseEvent.type == pygame.MOUSEBUTTONUP) and (mouseEvent.button == 1):
			self.previousMouseLeftBtnState = "UP"
			self.dragged = False
		if (mouseEvent.type == pygame.MOUSEBUTTONUP) and (mouseEvent.button == 3):
			self.previousMouseRightBtnState = "UP"
			self.dragged = False
	
	def haveIbeenDragged(self,mouseEvent):
		if (mouseEvent.type == pygame.MOUSEMOTION) and (self.leftClicked == True) and (self.previousMouseLeftBtnState == "DOWN"): # I have been dragged
			mousePos = OpenGLlib.returnOpenGLcoord(mouseEvent.pos)
			self.dragged = True
			self.mousedisplacement_x = mousePos[0] - self.previousMousePos[0]
			self.mousedisplacement_y = mousePos[1] - self.previousMousePos[1]
			return True
	
	def handleMouseEvent(self, mouseEvent):
		if (mouseEvent.type == pygame.MOUSEBUTTONDOWN) or (mouseEvent.type == pygame.MOUSEBUTTONUP) or (mouseEvent.type == pygame.MOUSEMOTION):
			mousePos = OpenGLlib.returnOpenGLcoord(mouseEvent.pos)
			
			self.haveIbeenLeftClicked(mouseEvent)
			self.haveIbeenRightClicked(mouseEvent)
			self.hasMouseButtonBeenReleased(mouseEvent)
			self.haveIbeenDragged(mouseEvent)
			
			self.previousMousePos = mousePos
			
	# virtual method. Overload this and use the internal isMouseOverMe/ functions to implement your logic
	def eventCallback(self,event):
		#-------------------------------------------------------
		# Handle mouse events
		#-------------------------------------------------------
		self.handleMouseEvent(event)
		#if self.dragged == True:
		#	self.moveBy(self.mousedisplacement_x,self.mousedisplacement_y)
			
		
class Window(Container):

	def __init__(self,position, size, eventManager, GLFont, name = "Window"):
		self.titleBarHeight = 25
		logging.info("init Window %s, titleBarHeight: %s", name, self.titleBarHeight)
		Container.__init__(self,position, size, name )
		
		self.setBorder(1,OpenGLlib.COLOR_GREY)
		self.setSelectedBorder(1,OpenGLlib.COLOR_WHITE)
		
		self.background = ImagePanel("window/window_grey_transparent_bgd",(0,0),[self.width,self.height],[0,0])
		self.addItem(self.background,(0,0),False)
		
		self.titleBarHeight = 25
		self.titleBarbackground = ImagePanel("window/window_grey_transparent_bgd",(0,0),[self.width,self.titleBarHeight],[0,0])
		
		self.titleBar = Container((0,0), (self.width,self.titleBarHeight),"Window title bar")
		self.titleBar.setBorder(1,OpenGLlib.COLOR_GREY)
		self.titleBar.setSelectedBorder(1,OpenGLlib.COLOR_WHITE)
		self.titleBar.addItem(self.titleBarbackground,(0,0),False)
		
		self.addItem(self.titleBar,(0,self.height-self.titleBarHeight),False)
		
		self.titleBarText = TextField(GLFont)
		self.titleBar.addItem(self.titleBarText, (5,(self.titleBarHeight/2-GLFont.height/2)), False)
		
		eventManager.registerCallBack("ALL_KEY_MOUSE_EVENTS",self.eventCallback)

	def setTitleText(self, text):
		self.titleBarText.setText(text)
	
	def eventCallback(self,event):
		#-------------------------------------------------------
		# Handle mouse events
		#-------------------------------------------------------
		self.handleMouseEvent(event)
		if self.dragged == True:
			self.moveBy(self.mousedisplacement_x,self.mousedisplacement_y)

class TextBox(Container):
	
	def __init__(self,position, size, eventManager, GLFont, name = "TextBox"):
		logging.info("init TextBox %s ", name)
		Container.__init__(self,position, size, name )
		self.name = name
		
		self.setClipping(True)
		self.font = GLFont
		self.linespacing = 0
		
		self.buffer = collections.deque()
		self.textFieldsArray = []
		self.nrDisplayedLines = (self.height // (self.font.height + self.linespacing))
		
		for i in range(0,self.nrDisplayedLines+1):
			textField = TextField(self.font)
			self.textFieldsArray.append(textField)
			self.addItem(textField, (2,(self.height -self.font.height -(self.font.height+self.linespacing)*i )), False)
			
	def writeLine(self,s):
		self.buffer.append(s)
		
	def draw(self):
		if len(self.buffer)<self.nrDisplayedLines:
			imin = 0
			imax = len(self.buffer)
		else:
			imin = len(self.buffer) - self.nrDisplayedLines
			imax = self.nrDisplayedLines+1
		for i in range (imin,len(self.buffer)):
			self.textFieldsArray[i-imin].setText(self.buffer[i])
		
		super(TextBox,self).draw()
		

		
class ClippingPanel(Container):
	
	def draw(self):
		glScissor(self.x, self.y, self.width, self.height)
		glEnable(GL_SCISSOR_TEST)
		
		for image in self.itemList:
			image.draw()
		
		glDisable(GL_SCISSOR_TEST)

class ImagePanel(Panel):
	image = None

	addTranslation = (0,0)
	
	valueToRotAnglesTable= [ [0,0]]
	valueToMoveTable = [ [0,0]]
	
	rotating = False
	translating = False
	translationAngle = None
	
	rotationXPdataSource = None
	rotationXPdata = False
	rotationCenter = None
	
	translationXPdata = False
	translationXPdataSource = None
	
	rotationConvertFunction = False
	translationConvertFunction = False
	
	visibilityXPData = None
	visibilityXPdataSource = None
	visibilityToggleFunction = None

	testRotationValue = 0
	testTranslationValue = 0
	
	addRotAngleForTranslation = 0
	rot_angle = 0
	xdev = 0
	ydev = 0

	def __init__(self, imagename, position=[0,0], cliprect=None, origin=None):
		self.image = OpenGLlib.GL_Image(imagename,cliprect,origin)
		Panel.__init__(self,position, (self.image.width,self.image.height), imagename)

	def addScissorBox(self,box_origin, box_size):
		if self.image != None:
			self.image.addScissorBox(box_origin, box_size)
		
	def setRotateTexture(self,rotateTexture):
		if self.image != None:
			self.image.setRotateTexture(rotateTexture)
	
	def setTranslateTexture(self,translateTexture):
		if self.image != None:
			self.image.setTranslateTexture(translateTexture)
	
	def forceTranslateQuad(self,translateQuad):
		if self.image != None:
			self.image.forceTranslateQuad(translateQuad)
	
	def setAddTranslation(self, translation):
		self.addTranslation = translation

	def resize(self,size):
		if self.image != None:
			self.image.resize(size[0],size[1])
			self.width = self.image.width
			self.height = self.image.height

	def toggleVisibility(self,XPdataSource, dataSourceKeyIndex, visibilityToggleFunction = False):
		self.visibilityToggleFunction = visibilityToggleFunction
		self.visibilityXPdataSource = XPdataSource
		self.visibilityXPData = dataSourceKeyIndex
		
	def enableRotation(self,XPdataSource, dataSourceKeyIndex, indValueToAnglesTable, rotationConvertFunction = False):
		self.rotating = True
		self.rotationConvertFunction = rotationConvertFunction
		self.rotationXPdataSource = XPdataSource
		self.rotationXPdata = dataSourceKeyIndex
		self.valueToRotAnglesTable = indValueToAnglesTable

	def setRotationCenter(self,rotationCenter):
		self.rotationCenter = rotationCenter
	
	def enableTranslation(self,XPdataSource,dataSourceKeyIndex, indValueToTranslationTable, translationConvertFunction = False,translationAngle=None,addAngleToRotation=None):
		self.translating = True
		self.translationConvertFunction = translationConvertFunction
		if translationAngle:
			self.translationAngle = translationAngle
		if addAngleToRotation:
			self.addRotAngleForTranslation = addAngleToRotation
		self.translationXPdataSource = XPdataSource
		self.translationXPdata = dataSourceKeyIndex
		self.valueToMoveTable = indValueToTranslationTable
		
	def draw(self):
		#print "update ", self.image_name
		#def draw(self, abspos=None, relpos=None, width=None, height=None,
		#color=None, rotation=None, rotationCenter=None):
		if self.visibilityXPData:
			XPindicatedValue = float(self.visibilityXPdataSource.getData(self.visibilityXPData[0],self.visibilityXPData[1]))
			self.visible = self.visibilityToggleFunction(XPindicatedValue,self.visibilityXPdataSource)

		if self.visible == True:
			if self.rotating == True:
				#print "rotate ", self.image_name
				if self.testMode == False:
					XPindicatedValue = self.rotationXPdataSource.getData(self.rotationXPdata[0],self.rotationXPdata[1])
				else: 
					XPindicatedValue = self.testValue
					
				if self.rotationConvertFunction != False :
					XPindicatedValue = float(self.rotationConvertFunction(XPindicatedValue,self.rotationXPdataSource))
				
				self.rot_angle = self.convertValueToTransformValue(XPindicatedValue,self.valueToRotAnglesTable)

			if self.translating == True:
				#print "translate ", self.image_name
				if self.testMode == False:
					XPindicatedValue = float(self.translationXPdataSource.getData(self.translationXPdata[0],self.translationXPdata[1]))
				else: 
					XPindicatedValue = self.testValue
				
				if self.translationConvertFunction != False :
					XPindicatedValue = float(self.translationConvertFunction(XPindicatedValue,self.translationXPdataSource))
				
				translationAmount = self.convertValueToTransformValue(XPindicatedValue,self.valueToMoveTable)
				#print self.image_name," XP indicated value: ",XPindicatedValue, " transl amount = ", translationAmount
				
				if self.translationAngle: 
					transl_angle_rad = math.radians(self.translationAngle)
				else:
					transl_angle_rad = math.radians(self.rot_angle+self.addRotAngleForTranslation)
				
				self.xdev = translationAmount * math.sin(transl_angle_rad) + self.addTranslation[0]
				self.ydev = translationAmount * math.cos(transl_angle_rad) + self.addTranslation[1]
			
			logging.debug("drawing image %s, at x: %s, y %s, width: %s, height: %s ", self.name, self.x, self.y,self.width, self.height ) #print "x: ", self.x, "y: ", self.y
			self.image.draw((self.x,self.y),(self.xdev,self.ydev),self.width,self.height,None,self.rot_angle, self.rotationCenter)

	# calculate the transformation value (angle or translation)- using the translation table - returns a linear calculation between 2 values in the table
	def convertValueToTransformValue(self,indicatedValue, translationTable):
		gaugeValsDict=translationTable
		
		if indicatedValue <=gaugeValsDict[0][0]:
			return gaugeValsDict[0][1]
		for i in range(0,len(gaugeValsDict)):
			if i == len(gaugeValsDict)-1:
				transformValue = gaugeValsDict[len(gaugeValsDict)-1][1]
				return transformValue
			elif gaugeValsDict[i][0] <= indicatedValue and gaugeValsDict[i+1][0]>=indicatedValue:
				a = float(float(gaugeValsDict[i][1]-gaugeValsDict[i+1][1])/float(gaugeValsDict[i][0]-gaugeValsDict[i+1][0]))
				b = float(float(gaugeValsDict[i][0]*gaugeValsDict[i+1][1] - gaugeValsDict[i][1]*gaugeValsDict[i+1][0])/float(gaugeValsDict[i][0]-gaugeValsDict[i+1][0]))
				transformValue = float(a*indicatedValue + b)
				return transformValue

class TextField(ImagePanel):
	text = ""
	textDataSource = None
	textDataSourceKeyIndex = None
	textFormat = "%.1f"
	unitText = ""
	prefixUnit = False
	dataConvertFunction = False
	
	def __init__(self, font):
		self.image = font
	
	def setText(self, s):
		self.text = s
	
	def setTextDataSource(self,XPdataSource,dataSourceKeyIndex, dataConvertFunction = False):
		self.textDataSource = XPdataSource
		self.textDataSourceKeyIndex = dataSourceKeyIndex
		self.dataConvertFunction = dataConvertFunction
	
	def setDisplayUnit(self, unitText, prefix = False ):
		self.unitText = unitText
		self.prefixUnit = prefix
	
	def setTextFormat(self, textFormat):
		self.textFormat = textFormat
	
	def draw(self):
		if self.visible == True:
			XPValue = 0
			if self.textDataSource != None:
				XPValue = self.textDataSource.getData(self.textDataSourceKeyIndex[0],self.textDataSourceKeyIndex[1])
				if self.dataConvertFunction != False:
					XPValue = float(self.dataConvertFunction(XPValue,self.textDataSource))
				
				self.text =  self.textFormat.format(float(XPValue))
				self.text += self.unitText
				#VVI = "%.0f" % XPlaneDataDispatcher.dataList[4][2]
			
			logging.debug("drawing text %s, at x: %s, y %s ", self.text, self.x, self.y )
			self.image.draw(self.text,self.x,self.y)

class NumberTextField10kraised(ImagePanel):
	number = 0
	
	def __init__(self, font10k, font10s, fontSize10y_adjust):
		self.font10k = font10k
		self.font10s = font10s
		self.fontSize10y_adjust = fontSize10y_adjust
	
	def setNumber(self,number):
		self.number = number
		
	def draw(self):
		number10k = D(self.number)//D(1000)
		number100s = abs((D(self.number)/D(1000)%1)*1000)
		#number100s = float('{:3.0f}'.format((abs(self.number/1000)%1)*1000))
		
		font10s_x = self.x
		lw = self.font10k.lw
		
		if number10k != 0:
			self.font10k.draw('{:.0f}'.format(number10k),self.x,self.y)
			font10s_x += lw
		if (self.number <0) and (self.number > -1000):
			self.font10s.draw("-",font10s_x,self.y+self.fontSize10y_adjust)
			font10s_x += lw
		if (self.number <=-1000):
			font10s_x += lw
		if abs(number10k) >= 10:
			font10s_x += lw
			
		if number100s == 0 or number100s == 500:
			self.font10k.draw('{:0>3.0f}'.format(number100s),font10s_x,self.y)
		else:
			self.font10s.draw('{:0>3.0f}'.format(number100s),font10s_x,self.y+self.fontSize10y_adjust)

class AnimatedImage(ImagePanel):
	def __init__(self, imageDir, imageBaseName, startStepNumber, endStepNumber, imageNameSuffix, indexPadding,  position=[0,0], cliprect=None, origin=None, testMode=False):
		self.image_name = imageBaseName
		logging.info("init AnimatedImage %s", self.image_name)
		imageBaseName = os.path.join(imageDir, imageBaseName)
		self.startStepNumber = startStepNumber
		self.endStepNumber = endStepNumber
		self.visibleFrame = startStepNumber
		
		self.imageFrames = {}
		
		if endStepNumber >= startStepNumber :
			for i in range(startStepNumber,endStepNumber+1) :
				index = str(i).zfill(indexPadding)
				
				imagename = imageBaseName + index + imageNameSuffix
				logging.debug("loading AnimatedImage %s", imagename)
				self.imageFrames[i] = OpenGLlib.GL_Image(imagename,cliprect,origin)

		self.x = position[0]
		self.y = position[1]
		self.width = self.imageFrames[startStepNumber].width
		self.height = self.imageFrames[startStepNumber].height
		
		self.testMode = testMode
		self.testValue = 1
		self.dataConvertFunction = False
		self.XPdataSource = False
		self.dataSourceKeyIndex = False
		
	def resize(self,size):
		for i in range(self.startStepNumber,self.endStepNumber+1) :
			self.imageFrames[i].resize(size[0],size[1])
		self.width = self.imageFrames[self.startStepNumber].width
		self.height = self.imageFrames[self.startStepNumber].height
	
	def setAnimationDataValue(self,XPdataSource, dataSourceKeyIndex, dataConvertFunction = False):
		self.dataConvertFunction = dataConvertFunction
		self.XPdataSource = XPdataSource
		self.dataSourceKeyIndex = dataSourceKeyIndex
	
	def draw(self):
		if self.testMode == True :
			drawIndex = int(self.testValue%360)
		else :
			drawIndex = int(self.XPdataSource.getData(self.dataSourceKeyIndex[0],self.dataSourceKeyIndex[1]))
		if self.dataConvertFunction != False:
			drawIndex = self.dataConvertFunction(drawIndex,self.XPdataSource)
		
		self.imageFrames[drawIndex].draw((self.x,self.y),(0,0),self.width,self.height)
	
	