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
		self.XPlaneDataDispatcher.requestXPDref(314, "sim/cockpit2/radios/actuators/adf1_power[0]")
		self.XPlaneDataDispatcher.requestXPDref(315, "sim/time/total_flight_time_sec[0]")
		
		self.XPlaneDataDispatcher.registerXPCmdCallback(self.XPCmdCallback)
		
		self.layer = 1
		
		TXT_FMT_3DIG_PREC2 = '{:06.2f}'
		TXT_FMT_3DIG_PREC3 = '{:07.3f}'
		
		x_ADF_actFrequ 		= 81
		x_ADF_sbyFrequ 		= 244
		ydelta_ind_bottom 	= 5
		ydelta_ind_top 		= 17
		y_frequencies 		= -18
		
		#-------------------------------------------------------------------------------------------------
		# Background 
		#-------------------------------------------------------------------------------------------------
		self.ADF_BGD = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[399,68],[0,2048-186], "ADF_BGD")
		self.ADF_BGD.resize((399,68))
		self.addItem(self.ADF_BGD, (199.5,0), False)
		
		# ADF Active Frequency text
		self.ADF_ACT_FREQU_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.ADF_ACT_FREQU_Text.setTextFormat('{:> 5.0f}')
		self.ADF_ACT_FREQU_Text.setTextDataSource(self.XPlaneDataDispatcher,(101,0))
		self.addItem(self.ADF_ACT_FREQU_Text, (x_ADF_actFrequ,y_frequencies), False)
		
		# ADF standby Frequency text
		self.ADF_SBY_FREQU_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.ADF_SBY_FREQU_Text.setTextFormat('{:> 5.0f}')
		self.ADF_SBY_FREQU_Text.setTextDataSource(self.XPlaneDataDispatcher,(313,0))
		self.addItem(self.ADF_SBY_FREQU_Text, (x_ADF_sbyFrequ,y_frequencies), False)
		
		# ADF flight timer minutes text
		self.ADF_FLT_TMR_MNS_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.ADF_FLT_TMR_MNS_Text.setTextFormat('{::>3.0f}')
		self.ADF_FLT_TMR_MNS_Text.setTextDataSource(self.XPlaneDataDispatcher,(315,0),conversionFunctions.returnMinutes)
		self.addItem(self.ADF_FLT_TMR_MNS_Text, (x_ADF_sbyFrequ+200,y_frequencies), False)
		
		# ADF flight timer hours text
		self.ADF_FLT_TMR_HRS_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.ADF_FLT_TMR_HRS_Text.setTextFormat('{:>02.0f}')
		self.ADF_FLT_TMR_HRS_Text.setTextDataSource(self.XPlaneDataDispatcher,(315,0),conversionFunctions.returnHours)
		self.addItem(self.ADF_FLT_TMR_HRS_Text, (x_ADF_sbyFrequ+165,y_frequencies), False)
		
		# ADF ANT indicator
		self.ADF_ANT_Indicator = graphics.TextField(fonts.VERA_VSMALL_BOLD_ORANGE)
		self.ADF_ANT_Indicator.setText('ANT')
		self.addItem(self.ADF_ANT_Indicator, (x_ADF_actFrequ-46,y_frequencies+ydelta_ind_top), False)
		
		# ADF ADF indicator
		self.ADF_ADF_Indicator = graphics.TextField(fonts.VERA_VSMALL_BOLD_ORANGE)
		self.ADF_ADF_Indicator.setText('ADF')
		self.addItem(self.ADF_ADF_Indicator, (x_ADF_actFrequ-46,y_frequencies+ydelta_ind_bottom), False)
		
		# ADF FRQ indicator
		self.ADF_FRQ_Indicator = graphics.TextField(fonts.VERA_VSMALL_BOLD_ORANGE)
		self.ADF_FRQ_Indicator.setText('FRQ')
		self.addItem(self.ADF_FRQ_Indicator, (x_ADF_actFrequ+124,y_frequencies+ydelta_ind_bottom), False)
		
		# ADF BFO indicator
		self.ADF_BFO_Indicator = graphics.TextField(fonts.VERA_VSMALL_BOLD_ORANGE)
		self.ADF_BFO_Indicator.setText('BFO')
		self.addItem(self.ADF_BFO_Indicator, (x_ADF_actFrequ+96,y_frequencies+ydelta_ind_top), False)
		
		# ADF FLT indicator
		self.ADF_FLT_Indicator = graphics.TextField(fonts.VERA_VSMALL_BOLD_ORANGE)
		self.ADF_FLT_Indicator.setText('FLT')
		self.addItem(self.ADF_FLT_Indicator, (x_ADF_sbyFrequ+93,y_frequencies+ydelta_ind_top), False)
		
		# ADF ET indicator
		self.ADF_ET_Indicator = graphics.TextField(fonts.VERA_VSMALL_BOLD_ORANGE)
		self.ADF_ET_Indicator.setText(' ET')
		self.addItem(self.ADF_ET_Indicator, (x_ADF_sbyFrequ+93,y_frequencies+ydelta_ind_bottom), False)

	def XPCmdCallback(self, command):
		print "ADF handling command: ", command
		
		
	def draw(self):
		powered = self.XPlaneDataDispatcher.getData(314,0)  # 0 = off, 1 = antenna, 2 = on, 3 = tone, 4 = test
		if powered >= 1.0 :
			self.ADF_BGD.setVisible(True)
			self.ADF_ACT_FREQU_Text.setVisible(True)
			self.ADF_SBY_FREQU_Text.setVisible(True)
			if powered == 1.0 :
				self.ADF_ANT_Indicator.setVisible(True)
				self.ADF_ADF_Indicator.setVisible(False)
				self.ADF_BFO_Indicator.setVisible(False)
			elif powered == 3.0 :
				self.ADF_ANT_Indicator.setVisible(False)
				self.ADF_ADF_Indicator.setVisible(True)
				self.ADF_BFO_Indicator.setVisible(True)
			else:
				self.ADF_ANT_Indicator.setVisible(False)
				self.ADF_ADF_Indicator.setVisible(True)
				self.ADF_BFO_Indicator.setVisible(False)
			
		else:
			self.ADF_BGD.setVisible(False)
			self.ADF_ACT_FREQU_Text.setVisible(False)
			self.ADF_SBY_FREQU_Text.setVisible(False)
			self.ADF_ANT_Indicator.setVisible(False)
			self.ADF_ADF_Indicator.setVisible(False)
			self.ADF_BFO_Indicator.setVisible(False)
		
		super(BK_ADF_KR87,self).draw()

