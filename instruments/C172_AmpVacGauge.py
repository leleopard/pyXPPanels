import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_AmpVacGauge(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, name = "C172_AmpVacGauge"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#------------------------------------------------------------------------------------------
		#	AMP and VAC gauge
		#------------------------------------------------------------------------------------------
		self.vacAmpGaugeBackground = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*7		])
		
		self.vacAmpGaugeRightNeedle = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [110,18],	[300*6		,2048-200*3-36	])
		self.vacAmpGaugeRightNeedle.resize([110,18])
		self.vacAmpGaugeRightNeedle.enableRotation (XPlaneDataDispatcher,(53,0),[ [-66,-59],[0,0],[66,57]])
		
		self.vacAmpGaugeLeftNeedle = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [110,18],	[300*6		,2048-200*3-18	])
		self.vacAmpGaugeLeftNeedle.resize([110,18])
		self.vacAmpGaugeLeftNeedle.enableRotation (XPlaneDataDispatcher,(7,2),[ [2.8,57],[3,52],[4,26],[5,0],[6,-25],[7,-50],[7.2,-55]],conversionFunctions.convertSuction)
		
		self.vacAmpGaugeBorder = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*3		])
		self.vacAmpGaugeText = 				graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [200,200],	[300*6		,2048-200*10	])
		self.vacAmpGaugeBezel = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [310,310],	[300*4		,2048-300*6-10	])
		self.vacAmpGaugeBezel.resize([200,200])

		self.addItem(self.vacAmpGaugeBackground)
		self.addItem(self.vacAmpGaugeRightNeedle,[60,0.5], False)
		self.addItem(self.vacAmpGaugeLeftNeedle,[-56,2], False)
		self.addItem(self.vacAmpGaugeBorder)
		self.addItem(self.vacAmpGaugeText)
		self.addItem(self.vacAmpGaugeBezel)
				
	def draw(self):
		
		super(C172_AmpVacGauge,self).draw()

