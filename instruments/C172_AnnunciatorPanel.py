import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class C172_AnnunciatorPanel(graphics.Container):
	
	def __init__(self,position, size, batchImageRenderer, texture, name = "C172_AnnunciatorPanel"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		#-------------------------------------------------------------------------------------------------
		# Annunciator Container background
		#-------------------------------------------------------------------------------------------------
		self.C172_AnnunciatorPanel_background  = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [446,66],	[300		,2048-300*6-67		])

		self.addItem(self.C172_AnnunciatorPanel_background)
		
		annunc_xoffset = -155
		annunc_yoffset = 13
		
		self.C172_AnnunciatorPanel_alternator  = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [107,24],	[300		,2048-300*6-67-25		])
		self.C172_AnnunciatorPanel_alternator.resize([107,24])
		self.C172_AnnunciatorPanel_alternator.toggleVisibility((115,4), conversionFunctions.returnTrueIfOverZero)
		self.addItem(self.C172_AnnunciatorPanel_alternator, (annunc_xoffset,annunc_yoffset), False)
		
		self.C172_AnnunciatorPanel_battery  = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [107,24],	[300+107		,2048-300*6-67-25		])
		self.C172_AnnunciatorPanel_battery.resize([107,24])
		self.C172_AnnunciatorPanel_battery.toggleVisibility((113,5), conversionFunctions.returnTrueIfOverZero)
		self.addItem(self.C172_AnnunciatorPanel_battery, (annunc_xoffset+107,annunc_yoffset), False)
		
		self.C172_AnnunciatorPanel_lowfuel  = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [107,24],	[300+107*2		,2048-300*6-67-25		])
		self.C172_AnnunciatorPanel_lowfuel.resize([107,24])
		self.C172_AnnunciatorPanel_lowfuel.toggleVisibility((113,6), conversionFunctions.returnTrueIfOverZero)
		self.addItem(self.C172_AnnunciatorPanel_lowfuel, (annunc_xoffset+107*2,annunc_yoffset), False)
		
		self.C172_AnnunciatorPanel_brakes  = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [107,24],	[300+107*3		,2048-300*6-67-25		])
		self.C172_AnnunciatorPanel_brakes.resize([107,24])
		self.C172_AnnunciatorPanel_brakes.toggleVisibility((14,1), conversionFunctions.returnTrueIfOverZero)
		self.addItem(self.C172_AnnunciatorPanel_brakes, (annunc_xoffset+107*3,annunc_yoffset), False)
		
		self.C172_AnnunciatorPanel_oilpress  = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [107,25],	[300		,2048-300*6-67-25*2		])
		self.C172_AnnunciatorPanel_oilpress.resize([107,25])
		self.C172_AnnunciatorPanel_oilpress.toggleVisibility((115,1), conversionFunctions.returnTrueIfOverZero)
		self.addItem(self.C172_AnnunciatorPanel_oilpress, (annunc_xoffset,annunc_yoffset-25), False)

		self.C172_AnnunciatorPanel_oiltemp  = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [107,25],	[300+107		,2048-300*6-67-25*2		])
		self.C172_AnnunciatorPanel_oiltemp.resize([107,25])
		self.C172_AnnunciatorPanel_oiltemp.toggleVisibility((115,2), conversionFunctions.returnTrueIfOverZero)
		self.addItem(self.C172_AnnunciatorPanel_oiltemp, (annunc_xoffset+107,annunc_yoffset-25), False)

		self.C172_AnnunciatorPanel_lowvacuum  = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [107,25],	[300+107*2		,2048-300*6-67-25*2		])
		self.C172_AnnunciatorPanel_lowvacuum.resize([107,25])
		self.C172_AnnunciatorPanel_lowvacuum.toggleVisibility((113,4), conversionFunctions.returnTrueIfOverZero)
		self.addItem(self.C172_AnnunciatorPanel_lowvacuum, (annunc_xoffset+107*2,annunc_yoffset-25), False)

		self.C172_AnnunciatorPanel_apdisconnect  = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [107,25],	[300+107*3		,2048-300*6-67-25*2		])
		self.C172_AnnunciatorPanel_apdisconnect.resize([107,25])
		self.C172_AnnunciatorPanel_apdisconnect.toggleVisibility((113,3), conversionFunctions.returnTrueIfOverZero)
		self.addItem(self.C172_AnnunciatorPanel_apdisconnect, (annunc_xoffset+107*3,annunc_yoffset-25), False)


	def draw(self):
		
		super(C172_AnnunciatorPanel,self).draw()

