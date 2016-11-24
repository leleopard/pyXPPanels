import XPlaneUDPServer
import XPinstrument
import conversionFunctions
import logging
import G1000_fonts

class G1000AirspeedIndicator(XPinstrument.STinstrument):
	XPlaneDataDispatcher = None
	VNE = 9999
	
	def __init__(self,position, size, XPlaneDataDispatcher,VNE,VSO,VSI,VFE,VNO, Vx, Vy, Vr, Vg,name = "G1000AirspeedIndicator"):
		XPinstrument.STinstrument.__init__(self,position, size,name)
		
		self.testMode = False
		
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.VNE = VNE # never exceed speed
		self.VSO = VSO # stall speed, flaps extended, power off
		self.VSI = VSI # stall speed, flaps retracted, power off
		self.VFE = VFE # max flaps extended speed
		self.VNO = VNO # max structural cruising speed (yellow)
		
		self.Vx = Vx # best angle of climb
		self.Vy = Vy # bext climb speed
		self.Vr = Vr # take off speed
		self.Vg = Vg # Best glide speed
		
		self.maxdisplayedspeed = 1000

		#-------------------------------------------------------------------------------------------------
		# Background 
		#-------------------------------------------------------------------------------------------------
		
		self.G1000AirspeedBackground = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_background")
		self.addImage(self.G1000AirspeedBackground, (0,0), False)
		
		#-------------------------------------------------------------------------------------------------
		# Ref speed indicators
		#-------------------------------------------------------------------------------------------------
#Vx = 62 # best angle of climb
#Vy = 74 # bext climb speed
#Vr = 55 # take off speed
#Vg = 68 # Best glide speed
		self.opSpeedTapesClippingPanel = XPinstrument.ClippingPanel([0,0],[100,276],"altiClippingPanel")
		self.addImage(self.opSpeedTapesClippingPanel, (0,17), False)
		
		xref = 139
		initial_pos = xref+self.Vx*46/10
		self.G1000AirspeedVxIndicator = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_VREF_Vx",(0,0),None,None, self.testMode)
		self.G1000AirspeedVxIndicator.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[self.maxdisplayedspeed,-self.maxdisplayedspeed*46/10]])
		self.opSpeedTapesClippingPanel.addImage(self.G1000AirspeedVxIndicator, (73,initial_pos), False)
		
		initial_pos = xref+self.Vy*46/10
		self.G1000AirspeedVyIndicator = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_VREF_Vy",(0,0),None,None, self.testMode)
		self.G1000AirspeedVyIndicator.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[self.maxdisplayedspeed,-self.maxdisplayedspeed*46/10]])
		self.opSpeedTapesClippingPanel.addImage(self.G1000AirspeedVyIndicator, (73,initial_pos), False)
		
		initial_pos = xref+self.Vr*46/10
		self.G1000AirspeedVrIndicator = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_VREF_Vr",(0,0),None,None, self.testMode)
		self.G1000AirspeedVrIndicator.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[self.maxdisplayedspeed,-self.maxdisplayedspeed*46/10]])
		self.opSpeedTapesClippingPanel.addImage(self.G1000AirspeedVrIndicator, (73,initial_pos), False)
	
		initial_pos = xref+self.Vg*46/10
		self.G1000AirspeedVgIndicator = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_VREF_Vg",(0,0),None,None, self.testMode)
		self.G1000AirspeedVgIndicator.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[self.maxdisplayedspeed,-self.maxdisplayedspeed*46/10]])
		self.opSpeedTapesClippingPanel.addImage(self.G1000AirspeedVgIndicator, (73,initial_pos), False)
		
		#-------------------------------------------------------------------------------------------------
		# Operating speed tapes
		#-------------------------------------------------------------------------------------------------

		VStalltape_height_px = (self.VSO)*46 / 10
		VStalltape_initial_pos = 147
		
		self.G1000AirspeedStallTape = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_Stalltape",(0,0),[7,VStalltape_height_px],[0,0], self.testMode)
		self.G1000AirspeedStallTape.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[self.maxdisplayedspeed,-self.maxdisplayedspeed*46/10]])
		self.opSpeedTapesClippingPanel.addImage(self.G1000AirspeedStallTape, (63,VStalltape_initial_pos), False)	
		
		
		VNEtape_height_px = (self.maxdisplayedspeed - self.VNE)*46 / 10
		VNEtape_initial_pos = VStalltape_initial_pos+self.VNE*46/10
		
		self.G1000AirspeedNETape = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_NEtape",(0,0),[7,VNEtape_height_px],[0,0], self.testMode)
		self.G1000AirspeedNETape.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[self.maxdisplayedspeed,-self.maxdisplayedspeed*46/10]])
		self.opSpeedTapesClippingPanel.addImage(self.G1000AirspeedNETape, (63,VNEtape_initial_pos), False)	
		
		VSOtape_height_px = (self.VSI - self.VSO)*46 / 10
		VSOtape_initial_pos = VStalltape_initial_pos+self.VSO*46/10
		
		self.G1000AirspeedVSOTape = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_flapstape",(0,0),[7,VSOtape_height_px],[0,0], self.testMode)
		self.G1000AirspeedVSOTape.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[self.maxdisplayedspeed,-self.maxdisplayedspeed*46/10]])
		self.opSpeedTapesClippingPanel.addImage(self.G1000AirspeedVSOTape, (63,VSOtape_initial_pos), False)
		
		VFEtape_height_px = (self.VFE - self.VSI)*46 / 10
		VFEtape_initial_pos = VStalltape_initial_pos+self.VSI*46/10
		
		self.G1000AirspeedVFETape = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_VFEtape",(0,0),[7,VFEtape_height_px],[0,0], self.testMode)
		self.G1000AirspeedVFETape.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[self.maxdisplayedspeed,-self.maxdisplayedspeed*46/10]])
		self.opSpeedTapesClippingPanel.addImage(self.G1000AirspeedVFETape, (63,VFEtape_initial_pos), False)	
		
		
		Vnormaltape_height_px = (self.VNO - self.VFE)*46 / 10
		Vnormaltape_initial_pos = VStalltape_initial_pos+self.VFE*46/10
		
		self.G1000AirspeedVnormalTape = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_Vnormal_tape",(0,0),[7,Vnormaltape_height_px],[0,0], self.testMode)
		self.G1000AirspeedVnormalTape.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[self.maxdisplayedspeed,-self.maxdisplayedspeed*46/10]])
		self.opSpeedTapesClippingPanel.addImage(self.G1000AirspeedVnormalTape, (63,Vnormaltape_initial_pos), False)
		
		VNOtape_height_px = (self.VNE - self.VNO)*46 / 10
		VNOtape_initial_pos = VStalltape_initial_pos+self.VNO*46/10
		
		self.G1000AirspeedVNOTape = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_VNOtape",(0,0),[7,VNOtape_height_px],[0,0], self.testMode)
		self.G1000AirspeedVNOTape.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[self.maxdisplayedspeed,-self.maxdisplayedspeed*46/10]])
		self.opSpeedTapesClippingPanel.addImage(self.G1000AirspeedVNOTape, (63,VNOtape_initial_pos), False)
		
		
		
		#-------------------------------------------------------------------------------------------------
		# Airspeed tape 
		#-------------------------------------------------------------------------------------------------
		self.G1000AirspeedTape = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_tape",(0,0),[16,276],[204,24.5], self.testMode)
		self.G1000AirspeedTape.setTranslateTexture(True)
		self.G1000AirspeedTape.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[100,460]],conversionFunctions.returnSpeed100sValue)
		self.addImage(self.G1000AirspeedTape, (54,25), False)	
		
		self.G1000Airspeed10sTape = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_tape",(0,0),[25,276],[149,24.5], self.testMode)
		self.G1000Airspeed10sTape.setTranslateTexture(True)
		self.G1000Airspeed10sTape.setAddTranslation((26,0))
		self.G1000Airspeed10sTape.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[100,460]],conversionFunctions.returnSpeed100sValue)
		self.addImage(self.G1000Airspeed10sTape, (26,25), False)	
		
		self.G1000AirspeedTape100s = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_tape",(0,0),[12,276],[3,24.5], self.testMode)
		self.G1000AirspeedTape100s.setTranslateTexture(True)
		self.G1000AirspeedTape100s.setAddTranslation((0,0))
		self.G1000AirspeedTape100s.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[100,460]],conversionFunctions.returnSpeed100sValue)
		self.addImage(self.G1000AirspeedTape100s, (15,25), False)	
		
		#-------------------------------------------------------------------------------------------------
		# Airspeed select bug 
		#-------------------------------------------------------------------------------------------------
		self.airSpeedBugClippingPanel = XPinstrument.ClippingPanel([0,0],[100,276],"altiClippingPanel")
		self.addImage(self.airSpeedBugClippingPanel, (0,17), False)
		
		self.airspeedSelectBug = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_airspeedselectbug",(0,0),None,None, self.testMode)
		self.airspeedSelectBug.enableTranslation (self.XPlaneDataDispatcher,(118,0),[ [-30,-30*4.6],[30,30*4.6]],self.returnAirspeedSelectDifference)
		self.airSpeedBugClippingPanel.addImage(self.airspeedSelectBug, (60,125), False)
		
		#-------------------------------------------------------------------------------------------------
		# Selected airspeed box 
		#-------------------------------------------------------------------------------------------------
		self.selectedAirspeedBox = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_selectedairspeedbox",(0,0),None,None, self.testMode)
		self.addImage(self.selectedAirspeedBox, (1,302),False)
		
		self.airspeedSelectLabel = XPinstrument.TextField(G1000_fonts.FONT_MED_TURQUOISE)
		self.airspeedSelectLabel.setTextFormat('{: >3.0f}')
		self.airspeedSelectLabel.setTextDataSource(self.XPlaneDataDispatcher,(118,0))
		self.addImage(self.airspeedSelectLabel, (21,304), False)
		
		self.airspeedSelectUnitLabel = XPinstrument.TextField(G1000_fonts.FONT_VSMALL_TURQUOISE)
		self.airspeedSelectUnitLabel.setText("KT")
		self.addImage(self.airspeedSelectUnitLabel, (49,305.5), False)
		
		#-------------------------------------------------------------------------------------------------
		# IAS box 
		#-------------------------------------------------------------------------------------------------
		self.G1000AirspeedSpeedbox = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_speedbox")
		self.addImage(self.G1000AirspeedSpeedbox, (4,135), False)
		self.G1000AirspeedSpeedboxRed = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_speedbox_red")
		self.addImage(self.G1000AirspeedSpeedboxRed, (4,135), False)
		
		self.IASSpeedLabel = XPinstrument.TextField(G1000_fonts.FONT_LARGE_WHITE)
		self.IASSpeedLabel.setTextFormat('{: >2.0f}')
		self.IASSpeedLabel.setTextDataSource(self.XPlaneDataDispatcher,(3,0),conversionFunctions.returnSpeedLabelValue)
		self.addImage(self.IASSpeedLabel, (22,152), False)

		#def __init__(self, imagename, position=[0,0], cliprect=None, origin=None, testMode=False):
		self.G1000AirspeedNrTape = XPinstrument.InstrumentImage("G1000AirspeedIndicator/G1000_airspeed_nr_tape",(0,0),[17,48],[0,4], self.testMode)
		self.G1000AirspeedNrTape.setTranslateTexture(True)
		self.G1000AirspeedNrTape.enableTranslation (self.XPlaneDataDispatcher,(3,0),[ [0,0],[10,190]],conversionFunctions.returnSpeedTapeValue)
		self.addImage(self.G1000AirspeedNrTape, (43,139), False)	
		
		#-------------------------------------------------------------------------------------------------
		# TAS labels 
		#-------------------------------------------------------------------------------------------------
		self.TASlabel = XPinstrument.TextField(G1000_fonts.FONT_VSMALL_WHITE)
		self.TASlabel.setText("TAS")
		self.addImage(self.TASlabel, (3,5), False)
		self.TASUnitlabel = XPinstrument.TextField(G1000_fonts.FONT_VSMALL_WHITE)
		self.TASUnitlabel.setText("KT")
		self.addImage(self.TASUnitlabel, (55,5), False)
		
		self.TASSpeedLabel = XPinstrument.TextField(G1000_fonts.FONT_SMALL_WHITE)
		self.TASSpeedLabel.setTextFormat('{: >3.0f}')
		self.TASSpeedLabel.setTextDataSource(self.XPlaneDataDispatcher,(3,2))
		self.addImage(self.TASSpeedLabel, (29,5), False)

	def returnAirspeedSelectDifference(self,selectedAirspeed,XPlaneDataDispatcher):
		airspeed = self.XPlaneDataDispatcher.getData(3,0)
		if self.testMode == True:
			return self.testValue
		else: 
			return (selectedAirspeed - airspeed)

	def draw(self):
		
		IAS = self.XPlaneDataDispatcher.getData(3,0)
		if self.testMode == True:
			IAS = self.G1000Airspeed10sTape.testValue
			print "Airspeed indicator: test mode :: Airspeed: ", IAS
			
		if IAS >= self.VNE:
			self.G1000AirspeedSpeedbox.setVisible(False)
			self.G1000AirspeedSpeedboxRed.setVisible(True)
		else:
			self.G1000AirspeedSpeedbox.setVisible(True)
			self.G1000AirspeedSpeedboxRed.setVisible(False)
		
		if IAS > 99:
			self.G1000Airspeed10sTape.setAddTranslation((26,0))
		else:
			self.G1000Airspeed10sTape.setAddTranslation((0,0))
		
		if IAS < 100:
			self.G1000AirspeedTape100s.setAddTranslation((132,0))
		elif IAS <200:
			self.G1000AirspeedTape100s.setAddTranslation((119,0))
		elif IAS <300:
			self.G1000AirspeedTape100s.setAddTranslation((106,0))
		elif IAS <400:
			self.G1000AirspeedTape100s.setAddTranslation((92,0))
		elif IAS <500:
			self.G1000AirspeedTape100s.setAddTranslation((78,0))
		elif IAS <600:
			self.G1000AirspeedTape100s.setAddTranslation((65,0))
		elif IAS <700:
			self.G1000AirspeedTape100s.setAddTranslation((52,0))
		elif IAS <800:
			self.G1000AirspeedTape100s.setAddTranslation((39,0))
		elif IAS <900:
			self.G1000AirspeedTape100s.setAddTranslation((26,0))
		elif IAS <1000:
			self.G1000AirspeedTape100s.setAddTranslation((13,0))
		elif IAS <1100:
			self.G1000AirspeedTape100s.setAddTranslation((0,0))
			
		super(G1000AirspeedIndicator,self).draw()
		