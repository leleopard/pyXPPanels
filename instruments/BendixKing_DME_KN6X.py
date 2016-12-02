import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.graphics import fonts

from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions


class BK_DME_KN6X(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, name = "BK_NAVCOMM_KX165A"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.layer = 1
		
		TXT_FMT_3DIG_PREC2 = '{:06.2f}'
		TXT_FMT_3DIG_PREC3 = '{:07.3f}'
		
		x_DME_txt 		= 10
		x_DME_speed 	= 182
		x_DME_time 		= 302
		y_frequencies 	= -20
		#-------------------------------------------------------------------------------------------------
		# Background 
		#-------------------------------------------------------------------------------------------------
		self.DME_BGD = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[417,46],[0,2048-117], "DME_BGD")
		self.DME_BGD.resize((417,46))
		self.addItem(self.DME_BGD, (208.5,0), False)
		
		# DME Distance text
		self.DME_DIST_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.DME_DIST_Text.setTextFormat('{:05.1f}')
		self.DME_DIST_Text.setTextDataSource(self.XPlaneDataDispatcher,(102,3))
		self.addItem(self.DME_DIST_Text, (x_DME_txt,y_frequencies), False)
		
		# DME Speed text
		self.DME_SPEED_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.DME_SPEED_Text.setTextFormat('{:03.0f}')
		self.DME_SPEED_Text.setTextDataSource(self.XPlaneDataDispatcher,(102,4))
		self.addItem(self.DME_SPEED_Text, (x_DME_speed,y_frequencies), False)
		
		# DME time text
		self.DME_TIME_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.DME_TIME_Text.setTextFormat('{:03.0f}')
		self.DME_TIME_Text.setTextDataSource(self.XPlaneDataDispatcher,(102,5))
		self.addItem(self.DME_TIME_Text, (x_DME_time,y_frequencies), False)
		
		# DME NAV1 indicator
		self.DME_NAV1_Indicator = graphics.TextField(fonts.ARIAL_CONDENSED_SMALL_ORANGE)
		self.DME_NAV1_Indicator.setTextFormat('{:01.0f}')
		self.DME_NAV1_Indicator.setText('1')
		self.addItem(self.DME_NAV1_Indicator, (x_DME_txt+135,y_frequencies), False)
		
		# DME NAV2 indicator
		self.DME_NAV2_Indicator = graphics.TextField(fonts.ARIAL_CONDENSED_SMALL_ORANGE)
		self.DME_NAV2_Indicator.setTextFormat('{:01.0f}')
		self.DME_NAV2_Indicator.setText('2')
		self.addItem(self.DME_NAV2_Indicator, (x_DME_txt+135,y_frequencies+20), False)
		
	def draw(self):
		powered = self.XPlaneDataDispatcher.getData(312,0)
		if powered ==1.0 :
			self.setVisible(True)
			DME_found = self.XPlaneDataDispatcher.getData(102,2)
			if DME_found == 0.0:
				self.DME_DIST_Text.setVisible(False)
				self.DME_SPEED_Text.setVisible(False)
				self.DME_TIME_Text.setVisible(False)
			else:
				self.DME_DIST_Text.setVisible(True)
				self.DME_SPEED_Text.setVisible(True)
				self.DME_TIME_Text.setVisible(True)
			
			ACT_DME = self.XPlaneDataDispatcher.getData(102,0)
			
			if ACT_DME == 0.0:
				self.DME_NAV1_Indicator.setVisible(True)
				self.DME_NAV2_Indicator.setVisible(False)
			else:
				self.DME_NAV1_Indicator.setVisible(False)
				self.DME_NAV2_Indicator.setVisible(True)
		else:
			#self.setVisible(False)
			self.DME_BGD.setVisible(False)
			self.DME_NAV1_Indicator.setVisible(False)
			self.DME_NAV2_Indicator.setVisible(False)
			self.DME_DIST_Text.setVisible(False)
			self.DME_SPEED_Text.setVisible(False)
			self.DME_TIME_Text.setVisible(False)
			
			
		super(BK_DME_KN6X,self).draw()

