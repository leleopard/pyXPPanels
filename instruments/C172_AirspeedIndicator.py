import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_AirspeedIndicator(graphics.Container):
	
	def __init__(self,position, size, batchImageRenderer, texture, zoom = 1.0, name = "C172_AirspeedIndicator"):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#------------------------------------------------------------------------------------------
		#	Airspeed Indicator
		#------------------------------------------------------------------------------------------
		self.airspeedBackground = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[0				,2048-300*2		])
		self.airspeedNeedle = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [40,300],	[300*2+ 130		,2048-300*6		])
		self.airspeedNeedle.resize([40*zoom,300*zoom])
		self.airspeedBezel = 		graphics.ImagePanel(texture, batchImageRenderer,self.layer, [0,0], [310,310],	[300*4	,2048-300*6-10	])
		self.airspeedBezel.resize([310*zoom,310*zoom])

		self.airspeedNeedle.enableRotation((3,0), [ [0,0],
			[40,30],
			[50,50],
			[60,70],
			[70,90],
			[80,115],
			[90,140.5],
			[95,151],
			[100,162.5],
			[105,174],
			[110,185],
			[115,196],
			[120,207.5],
			[130,222.5],
			[140,237.5],
			[160,267.5],
			[200,317.5]])
			
		self.addItem(self.airspeedBackground)
		self.addItem(self.airspeedNeedle,[0,0],False)
		self.addItem(self.airspeedBezel,[0,0],False)
		
	def draw(self):
		
		super(C172_AirspeedIndicator,self).draw()

