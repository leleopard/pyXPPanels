import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.graphics import fonts

from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions


class BK_NAVCOMM_KX165A(graphics.Container):
	
	def __init__(self,position, size, batchImageRenderer, texture, NAV_COMM_ID = 1, name = "BK_NAVCOMM_KX165A"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		if NAV_COMM_ID == 1 or NAV_COMM_ID == 2:
			self.NAV_COMM_ID = NAV_COMM_ID
		else:
			self.NAV_COMM_ID = 1
		
		#self.XPlaneDataDispatcher.sendXPCmd("sim/radios/power_com"+str(NAV_COMM_ID)+"_on")
		#self.XPlaneDataDispatcher.sendXPCmd("sim/radios/power_nav"+str(NAV_COMM_ID)+"_on")
		self.layer = 1
		
		
		TXT_FMT_3DIG_PREC2 = '{:06.2f}'
		TXT_FMT_3DIG_PREC3 = '{:07.3f}'
		
		y_frequencies = 29
		#-------------------------------------------------------------------------------------------------
		# Background 
		#-------------------------------------------------------------------------------------------------
		self.BK_NAVCOMM_KX165ABackground = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[574,70],[0,2048-70], "BK_NAVCOMM_KX165ABackground")
		self.BK_NAVCOMM_KX165ABackground.resize((574,70))
		self.addItem(self.BK_NAVCOMM_KX165ABackground, (287,35), False)
		
		# COMM frequency ACTIVE text
		self.COMM_Frequ_ACT_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.COMM_Frequ_ACT_Text.setTextFormat(TXT_FMT_3DIG_PREC3)
		self.COMM_Frequ_ACT_Text.setTextDataSource("sim/cockpit/radios/com"+str(self.NAV_COMM_ID)+"_freq_hz[0]",conversionFunctions.divideby100)
		self.addItem(self.COMM_Frequ_ACT_Text, (9,y_frequencies), False)
		
		# COMM frequency STANDBY text
		self.COMM_Frequ_STBY_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.COMM_Frequ_STBY_Text.setTextFormat(TXT_FMT_3DIG_PREC3)
		self.COMM_Frequ_STBY_Text.setTextDataSource("sim/cockpit/radios/com"+str(self.NAV_COMM_ID)+"_stdby_freq_hz[0]",conversionFunctions.divideby100)
		self.addItem(self.COMM_Frequ_STBY_Text, (145,y_frequencies), False)
		
		# NAV frequency ACTIVE text
		self.NAV_Frequ_ACT_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.NAV_Frequ_ACT_Text.setTextFormat(TXT_FMT_3DIG_PREC2)
		self.NAV_Frequ_ACT_Text.setTextDataSource("sim/cockpit/radios/nav"+str(self.NAV_COMM_ID)+"_freq_hz[0]",conversionFunctions.divideby100)
		self.addItem(self.NAV_Frequ_ACT_Text, (288,y_frequencies), False)
		
		# NAV frequency STANDBY text
		self.NAV_Frequ_STBY_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.NAV_Frequ_STBY_Text.setTextFormat(TXT_FMT_3DIG_PREC2)
		self.NAV_Frequ_STBY_Text.setTextDataSource("sim/cockpit/radios/nav"+str(self.NAV_COMM_ID)+"_stdby_freq_hz[0]",conversionFunctions.divideby100)
		self.addItem(self.NAV_Frequ_STBY_Text, (408,y_frequencies), False)
		
		
	def draw(self):
		powered = 0.0
		if self.NAV_COMM_ID == 1:
			powered = XPlaneUDPServer.pyXPUDPServer.getData("sim/cockpit2/radios/actuators/com1_power[0]")
		elif self.NAV_COMM_ID == 2:
			powered = XPlaneUDPServer.pyXPUDPServer.getData("sim/cockpit2/radios/actuators/com2_power[0]")
		
		if powered == 1.0:
			self.BK_NAVCOMM_KX165ABackground.setVisible(True)
			self.COMM_Frequ_ACT_Text.setVisible(True)
			self.COMM_Frequ_STBY_Text.setVisible(True)
			self.NAV_Frequ_ACT_Text.setVisible(True)
			self.NAV_Frequ_STBY_Text.setVisible(True)
		else:
			self.BK_NAVCOMM_KX165ABackground.setVisible(False)
			self.COMM_Frequ_ACT_Text.setVisible(False)
			self.COMM_Frequ_STBY_Text.setVisible(False)
			self.NAV_Frequ_ACT_Text.setVisible(False)
			self.NAV_Frequ_STBY_Text.setVisible(False)
			
			
		super(BK_NAVCOMM_KX165A,self).draw()

