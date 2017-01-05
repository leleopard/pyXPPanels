import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_ArtificialHorizon(graphics.Container):
	
	def __init__(self,position, size, batchImageRenderer, texture, zoom = 1.0, name = "C172_ArtificialHorizon"):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#------------------------------------------------------------------------------------------
		#	Artificial Horizon
		#------------------------------------------------------------------------------------------
		self.artHorizonBackgroundHor = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[0			,2048-300*4		])
		self.artHorizonInnerHor = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300		,2048-300*4		], 	"artHorizonInnerHor")
		self.artHorizonOuterHor = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*2		,2048-300*4		], 	"artHorizonOuterHor")
		self.artHorizonPlaneGizmo = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*4		,2048-300*4		])
		self.artHorizonPlane = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*3		,2048-300*4		])
		self.artHorizonBezel = 			graphics.ImagePanel(texture, batchImageRenderer,self.layer, [0,0], [310,310],	[300*4	,2048-300*6-10	])
		self.artHorizonBezel.resize([310*zoom,310*zoom])

		self.artHorizonOuterHor.enableRotation ((17,1),[[-180,180],[0,0],[180,-180]])
		self.artHorizonInnerHor.enableRotation ((17,1),[[-180,180],[0,0],[180,-180]])
		self.artHorizonInnerHor.enableTranslation ((17,0),[[-25,48*zoom],[0,0],[25,-50*zoom]])
		self.artHorizonBackgroundHor.enableRotation ((17,1),[ [-180,180],[0,0],[180,-180]])
		self.artHorizonPlaneGizmo.enableTranslation ((306,0),[[-25,-48*zoom],[0,0],[25,50*zoom]])
		
		self.addItem(self.artHorizonBackgroundHor)
		self.addItem(self.artHorizonInnerHor)
		self.addItem(self.artHorizonOuterHor)
		self.addItem(self.artHorizonPlaneGizmo)
		self.addItem(self.artHorizonPlane)
		
		self.addItem(self.artHorizonBezel,[0,0],False)
		
	def draw(self):
		
		super(C172_ArtificialHorizon,self).draw()

