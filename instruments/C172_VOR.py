import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_VOR(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, name = "C172_VOR", VOR_ID = "VOR1", zoom = 1.0):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		if VOR_ID == "VOR1":
			VORcompassData = (98,0)
			VORvneedleData = (99,5)
			VORhneedleData = (99,6)
			VORTO_FR_NAVindicatorData = (98,2)
			VORGSflagData = (99,0)
		else:
			VORcompassData = (98,4)
			VORvneedleData = (100,5)
			VORhneedleData = (100,6)
			VORTO_FR_NAVindicatorData = (98,6)
			VORGSflagData = (100,0)
			
		#------------------------------------------------------------------------------------------
		#	VOR
		#------------------------------------------------------------------------------------------
		self.VORGSflag = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [45,27],	[44			,7				])
		self.VORGSflag.resize([45*zoom,27*zoom])
		self.VORNAV1flag = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [40,74],	[44			,35				])
		self.VORNAV1flag.resize([40*zoom,74*zoom])
		
		self.VORbackground = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[0			,2048-300*5		])
		
		self.VORFRindicator = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [37,31],	[8			,7				])
		self.VORFRindicator.resize([37*zoom,31*zoom])
		self.VORTOindicator = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [37,31],	[8			,38				])
		self.VORTOindicator.resize([37*zoom,31*zoom])
		
		self.VORhneedle = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [148,8],	[0			,0				])
		self.VORhneedle.resize([148*zoom,8*zoom])
		self.VORvneedle = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [9,150],	[0			,9				])
		self.VORvneedle.resize([9*zoom,149*zoom])
		
		self.VORcompass = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300		,2048-300*5		])
		self.VORdirarrows = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*2		,2048-300*5		])
		
		self.VORbezel = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [310,310],	[300*4	,2048-300*6-10	])
		self.VORbezel.resize([310*zoom,310*zoom])

		self.VORcompass.enableRotation (XPlaneDataDispatcher,VORcompassData,[ [-380,380],[360,-360]])
		self.VORhneedle.enableTranslation (XPlaneDataDispatcher,VORhneedleData,[ [-2.5,65*zoom],[2.5,-65*zoom]])
		self.VORvneedle.enableTranslation (XPlaneDataDispatcher,VORvneedleData,[ [-2.5,-65*zoom],[2.5,65*zoom]],False,90)
		
		self.VORTOindicator.toggleVisibility(XPlaneDataDispatcher,VORTO_FR_NAVindicatorData, conversionFunctions.NAV_TO_Toggle)
		self.VORFRindicator.toggleVisibility(XPlaneDataDispatcher,VORTO_FR_NAVindicatorData, conversionFunctions.NAV_FR_Toggle)
		self.VORNAV1flag.toggleVisibility(XPlaneDataDispatcher,VORTO_FR_NAVindicatorData, conversionFunctions.NAV_FLG_Toggle)
		self.VORGSflag.toggleVisibility(XPlaneDataDispatcher,VORGSflagData, conversionFunctions.NAV_GSFLG_Toggle)

		self.addItem(self.VORNAV1flag,		[22*zoom,51*zoom], 	False)
		self.addItem(self.VORGSflag,		[-45*zoom,23*zoom], 	False)
		
		self.addItem(self.VORbackground)
		
		self.addItem(self.VORTOindicator,	[46*zoom,27*zoom], 	False)
		self.addItem(self.VORFRindicator,	[46*zoom,-27*zoom], 	False)
		
		self.addItem(self.VORvneedle	, 	[0,2*zoom], 		False)
		self.addItem(self.VORhneedle	, 	[0,0], 		False)
		self.addItem(self.VORcompass)
		self.addItem(self.VORdirarrows)
		self.addItem(self.VORbezel		, 	[0,0], 		False)
		
	def draw(self):
		
		super(C172_VOR,self).draw()

