import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_RPM_Indicator(graphics.Container):
	
	def __init__(self,position, size,  batchImageRenderer, texture, zoom = 1.0, name = "C172_RPM_Indicator"):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#------------------------------------------------------------------------------------------
		#	RPM
		#------------------------------------------------------------------------------------------
		self.RPMBackground = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [280,280],	[300*4		,2048-300*3		])
		self.RPMNeedle = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [280,280],	[300*5		,2048-300*3		])
		self.RPMBezel = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [310,310],	[300*4		,2048-300*6-10	])
		self.RPMBezel.resize([280*zoom,280*zoom])

		self.RPMNeedle.enableRotation ((37,0),[ [0,-124.5],
			[500,-94],
			[1000,-64.5],
			[1800,0],
			[2000,15.5],
			[2200,32],
			[2500,55],
			[2600,62],
			[2700,70.5],
			[3500,125.5]])

		self.addItem(self.RPMBackground)
		self.addItem(self.RPMNeedle)
		self.addItem(self.RPMBezel, [0,0], False)
		
	def draw(self):
		
		super(C172_RPM_Indicator,self).draw()

