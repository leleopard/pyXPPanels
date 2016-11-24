import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_OilPressTempGauge(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, name = "C172_OilPressTempGauge"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		self.oilGaugeBackground = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*5		])
		
		self.oilGaugeRightNeedle = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [110,18],	[300*6		,2048-200*3-36		])
		self.oilGaugeRightNeedle.resize([110,18])
		self.oilGaugeRightNeedle.enableRotation (self.XPlaneDataDispatcher,(49,0),[ [-7.821,-60.5],[100,36],[121.3636,59.5]])
		
		self.oilGaugeLeftNeedle = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [110,18],	[300*6		,2048-200*3-18		])
		self.oilGaugeLeftNeedle.resize([110,18])
		self.oilGaugeLeftNeedle.enableRotation (self.XPlaneDataDispatcher,(50,0),[ [58.33,62],[150,18],[200,-30],[257.6,-62]])
		
		self.oilGaugeBorder = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*3		])
		self.oilGaugeSideText = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*8		])
		
		self.oilGaugeBezel = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [310,310],	[300*4		,2048-300*6-10	])
		self.oilGaugeBezel.resize([200,200])

		self.addItem(self.oilGaugeBackground)
		
		self.addItem(self.oilGaugeRightNeedle,[60,3], False)
		self.addItem(self.oilGaugeLeftNeedle,[-55,5], False)
		self.addItem(self.oilGaugeBorder)
		self.addItem(self.oilGaugeSideText)
		self.addItem(self.oilGaugeBezel)
				
	def draw(self):
		
		super(C172_OilPressTempGauge,self).draw()

