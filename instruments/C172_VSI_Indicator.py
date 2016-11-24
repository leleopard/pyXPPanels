import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_VSI_Indicator(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, zoom = 1.0, name = "C172_VSI_Indicator"):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		#------------------------------------------------------------------------------------------
		#	Vertical Speed Indicator
		#------------------------------------------------------------------------------------------
		#graphics.ImagePanel.__init__(texture, position=[0,0], cliprect=None, origin=None):
	
		self.varioBackground = 	graphics.ImagePanel(texture, batchImageRenderer,self.layer, [0,0], [300,298],	[0		,2048-300		])		# vario background
		self.varioNeedle = 		graphics.ImagePanel(texture, batchImageRenderer,self.layer, [0,0], [40,300],	[430	,2048-300*6		])			# needle
		self.varioNeedle.resize([40*zoom,300*zoom])
		self.varioBezel = 		graphics.ImagePanel(texture, batchImageRenderer,self.layer, [0,0], [310,310],	[300*4	,2048-300*6-10	])		# vario background
		self.varioBezel.resize([310*zoom,310*zoom])
		
		self.varioNeedle.enableRotation (XPlaneDataDispatcher,(4,2),[ [-2000,96.5],[-1500,140],[-1000,189.5],[-500,235],[0,270],[500,304.5],[1000,349.5],[1500,400],[2000,442.5]])

		self.addItem(self.varioBackground)
		self.addItem(self.varioNeedle,[0,0],False)
		self.addItem(self.varioBezel,[0,0], False)

		
	def draw(self):
		
		super(C172_VSI_Indicator,self).draw()

