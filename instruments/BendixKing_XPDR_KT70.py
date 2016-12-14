import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.graphics import fonts

from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions


class BK_XPDR_KT70(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, name = "BK_XPDR_KT70"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.XPlaneDataDispatcher.requestXPDref(318, "sim/cockpit2/radios/actuators/transponder_code[0]")
		self.XPlaneDataDispatcher.requestXPDref(319, "sim/cockpit2/radios/actuators/transponder_mode[0]")
		self.XPlaneDataDispatcher.requestXPDref(320, "sim/cockpit/radios/transponder_light[0]")
		
		self.layer = 1
		
		x_flight_level = 104
		x_xpdr_code = x_flight_level+195
		x_alt_ind = 197
		
		ydelta_ind_bottom 	= -3
		ydelta_ind_top 		= 19
		y_frequencies 		= -20
		#-------------------------------------------------------------------------------------------------
		# Background 
		#-------------------------------------------------------------------------------------------------
		self.XPDR_BGD = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[382,65],[0,2048-251], "XPDR_BGD")
		self.XPDR_BGD.resize((399,68))
		self.addItem(self.XPDR_BGD, (199.5,0), False)
		
		#-------------------------------------------------------------------------------------------------
		# Flight level label
		#-------------------------------------------------------------------------------------------------
		self.XPDR_FL_Text = graphics.TextField(fonts.DIGITAL_ITAL_XXLARGE_ORANGE)
		self.XPDR_FL_Text.setTextFormat('{:0= 4.0f}')
		self.XPDR_FL_Text.setTextDataSource(self.XPlaneDataDispatcher,(20,2), conversionFunctions.returnAltitude100sfeet)
		self.addItem(self.XPDR_FL_Text, (x_flight_level,y_frequencies), False)
		
		#-------------------------------------------------------------------------------------------------
		# Transponder code label
		#-------------------------------------------------------------------------------------------------
		self.XPDR_CODE_Text = graphics.TextField(fonts.DIGITAL_ITAL_XXLARGE_ORANGE)
		self.XPDR_CODE_Text.setTextFormat('{:0>4.0f}')
		self.XPDR_CODE_Text.setTextDataSource(self.XPlaneDataDispatcher,(318,0))
		self.addItem(self.XPDR_CODE_Text, (x_xpdr_code,y_frequencies), False)
		
		#-------------------------------------------------------------------------------------------------
		# Indicators
		#-------------------------------------------------------------------------------------------------
		# XPDR ALT indicator
		self.XPDR_ALT_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.XPDR_ALT_Indicator.setText('ALT')
		self.addItem(self.XPDR_ALT_Indicator, (x_alt_ind,y_frequencies+ydelta_ind_top), False)
		
		# XPDR ON indicator
		self.XPDR_ON_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.XPDR_ON_Indicator.setText('ON')
		self.addItem(self.XPDR_ON_Indicator, (x_alt_ind+37,y_frequencies+ydelta_ind_top), False)
		
		# XPDR GND indicator
		self.XPDR_GND_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.XPDR_GND_Indicator.setText('GND')
		self.addItem(self.XPDR_GND_Indicator, (x_alt_ind,y_frequencies+ydelta_ind_bottom), False)
		
		# XPDR SBY indicator
		self.XPDR_SBY_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.XPDR_SBY_Indicator.setText('SBY')
		self.addItem(self.XPDR_SBY_Indicator, (x_alt_ind+37,y_frequencies+ydelta_ind_bottom), False)
		
		# XPDR FL indicator
		self.XPDR_FL_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.XPDR_FL_Indicator.setText('FL')
		self.addItem(self.XPDR_FL_Indicator, (x_flight_level-26,y_frequencies+ydelta_ind_bottom), False)
		
		# XPDR R indicator
		self.XPDR_R_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.XPDR_R_Indicator.setText(' R')
		self.addItem(self.XPDR_R_Indicator, (x_alt_ind+72,y_frequencies+ydelta_ind_top), False)


	def draw(self):
		transp_mode = self.XPlaneDataDispatcher.getData(319,0) # Transponder mode (off=0,stdby=1,on=2,test=3) ALT=4, GND=5
		transp_light = self.XPlaneDataDispatcher.getData(320,0) # 1.0 = light lit, 0.0 not
		if transp_mode >= 1.0:
			if transp_mode != 3.0 : # if we are not in test mode, reset the flight level and code text fields to follow XP values. 
				self.XPDR_FL_Text.setTextDataSource(self.XPlaneDataDispatcher,(20,2), conversionFunctions.returnAltitude100sfeet)
				self.XPDR_CODE_Text.setTextDataSource(self.XPlaneDataDispatcher,(318,0))
			
			if transp_mode == 1.0 : # Standby. 
				self.XPDR_R_Indicator.setVisible(False)
				self.XPDR_BGD.setVisible(True)
				self.XPDR_FL_Text.setVisible(False)
				self.XPDR_CODE_Text.setVisible(True)
				self.XPDR_ALT_Indicator.setVisible(False)
				self.XPDR_ON_Indicator.setVisible(False)
				self.XPDR_GND_Indicator.setVisible(False)
				self.XPDR_SBY_Indicator.setVisible(True)
				self.XPDR_FL_Indicator.setVisible(False)
			
			if transp_mode == 2.0 : # ON. 
				if transp_light == 0.0 :
					self.XPDR_R_Indicator.setVisible(False)
				else: 
					self.XPDR_R_Indicator.setVisible(True)
				self.XPDR_BGD.setVisible(True)
				self.XPDR_FL_Text.setVisible(False)
				self.XPDR_CODE_Text.setVisible(True)
				self.XPDR_ALT_Indicator.setVisible(False)
				self.XPDR_ON_Indicator.setVisible(True)
				self.XPDR_GND_Indicator.setVisible(False)
				self.XPDR_SBY_Indicator.setVisible(False)
				self.XPDR_FL_Indicator.setVisible(False)
			
			if transp_mode == 3.0 : # TEST 
				self.XPDR_R_Indicator.setVisible(True)
				self.XPDR_BGD.setVisible(True)
				self.XPDR_FL_Text.setVisible(True)
				self.XPDR_FL_Text.setTextDataSource(None, None) # this is to avoid XPlane overriding the test value we will set on next line
				self.XPDR_FL_Text.setText('-888')
				
				self.XPDR_CODE_Text.setVisible(True)
				self.XPDR_CODE_Text.setTextDataSource(None, None) # this is to avoid XPlane overriding the test value we will set on next line
				self.XPDR_CODE_Text.setText('8888')
				
				self.XPDR_ALT_Indicator.setVisible(True)
				self.XPDR_ON_Indicator.setVisible(True)
				self.XPDR_GND_Indicator.setVisible(True)
				self.XPDR_SBY_Indicator.setVisible(True)
				self.XPDR_FL_Indicator.setVisible(True)
			
			if transp_mode == 4.0 : # we are in ALT mode 
				
				if transp_light == 0.0 :
					self.XPDR_R_Indicator.setVisible(False)
				else: 
					self.XPDR_R_Indicator.setVisible(True)
				
				self.XPDR_BGD.setVisible(True)
				self.XPDR_FL_Text.setVisible(True)
				self.XPDR_CODE_Text.setVisible(True)
				self.XPDR_ALT_Indicator.setVisible(True)
				self.XPDR_ON_Indicator.setVisible(True)
				self.XPDR_GND_Indicator.setVisible(False)
				self.XPDR_SBY_Indicator.setVisible(False)
				self.XPDR_FL_Indicator.setVisible(True)
			
			if transp_mode == 5.0 : # we are in GND mode 
				
				if transp_light == 0.0 :
					self.XPDR_R_Indicator.setVisible(False)
				else: 
					self.XPDR_R_Indicator.setVisible(True)
				
				self.XPDR_BGD.setVisible(True)
				self.XPDR_FL_Text.setVisible(True)
				self.XPDR_CODE_Text.setVisible(True)
				self.XPDR_ALT_Indicator.setVisible(False)
				self.XPDR_ON_Indicator.setVisible(False)
				self.XPDR_GND_Indicator.setVisible(True)
				self.XPDR_SBY_Indicator.setVisible(False)
				self.XPDR_FL_Indicator.setVisible(True)
			
		else:
			self.XPDR_BGD.setVisible(False)
			self.XPDR_FL_Text.setVisible(False)
			self.XPDR_CODE_Text.setVisible(False)
			self.XPDR_ALT_Indicator.setVisible(False)
			self.XPDR_ON_Indicator.setVisible(False)
			self.XPDR_GND_Indicator.setVisible(False)
			self.XPDR_SBY_Indicator.setVisible(False)
			self.XPDR_FL_Indicator.setVisible(False)
			self.XPDR_R_Indicator.setVisible(False)
		
		super(BK_XPDR_KT70,self).draw()

