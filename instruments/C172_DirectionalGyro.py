import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_DirectionalGyro(graphics.Container):
	
	def __init__(self,position, size, batchImageRenderer, texture, zoom = 1.0, name = "C172_DirectionalGyro"):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#------------------------------------------------------------------------------------------
		#	Directional Gyro
		#------------------------------------------------------------------------------------------
		self.dirGyroBackground = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[0			,2048-300*3		])
		self.dirGyroBug = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*3		,2048-300*2		])
		self.dirGyroPlane = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*3		,2048-300		])
		self.dirGyroBezel =  		graphics.ImagePanel(texture, batchImageRenderer,self.layer, [0,0], [310,310],	[300*4	,2048-300*6-10	])
		self.dirGyroBezel.resize([310*zoom,310*zoom])
		
		self.dirGyroBackground.enableRotation ((308,0),[[0,0],[160,-160],[210,-211],[360,-360]])
		self.dirGyroBug.enableRotation ((118,1),[ [0,0],[160,160],[210,211],[360,360]], conversionFunctions.addCompassHeadingToValue)

		self.addItem(self.dirGyroBackground)
		self.addItem(self.dirGyroBug)
		self.addItem(self.dirGyroPlane)
		self.addItem(self.dirGyroBezel, [0,0], False)

		
	def draw(self):
		
		super(C172_DirectionalGyro,self).draw()

