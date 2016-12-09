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
		self.XPlaneDataDispatcher.requestXPDref(316, "sim/cockpit2/clock_timer/elapsed_time_minutes[0]")
		self.XPlaneDataDispatcher.requestXPDref(317, "sim/cockpit2/clock_timer/elapsed_time_seconds[0]")
		
		self.XPlaneDataDispatcher.registerXPCmdCallback(self.XPCmdCallback)
		
		self.layer = 1
		
		self.timer_mode = 0 #// 0 = inactive, 1 = flight time, 2 = elapsed time
		
		x_ADF_actFrequ 		= 105
		x_ADF_sbyFrequ 		= 285
		x_ADF_ANT_indicators = 45
		x_BFO_indicator 	= 177
		x_FLT_ET_indicators = 355
		x_time_left			= x_ADF_sbyFrequ - 33
		x_time_right		= x_time_left + 55
		ydelta_ind_bottom 	= -3
		ydelta_ind_top 		= 19
		y_frequencies 		= -19
		
		#-------------------------------------------------------------------------------------------------
		# Background 
		#-------------------------------------------------------------------------------------------------
		self.ADF_BGD = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[399,68],[0,2048-186], "ADF_BGD")
		self.ADF_BGD.resize((399,68))
		self.addItem(self.ADF_BGD, (199.5,0), False)
		
		#-------------------------------------------------------------------------------------------------
		# Frequency labels
		#-------------------------------------------------------------------------------------------------
		# ADF Active Frequency text
		self.ADF_ACT_FREQU_Text = graphics.TextField(fonts.DIGITAL_ITAL_XXLARGE_ORANGE)
		self.ADF_ACT_FREQU_Text.setTextFormat('{:0>3.0f}')
		self.ADF_ACT_FREQU_Text.setTextDataSource(self.XPlaneDataDispatcher,(101,0))
		self.addItem(self.ADF_ACT_FREQU_Text, (x_ADF_actFrequ,y_frequencies), False)
		
		# ADF standby Frequency text
		self.ADF_SBY_FREQU_Text = graphics.TextField(fonts.DIGITAL_ITAL_XXLARGE_ORANGE)
		self.ADF_SBY_FREQU_Text.setTextFormat('{:0>3.0f}')
		self.ADF_SBY_FREQU_Text.setTextDataSource(self.XPlaneDataDispatcher,(313,0))
		self.addItem(self.ADF_SBY_FREQU_Text, (x_ADF_sbyFrequ,y_frequencies), False)
		
		#-------------------------------------------------------------------------------------------------
		# Timer labels
		#-------------------------------------------------------------------------------------------------
		# ADF flight timer hours text
		self.ADF_FLT_TMR_HRS_Text = graphics.TextField(fonts.DIGITAL_ITAL_XXLARGE_ORANGE)
		self.ADF_FLT_TMR_HRS_Text.setTextFormat('{:0>2.0f}:')
		self.ADF_FLT_TMR_HRS_Text.setTextDataSource(self.XPlaneDataDispatcher,(315,0),conversionFunctions.returnHours)
		self.addItem(self.ADF_FLT_TMR_HRS_Text, (x_time_left,y_frequencies), False)
		
		# ADF flight timer minutes text
		self.ADF_FLT_TMR_MNS_Text = graphics.TextField(fonts.DIGITAL_ITAL_XXLARGE_ORANGE)
		self.ADF_FLT_TMR_MNS_Text.setTextFormat('{:0>2.0f}')
		self.ADF_FLT_TMR_MNS_Text.setTextDataSource(self.XPlaneDataDispatcher,(315,0),conversionFunctions.returnMinutes)
		self.addItem(self.ADF_FLT_TMR_MNS_Text, (x_time_right,y_frequencies), False)
				
		# ADF elapsed timer minutes text
		self.ADF_ET_TMR_MNS_Text = graphics.TextField(fonts.DIGITAL_ITAL_XXLARGE_ORANGE)
		self.ADF_ET_TMR_MNS_Text.setTextFormat('{:0>2.0f}:')  
		self.ADF_ET_TMR_MNS_Text.setTextDataSource(self.XPlaneDataDispatcher,(316,0))
		self.addItem(self.ADF_ET_TMR_MNS_Text, (x_time_left,y_frequencies), False)
		
		# ADF elapsed timer seconds text
		self.ADF_ET_TMR_SECS_Text = graphics.TextField(fonts.DIGITAL_ITAL_XXLARGE_ORANGE)
		self.ADF_ET_TMR_SECS_Text.setTextFormat('{:0>2.0f}')
		self.ADF_ET_TMR_SECS_Text.setTextDataSource(self.XPlaneDataDispatcher,(317,0))
		self.addItem(self.ADF_ET_TMR_SECS_Text, (x_time_right,y_frequencies), False)
		
		#-------------------------------------------------------------------------------------------------
		# Indicators
		#-------------------------------------------------------------------------------------------------
		# ADF ANT indicator
		self.ADF_ANT_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.ADF_ANT_Indicator.setText('ANT')
		self.addItem(self.ADF_ANT_Indicator, (x_ADF_ANT_indicators,y_frequencies+ydelta_ind_top), False)
		
		# ADF ADF indicator
		self.ADF_ADF_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.ADF_ADF_Indicator.setText('ADF')
		self.addItem(self.ADF_ADF_Indicator, (x_ADF_ANT_indicators,y_frequencies+ydelta_ind_bottom), False)
		
		#-------
		# ADF BFO indicator
		self.ADF_BFO_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.ADF_BFO_Indicator.setText('BFO')
		self.addItem(self.ADF_BFO_Indicator, (x_BFO_indicator,y_frequencies+ydelta_ind_top), False)
		
		# ADF FRQ indicator
		self.ADF_FRQ_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.ADF_FRQ_Indicator.setText('FRQ')
		self.addItem(self.ADF_FRQ_Indicator, (x_BFO_indicator+ 31,y_frequencies+ydelta_ind_bottom), False)
		
		#-------
		# ADF FLT indicator
		self.ADF_FLT_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.ADF_FLT_Indicator.setText('FLT')
		self.addItem(self.ADF_FLT_Indicator, (x_FLT_ET_indicators,y_frequencies+ydelta_ind_top), False)
		
		# ADF ET indicator
		self.ADF_ET_Indicator = graphics.TextField(fonts.VERA_13PT_BOLD_ORANGE)
		self.ADF_ET_Indicator.setText(' ET')
		self.addItem(self.ADF_ET_Indicator, (x_FLT_ET_indicators,y_frequencies+ydelta_ind_bottom), False)

	def XPCmdCallback(self, command):
		print "ADF handling command: ", command
		self.timer_mode
		# // 0 = inactive, 1 = flight time, 2 = elapsed time
		if (command == "ST/time/timer_mode_0"): self.timer_mode = 0
		if (command == "ST/time/timer_mode_1"): self.timer_mode = 1
		if (command == "ST/time/timer_mode_2"): self.timer_mode = 2
		
		
	def draw(self):
		powered = self.XPlaneDataDispatcher.getData(314,0)  # 0 = off, 1 = antenna, 2 = on, 3 = tone, 4 = test
		if powered >= 1.0 :
			self.ADF_BGD.setVisible(True)
			self.ADF_ACT_FREQU_Text.setVisible(True)
			if self.timer_mode == 0: #// 0 = inactive, 1 = flight time, 2 = elapsed time
				self.ADF_SBY_FREQU_Text.setVisible(True)
				self.ADF_FRQ_Indicator.setVisible(True)
				self.ADF_FLT_Indicator.setVisible(False)
				self.ADF_ET_Indicator.setVisible(False)
				self.ADF_FLT_TMR_MNS_Text.setVisible(False)
				self.ADF_FLT_TMR_HRS_Text.setVisible(False)
				self.ADF_ET_TMR_MNS_Text.setVisible(False)
				self.ADF_ET_TMR_SECS_Text.setVisible(False)
				
			elif self.timer_mode == 1:
				self.ADF_SBY_FREQU_Text.setVisible(False)
				self.ADF_FRQ_Indicator.setVisible(False)
				self.ADF_FLT_Indicator.setVisible(True)
				self.ADF_ET_Indicator.setVisible(False)
				self.ADF_FLT_TMR_MNS_Text.setVisible(True)
				self.ADF_FLT_TMR_HRS_Text.setVisible(True)
				self.ADF_ET_TMR_MNS_Text.setVisible(False)
				self.ADF_ET_TMR_SECS_Text.setVisible(False)
				
			elif self.timer_mode == 2:
				self.ADF_SBY_FREQU_Text.setVisible(False)
				self.ADF_FRQ_Indicator.setVisible(False)
				self.ADF_FLT_Indicator.setVisible(False)
				self.ADF_ET_Indicator.setVisible(True)
				self.ADF_FLT_TMR_MNS_Text.setVisible(False)
				self.ADF_FLT_TMR_HRS_Text.setVisible(False)
				self.ADF_ET_TMR_MNS_Text.setVisible(True)
				self.ADF_ET_TMR_SECS_Text.setVisible(True)
				
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
			self.ADF_FRQ_Indicator.setVisible(False)
			self.ADF_BFO_Indicator.setVisible(False)
			self.ADF_FLT_Indicator.setVisible(False)
			self.ADF_ET_Indicator.setVisible(False)
			self.ADF_FLT_TMR_MNS_Text.setVisible(False)
			self.ADF_FLT_TMR_HRS_Text.setVisible(False)
			self.ADF_ET_TMR_MNS_Text.setVisible(False)
			self.ADF_ET_TMR_SECS_Text.setVisible(False)
				
				
		super(BK_ADF_KR87,self).draw()

