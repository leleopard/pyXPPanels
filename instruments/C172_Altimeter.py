import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_Altimeter(graphics.Container):
	
	def __init__(self,position, size, batchImageRenderer, texture, zoom = 1.0, name = "C172_DirectionalGyro"):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#------------------------------------------------------------------------------------------
		#	Altimeter
		#------------------------------------------------------------------------------------------
		self.altimeterBlackBackground = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300		,2048-300*2		])
		self.altimeterHgWheel = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*2		,2048-300*2		])
		self.altimeterMbWheel = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*2		,2048-300*3		])
		self.altimeterBackground = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300		,2048-300*3		])
		self.altimeter10kNeedle =			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*3		,2048-300*3		])
		self.altimeter1kNeedle = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [40,300],	[130		,2048-300*6		])
		self.altimeter1kNeedle.resize([40*zoom,300*zoom])
		self.altimeter100sNeedle =			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [40,300],	[430		,2048-300*6		])
		self.altimeter100sNeedle.resize([40*zoom,300*zoom])
		
		self.altimeterBezel = 				graphics.ImagePanel(texture, batchImageRenderer,self.layer, [0,0], [310,310],	[300*4	,2048-300*6-10	])
		self.altimeterBezel.resize([310*zoom,310*zoom])

		self.altimeterMbWheel.enableRotation ((7,0),[ [945,165.5],[1000,0.5],[1050,-149.5]],conversionFunctions.convertINtomb)
		self.altimeterHgWheel.enableRotation ((7,0),[ [28,154],[29.5,-0.5],[31.1,-165.1]])
		self.altimeter100sNeedle.enableRotation ("sim/cockpit2/gauges/indicators/altitude_ft_pilot",[ [0,0],[1.0,360]],conversionFunctions.return100s)
		self.altimeter1kNeedle.enableRotation ("sim/cockpit2/gauges/indicators/altitude_ft_pilot",[ [0,0],[1.0,360]],conversionFunctions.return1000s)
		self.altimeter10kNeedle.enableRotation ("sim/cockpit2/gauges/indicators/altitude_ft_pilot",[ [0,0],[1.0,360]],conversionFunctions.return10000s)

		self.addItem(self.altimeterBlackBackground)
		self.addItem(self.altimeterHgWheel)
		self.addItem(self.altimeterMbWheel)
		self.addItem(self.altimeterBackground)
		self.addItem(self.altimeter10kNeedle)
		self.addItem(self.altimeter1kNeedle,[0,0],False)
		self.addItem(self.altimeter100sNeedle,[0,0],False)
		self.addItem(self.altimeterBezel,[0,0],False)

		
	def draw(self):
		
		super(C172_Altimeter,self).draw()

