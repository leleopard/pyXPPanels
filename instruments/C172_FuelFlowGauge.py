import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_FuelFlowGauge(graphics.Container):
	
	def __init__(self,position, size, batchImageRenderer, texture, name = "C172_FuelFlowGauge"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#------------------------------------------------------------------------------------------
		#	Fuel Flow gauge
		#------------------------------------------------------------------------------------------
		self.fuelFlowGaugeBackground = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*6		])
		
		self.fuelFlowGaugeRightNeedle = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [110,18],	[300*6		,2048-200*3-36	])
		self.fuelFlowGaugeRightNeedle.resize([110,18])
		self.fuelFlowGaugeRightNeedle.enableRotation ((45,0),[ [2.81,-65],[4,-57],[15,17],[19,55],[19.84,63]],conversionFunctions.convertLbsToGallons)
		
		self.fuelFlowGaugeLeftNeedle = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [110,18],	[300*6		,2048-200*3-18	])
		self.fuelFlowGaugeLeftNeedle.resize([110,18])
		self.fuelFlowGaugeLeftNeedle.enableRotation ((47,0),[ [0,58],[100,52],[1700,-49],[1900,-62]])
		
		self.fuelFlowGaugeBorder = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*3		])
		self.fuelFlowGaugeText =			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*9	])
		self.fuelFlowGaugeBezel = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [310,310],	[300*4		,2048-300*6-10	])
		self.fuelFlowGaugeBezel.resize([200,200])

		self.addItem(self.fuelFlowGaugeBackground)
		self.addItem(self.fuelFlowGaugeRightNeedle,[56,4], False)
		self.addItem(self.fuelFlowGaugeLeftNeedle,[-56,4], False)
		self.addItem(self.fuelFlowGaugeBorder)
		self.addItem(self.fuelFlowGaugeText)
		self.addItem(self.fuelFlowGaugeBezel)
				
	def draw(self):
		
		super(C172_FuelFlowGauge,self).draw()

