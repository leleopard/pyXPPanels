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
		self.zoom = zoom
		
		self.sliderBase = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [101,30],	[0			,256-30		])
		self.centerGrad  = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [101,30],	[0			,256-61		])
		self.tensGrads = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [101,30],	[0			,256-91		])
		
		self.sliderPointer = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [101,30],	[0			,256-121		])
		
		self.addItem(self.sliderBase)
		self.addItem(self.centerGrad)
		self.addItem(self.tensGrads)
		self.addItem(self.sliderPointer)
	
	## set if the center graduation of the slider is visible or not
	# @param visible boolean True or False
	#
	def setCenterGradVisible(self, visible):
		self.centerGrad.setVisible(visible)
	
	## set if the tens graduations of the slider are visible or not
	# @param visible boolean True or False
	#
	def setTensGradsVisible(self, visible):
		self.tensGrads.setVisible(visible)
	
	## sets which dataref value the pointer tracks, and position depending on value
	# @param tuple pointerDataref: ID, and index (0..7) of the value tracked
	# @param dataConversionTable: 
	#
	def setPointerDataref(self, pointerDatarefID, dataConversionTable = [ [-1.0,-1.0],[1.0,1.0]] ):
		for i in range(0, len(dataConversionTable)):
			dataConversionTable[i][1] = dataConversionTable[i][1] * 50 * self.zoom
			
		self.sliderPointer.enableTranslation (self.XPlaneDataDispatcher,pointerDatarefID,dataConversionTable, False, 90)
		
		
	def draw(self):
		
		super(Gen_SliderIndicator,self).draw()

