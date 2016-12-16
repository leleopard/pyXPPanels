import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class Gen_SliderIndicator(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, zoom = 1.0, layer = 0, name = "Gen_SliderIndicator"):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.batchImageRenderer = batchImageRenderer
		self.layer = layer
		
		self.sliderBase = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [101,30],	[0			,256-30		])
		self.centerGrad  = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [101,30],	[0			,256-61		])
		self.tensGrads = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [101,30],	[0			,256-91		])
		
		self.sliderPointer = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [101,30],	[0			,256-121		])
		
		self.addItem(self.sliderBase)
		self.addItem(self.centerGrad)
		self.addItem(self.tensGrads)
		self.addItem(self.sliderPointer)

		
	def draw(self):
		
		super(Gen_SliderIndicator,self).draw()

