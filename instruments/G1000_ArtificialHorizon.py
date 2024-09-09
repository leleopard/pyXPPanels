import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class G1000_ArtificialHorizon(graphics.Container):
	
	def __init__(self,position, size, batchImageRenderer, texture, zoom = 1.0, name = "G1000_ArtificialHorizon"):
		graphics.Container.__init__(self,position, (size[0]*zoom, size[1]*zoom), name)
		
		self.testMode = False
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#------------------------------------------------------------------------------------------
		#	Artificial Horizon
		#------------------------------------------------------------------------------------------
		G1000HorizonTexture = 	OpenGL3lib.GL_Texture("data/G1000_horizon.png")
		#								def __init__(self, texture, batchImageRenderer, layer=0, position=[0,0], cliprect=None, origin=None, name = ""):
		self.G1000Horizon = 		graphics.ImagePanel(G1000HorizonTexture, batchImageRenderer, self.layer, (0,0), [835,626], [606,713])			#G1000_horizon
		
		
		self.G1000BankIndicator = 	graphics.ImagePanel(texture, batchImageRenderer, self.layer+1,(0,0),[400,200],[56,28])	#G1000_bankindicator
		self.G1000BankIndicator.resize((400,200))
		self.G1000Bug = 			graphics.ImagePanel(texture, batchImageRenderer, self.layer+1,[0,0],[512,256],[512,0])					#G1000_bug
		self.G1000Bug.resize((512,256))
		
		self.G1000PitchScale = 		graphics.ImagePanel(texture, batchImageRenderer, self.layer+1, (0,0), [215,210], [21,2048-1409-149])			#G1000_horizon
		self.G1000PitchScale.resize((215,210))
		
		self.G1000Horizon.enableTextureRotation ((17,1),[ [-180,-180],[180,180]])
		self.G1000Horizon.enableTextureTranslation ((17,0),[ [-70,-398],[70,398]])
		self.G1000Horizon.setTextureRotationCenter((982,2048-939))
		
		self.G1000PitchScale.enableTextureRotation ((17,1),[ [-180,-180],[180,180]])
		self.G1000PitchScale.enableTextureTranslation ((17,0),[ [-70,-398],[70,398]])
		self.G1000PitchScale.setTextureRotationCenter((128,2048-1460))
		
		self.G1000BankIndicator.enableTextureRotation ((17,1),[ [-180,-180],[180,180]])
		self.G1000BankIndicator.setTextureRotationCenter((256,2048-1994))
		
		BUG_BANK_IND_POS = [-43,156]
		
		self.addItem(self.G1000Horizon)
		self.addItem(self.G1000BankIndicator,BUG_BANK_IND_POS,False)
		self.addItem(self.G1000Bug,BUG_BANK_IND_POS,False)
		self.addItem(self.G1000PitchScale,(-42,90),False)
		
	def draw(self):
		
		super(G1000_ArtificialHorizon,self).draw()

