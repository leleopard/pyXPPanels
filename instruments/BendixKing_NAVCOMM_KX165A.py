import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.graphics import fonts

from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions


class BK_NAVCOMM_KX165A(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, NAV_COMM_ID = 1, name = "BK_NAVCOMM_KX165A"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.NAV_COMM_ID = NAV_COMM_ID
		
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		#self.XPlaneDataDispatcher.requestXPDref( 512, "sim/cockpit2/radios/actuators/com1_power")
		#self.XPlaneDataDispatcher.sendXPCmd("sim/radios/power_com"+str(NAV_COMM_ID)+"_on")
		#self.XPlaneDataDispatcher.sendXPCmd("sim/radios/power_nav"+str(NAV_COMM_ID)+"_on")
		self.layer = 1
		
		COMM_ACT_INDEX = 0
		if NAV_COMM_ID == 2:
			COMM_ACT_INDEX = 3
		
		COMM_STDBY_INDEX = 1
		if NAV_COMM_ID == 2:
			COMM_STDBY_INDEX = 4
		
		NAV_ACT_INDEX = 0
		if NAV_COMM_ID == 2:
			NAV_ACT_INDEX = 4
		
		NAV_STDBY_INDEX = 1
		if NAV_COMM_ID == 2:
			NAV_STDBY_INDEX = 5
		
		TXT_FMT_3DIG_PREC2 = '{:06.2f}'
		TXT_FMT_3DIG_PREC3 = '{:07.3f}'
		
		y_frequencies = 27
		#-------------------------------------------------------------------------------------------------
		# Background 
		#-------------------------------------------------------------------------------------------------
		self.BK_NAVCOMM_KX165ABackground = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[574,70],[0,2048-70], "BK_NAVCOMM_KX165ABackground")
		self.BK_NAVCOMM_KX165ABackground.resize((574,70))
		self.addItem(self.BK_NAVCOMM_KX165ABackground, (287,35), False)
		
		# COMM frequency ACTIVE text
		self.COMM_Frequ_ACT_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.COMM_Frequ_ACT_Text.setTextFormat(TXT_FMT_3DIG_PREC3)
		self.COMM_Frequ_ACT_Text.setTextDataSource(self.XPlaneDataDispatcher,(96,COMM_ACT_INDEX),conversionFunctions.divideby100)
		self.addItem(self.COMM_Frequ_ACT_Text, (9,y_frequencies), False)
		
		# COMM frequency STANDBY text
		self.COMM_Frequ_STBY_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.COMM_Frequ_STBY_Text.setTextFormat(TXT_FMT_3DIG_PREC3)
		self.COMM_Frequ_STBY_Text.setTextDataSource(self.XPlaneDataDispatcher,(96,COMM_STDBY_INDEX),conversionFunctions.divideby100)
		self.addItem(self.COMM_Frequ_STBY_Text, (145,y_frequencies), False)
		
		# NAV frequency ACTIVE text
		self.NAV_Frequ_ACT_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.NAV_Frequ_ACT_Text.setTextFormat(TXT_FMT_3DIG_PREC2)
		self.NAV_Frequ_ACT_Text.setTextDataSource(self.XPlaneDataDispatcher,(97,NAV_ACT_INDEX),conversionFunctions.divideby100)
		self.addItem(self.NAV_Frequ_ACT_Text, (288,y_frequencies), False)
		
		# NAV frequency STANDBY text
		self.NAV_Frequ_STBY_Text = graphics.TextField(fonts.DIGITAL_ITAL_MED_ORANGE)
		self.NAV_Frequ_STBY_Text.setTextFormat(TXT_FMT_3DIG_PREC2)
		self.NAV_Frequ_STBY_Text.setTextDataSource(self.XPlaneDataDispatcher,(97,NAV_STDBY_INDEX),conversionFunctions.divideby100)
		self.addItem(self.NAV_Frequ_STBY_Text, (408,y_frequencies), False)
		
		
	def draw(self):
		powered = 0.0
		if self.NAV_COMM_ID == 1:
			powered = self.XPlaneDataDispatcher.getData(310,0)
		elif self.NAV_COMM_ID == 2:
			powered = self.XPlaneDataDispatcher.getData(311,0)
		
		if powered == 1.0:
			self.COMM_Frequ_ACT_Text.setVisible(True)
			self.COMM_Frequ_STBY_Text.setVisible(True)
			self.NAV_Frequ_ACT_Text.setVisible(True)
			self.NAV_Frequ_STBY_Text.setVisible(True)
		else:
			self.COMM_Frequ_ACT_Text.setVisible(False)
			self.COMM_Frequ_STBY_Text.setVisible(False)
			self.NAV_Frequ_ACT_Text.setVisible(False)
			self.NAV_Frequ_STBY_Text.setVisible(False)
			
			
		super(BK_NAVCOMM_KX165A,self).draw()

