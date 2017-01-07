import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions

class GenCompass(graphics.Container):
	
	def __init__(self,position, size, batchImageRenderer, texture, name = "GenCompass"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.batchImageRenderer = batchImageRenderer
		self.layer = 0
		
		self.previousCompassHeading = 0.0
		
		#------------------------------------------------------------------------------------------
		#	COMPASS
		#------------------------------------------------------------------------------------------
		self.CompassRose = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [120,66],	[2	,2048-66	])
		self.CompassRose.resize([120,66])
		
		self.CompassCover = graphics.ImagePanel(texture, batchImageRenderer, self.layer, [0,0], [185,185],	[0	,0	])
		self.CompassCover.resize([185,185])
		
		self.addItem(self.CompassRose,[0,0],False)
		self.addItem(self.CompassCover,[3,-5],False)
		
	def renderRose(self):
		# value is mag compass heading
		if self.testMode == False:
			compassHeading = XPlaneUDPServer.pyXPUDPServer.getData("sim/cockpit2/gauges/indicators/compass_heading_deg_mag[0]") % 360
		else:
			compassHeading = self.testValue % 360
		
		if abs(compassHeading - self.previousCompassHeading) > 0.1:
			self.previousCompassHeading = compassHeading
			#1 deg = 2px
			compassHdgDecplaces = compassHeading%1.0
			intCompassHeading = D(compassHeading)//D(1)
			textX = (-compassHdgDecplaces+ float(intCompassHeading%16*122))
			textY = 2048-float((intCompassHeading//16*66))
			
			#print ( "heading:", x,	"nr_intCompassHeading", 	x_nr,	"x_px:",	x_px,	"y_nr", 	y_nr,	"y_px:",	y_px,	"x trans: ", textX, "y trans: ", textY)
			#print("heading:", compassHeading, "textX", textX, "textY", textY)
			#print ("intCompassHeading:",intCompassHeading)
			#print ("textXpx:",textXpx,"textYpx:",textYpx)
			
			self.CompassRose.translateTexture(textX,textY)

		
	def draw(self):
		super(GenCompass,self).draw()
		self.renderRose()
		

