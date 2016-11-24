import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_ADF(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, zoom = 1.0, name = "C172_ADF"):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#------------------------------------------------------------------------------------------
		#	ADF
		#------------------------------------------------------------------------------------------
		self.ADFNeedle = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300		,2048-300		])
		self.ADFCompass = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300		,2048-300*5		])
		self.ADFPlane = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*2		,2048-300		])
		self.ADFBezel = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [310,310],	[300*4		,2048-300*6-10	])
		self.ADFBezel.resize([310*zoom,310*zoom])

		self.ADFCompass.enableRotation (XPlaneDataDispatcher,(101,1),[ [-360,360],[360,-360]])
		self.ADFNeedle.enableRotation (XPlaneDataDispatcher,(101,2),[ [-360,-360],[360,360]])

		self.addItem(self.ADFNeedle)
		self.addItem(self.ADFCompass)
		self.addItem(self.ADFPlane)
		self.addItem(self.ADFBezel)
		
	def draw(self):
		
		super(C172_ADF,self).draw()

