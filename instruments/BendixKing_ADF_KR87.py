import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.graphics import fonts

from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions


class BK_ADF_KR87(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, name = "BK_ADF_KR87"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.XPlaneDataDispatcher.requestXPDref(313, "sim/cockpit/radios/adf1_stdby_freq_hz[0]")
		
		self.layer = 1
		
		TXT_FMT_3DIG_PREC2 = '{:06.2f}'
		TXT_FMT_3DIG_PREC3 = '{:07.3f}'
		
		x_DME_txt 		= 10
		x_ADF_actFrequ 	= 125
		x_ADF_sbyFrequ 	= 280
		x_DME_time 		= 302
		y_frequencies 	= -18
		#-------------------------------------------------------------------------------------------------
		# Background 
		#-------------------------------------------------------------------------------------------------
		self.ADF_BGD = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[399,68],[0,2048-186], "ADF_BGD")
		self.ADF_BGD.resize((399,68))
		self.addItem(self.ADF_BGD, (199.5,0), False)
		
		# ADF Active Frequency text
		self.ADF_ACT_FREQU_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.ADF_ACT_FREQU_Text.setTextFormat('{:03.0f}')
		self.ADF_ACT_FREQU_Text.setTextDataSource(self.XPlaneDataDispatcher,(101,0))
		self.addItem(self.ADF_ACT_FREQU_Text, (x_ADF_actFrequ,y_frequencies), False)
		
		# ADF standby Frequency text
		self.ADF_SBY_FREQU_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.ADF_SBY_FREQU_Text.setTextFormat('{:03.0f}')
		self.ADF_SBY_FREQU_Text.setTextDataSource(self.XPlaneDataDispatcher,(313,0))
		self.addItem(self.ADF_SBY_FREQU_Text, (x_ADF_sbyFrequ,y_frequencies), False)
		
		'''
		# DME Distance text
		#self.DME_DIST_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.DME_DIST_Text.setTextFormat('{:05.1f}')
		self.DME_DIST_Text.setTextDataSource(self.XPlaneDataDispatcher,(102,3))
		self.addItem(self.DME_DIST_Text, (x_DME_txt,y_frequencies), False)
		
		
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
		'''
		
	def draw(self):
		'''powered = self.XPlaneDataDispatcher.getData(312,0)
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
			self.DME_BGD.setVisible(False)
			self.DME_NAV1_Indicator.setVisible(False)
			self.DME_NAV2_Indicator.setVisible(False)
			self.DME_DIST_Text.setVisible(False)
			self.DME_SPEED_Text.setVisible(False)
			self.DME_TIME_Text.setVisible(False)
			
		'''
		super(BK_ADF_KR87,self).draw()

