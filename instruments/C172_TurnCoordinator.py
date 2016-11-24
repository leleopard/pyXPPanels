import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_TurnCoordinator(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, zoom = 1.0, name = "C172_TurnCoordinator"):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#------------------------------------------------------------------------------------------
		#	Turn Coordinator
		#------------------------------------------------------------------------------------------
		self.turnCoordBallBackground = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*4			,2048-300		])
		self.turnCoordBall =			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*5			,2048-300		], "TC BALL")
		self.turnCoordBackground = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*4			,2048-300*2		])
		self.turnCoordPlane = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [300,300],	[300*5			,2048-300*2		])
		self.turnCoordBezel =			graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [310,310],	[300*4			,2048-300*6-10	])
		self.turnCoordBezel.resize([310*zoom,310*zoom])
		
		self.turnCoordPlane.enableRotation (XPlaneDataDispatcher,(17,3),[ [-9,-60],[-3,-20],[0,0],[3,20],[9,60]],conversionFunctions.calculateTurnRate)
		self.turnCoordBall.enableRotation (XPlaneDataDispatcher,(18,7),[ [-7,-15],[0,0],[7,15]])
		#self.turnCoordBall.setRotationCenter((0,671))
		self.turnCoordBall.setRotationCenter((0,300*zoom))
		
		self.addItem(self.turnCoordBallBackground)
		self.addItem(self.turnCoordBall)
		self.addItem(self.turnCoordBackground)
		self.addItem(self.turnCoordPlane)
		self.addItem(self.turnCoordBezel, [0,0], False)

		
	def draw(self):
		
		super(C172_TurnCoordinator,self).draw()

