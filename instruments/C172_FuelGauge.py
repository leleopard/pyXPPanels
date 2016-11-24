import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions


class C172_FuelGauge(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, name = "C172_FuelGauge"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		self.fuelGaugeBackground = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*1		])
		
		self.fuelGaugeRightNeedle = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [110,18],	[300*6		,2048-200*3-36		])
		self.fuelGaugeRightNeedle.resize([110,18])
		self.fuelGaugeRightNeedle.enableRotation (self.XPlaneDataDispatcher,(62,1),[ [-1.74,-66],[20,34],[28.08,65]],conversionFunctions.convertLbsToGallons)
		self.fuelGaugeLeftNeedle = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [110,18],	[300*6		,2048-200*3-18		])
		self.fuelGaugeLeftNeedle.resize([110,18])
		self.fuelGaugeLeftNeedle.enableRotation (self.XPlaneDataDispatcher,(62,0),[ [-1.74,62],[20,-33],[28.08,-64] ],conversionFunctions.convertLbsToGallons)
		self.fuelGaugeBorder = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*3		])
		self.fuelGaugeText =			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*2		])
		self.fuelGaugeBezel =			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [310,310],	[300*4		,2048-300*6-10	])
		self.fuelGaugeBezel.resize([200,200])


		self.addItem(self.fuelGaugeBackground)
		self.addItem(self.fuelGaugeRightNeedle, [57,4], False)
		self.addItem(self.fuelGaugeLeftNeedle,[-55,5], False)
		self.addItem(self.fuelGaugeBorder)
		self.addItem(self.fuelGaugeText)
		self.addItem(self.fuelGaugeBezel)
				
	def draw(self):
		
		super(C172_FuelGauge,self).draw()

