import logging
import decimal
D = decimal.Decimal

from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3 as graphics
from lib.graphics import fonts

from lib.network import XPlaneUDPServer
from lib.general import conversionFunctions


class G1000Altimeter(graphics.Container):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, jetVSI = False, name = "G1000Altimeter"):
		graphics.Container.__init__(self,position, size, name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		self.jetVSI = jetVSI
		self.maxVVI = 2000
		self.layer = 1
		
		#-------------------------------------------------------------------------------------------------
		# Background 
		#-------------------------------------------------------------------------------------------------
		if self.jetVSI == False:
			self.G1000AltimeterBackground = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[125,325],[643,2048-1699], "G1000AltimeterBackground")
		else:
			self.G1000AltimeterBackground = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[125,325],[512,2048-1699], "G1000AltimeterBackground")
		self.maxVVI = 4000
		
		self.G1000AltimeterBackground.resize((125,325))
		
		self.addItem(self.G1000AltimeterBackground, (0,0), False)
		'''
		#-------------------------------------------------------------------------------------------------
		# Altimeter tape 
		#-------------------------------------------------------------------------------------------------
		self.G1000AltimeterTape = XPinstrument.InstrumentImage("G1000Altimeter/G1000Alti_tape",(0,0),[12,276],[0,0], self.testMode)
		self.G1000AltimeterTape.setTranslateTexture(True)
		self.G1000AltimeterTape.enableTranslation (self.XPlaneDataDispatcher,(20,5),[ [0,0],[100,45]],conversionFunctions.returnAlti10s)
		self.addItem(self.G1000AltimeterTape, (2,25), False)	

		self.altiMarksClippingPanel = XPinstrument.ClippingPanel([0,0],[80,275],"altiClippingPanel")
		self.addItem(self.altiMarksClippingPanel, (0,15), False)
		
		altiMarks_yorigin = 135	#152
		altiMarks_xorigin = 18	#20
		altiMarks_spacing = 45
		fontSize10y_adjust = 0
		
		self.altiMarking0 = XPinstrument.NumberTextField10kraised(G1000_fonts.FONT_LARGE_WHITE,G1000_fonts.FONT_MED_WHITE,fontSize10y_adjust)
		self.altiMarksClippingPanel.addItem(self.altiMarking0, (altiMarks_xorigin,altiMarks_yorigin), False)
		
		self.altiMarking_h1 = XPinstrument.NumberTextField10kraised(G1000_fonts.FONT_LARGE_WHITE,G1000_fonts.FONT_MED_WHITE,fontSize10y_adjust)
		self.altiMarksClippingPanel.addItem(self.altiMarking_h1, (altiMarks_xorigin,altiMarks_yorigin+altiMarks_spacing), False)
		
		self.altiMarking_h2 = XPinstrument.NumberTextField10kraised(G1000_fonts.FONT_LARGE_WHITE,G1000_fonts.FONT_MED_WHITE,fontSize10y_adjust)
		self.altiMarksClippingPanel.addItem(self.altiMarking_h2, (altiMarks_xorigin,altiMarks_yorigin+altiMarks_spacing*2), False)
		
		self.altiMarking_h3 = XPinstrument.NumberTextField10kraised(G1000_fonts.FONT_LARGE_WHITE,G1000_fonts.FONT_MED_WHITE,fontSize10y_adjust)
		self.altiMarksClippingPanel.addItem(self.altiMarking_h3, (altiMarks_xorigin,altiMarks_yorigin+altiMarks_spacing*3), False)
		
		self.altiMarking_h4 = XPinstrument.NumberTextField10kraised(G1000_fonts.FONT_LARGE_WHITE,G1000_fonts.FONT_MED_WHITE,fontSize10y_adjust)
		self.altiMarksClippingPanel.addItem(self.altiMarking_h4, (altiMarks_xorigin,altiMarks_yorigin+altiMarks_spacing*4), False)
		
		self.altiMarking_b1 = XPinstrument.NumberTextField10kraised(G1000_fonts.FONT_LARGE_WHITE,G1000_fonts.FONT_MED_WHITE,fontSize10y_adjust)
		self.altiMarksClippingPanel.addItem(self.altiMarking_b1, (altiMarks_xorigin,altiMarks_yorigin-altiMarks_spacing), False)
		
		self.altiMarking_b2 = XPinstrument.NumberTextField10kraised(G1000_fonts.FONT_LARGE_WHITE,G1000_fonts.FONT_MED_WHITE,fontSize10y_adjust)
		self.altiMarksClippingPanel.addItem(self.altiMarking_b2, (altiMarks_xorigin,altiMarks_yorigin-altiMarks_spacing*2), False)
		
		self.altiMarking_b3 = XPinstrument.NumberTextField10kraised(G1000_fonts.FONT_LARGE_WHITE,G1000_fonts.FONT_MED_WHITE,fontSize10y_adjust)
		self.altiMarksClippingPanel.addItem(self.altiMarking_b3, (altiMarks_xorigin,altiMarks_yorigin-altiMarks_spacing*3), False)
		
		# Altitude select bug 
		self.altiSelectBug = XPinstrument.InstrumentImage("G1000Altimeter/G1000Alti_altselectbug",(0,0),None,None, self.testMode)
		self.altiSelectBug.enableTranslation (self.XPlaneDataDispatcher,(118,3),[ [-301,-301*0.45],[308,308*0.45]],self.returnAltiSelectDifference)
		self.altiMarksClippingPanel.addItem(self.altiSelectBug, (1,altiMarks_yorigin-2), False)
		
		#-------------------------------------------------------------------------------------------------
		# VSI 
		#-------------------------------------------------------------------------------------------------
		VSI_yorigin = 153
		
		self.VSIindicator = XPinstrument.InstrumentImage("G1000Altimeter/G1000Alti_VSI_indicator",(0,0),None,None, self.testMode)
		self.VSIindicator.enableTranslation (self.XPlaneDataDispatcher,(4,2),[ [-self.maxVVI,-28*4],[self.maxVVI,28*4]])
		self.addItem(self.VSIindicator,(90,VSI_yorigin),False)
		
		self.VSILabel = XPinstrument.TextField(G1000_fonts.FONT_SMALL_WHITE)
		self.VSILabel.setTextFormat('{: >5.0f}')
		self.VSILabel.setTextDataSource(self.XPlaneDataDispatcher,(4,2),conversionFunctions.roundToNearest10)
		self.addItem(self.VSILabel, (98,VSI_yorigin+2), False)
		
		self.refVSIindicatorBug = XPinstrument.InstrumentImage("G1000Altimeter/G1000Alti_VSI_refindicator",(0,0),None,None, self.testMode)
		self.refVSIindicatorBug.enableTranslation (self.XPlaneDataDispatcher,(118,2),[ [-self.maxVVI,-28*4],[self.maxVVI,28*4]])
		self.addItem(self.refVSIindicatorBug,(87,VSI_yorigin+1),False)
		
		self.refVSIbox = XPinstrument.InstrumentImage("G1000Altimeter/G1000Alti_refVS_box",(0,0),None,None, self.testMode)
		self.addItem(self.refVSIbox,(87,291),False)
		
		self.refVSILabel = XPinstrument.TextField(G1000_fonts.FONT_SMALL_WHITE)
		self.refVSILabel.setTextFormat('{: >5.0f}')
		self.refVSILabel.setTextDataSource(self.XPlaneDataDispatcher,(118,2))
		self.addItem(self.refVSILabel, (90,292), False)
		
		
		#-------------------------------------------------------------------------------------------------
		# Pressure labels 
		#-------------------------------------------------------------------------------------------------
		self.BAROUnitlabel = XPinstrument.TextField(G1000_fonts.FONT_VSMALL_TURQUOISE)
		self.BAROUnitlabel.setText("IN")
		self.addItem(self.BAROUnitlabel, (61,4), False)
		
		self.BAROLabel = XPinstrument.TextField(G1000_fonts.FONT_SMALL_TURQUOISE)
		self.BAROLabel.setTextFormat('{: >2.2f}')
		self.BAROLabel.setTextDataSource(self.XPlaneDataDispatcher,(7,0))
		self.addItem(self.BAROLabel, (16,4), False)
		'''
		#-------------------------------------------------------------------------------------------------
		# Altimeter box 
		#-------------------------------------------------------------------------------------------------
		self.G1000AltimeterAltibox = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[80,55],[827,2048-1536], "G1000AltimeterBackground")
		self.G1000AltimeterAltibox.resize((80,55))
		self.addItem(self.G1000AltimeterAltibox, (-20,0), False)
		
		self.Alti1kLabel = graphics.TextField(fonts.PROFONTWINDOWS_VLARGE_WHITE)
		self.Alti1kLabel.setTextFormat('{: >2.0f}')
		self.Alti1kLabel.setTextDataSource(self.XPlaneDataDispatcher,(20,5),conversionFunctions.returnAlti1k10kDigits)
		self.addItem(self.Alti1kLabel, (-50,-12), False)
		
		self.Alti10Label = graphics.TextField(fonts.PROFONTWINDOWS_LARGE_WHITE)
		self.Alti10Label.setTextFormat('{: >1.0f}')
		self.Alti10Label.setTextDataSource(self.XPlaneDataDispatcher,(20,5),conversionFunctions.returnAlti100sDigit)
		self.addItem(self.Alti10Label, (-20,-11), False)
		
		#def __init__(self, imagename, position=[0,0], cliprect=None, origin=None, testMode=False):
		self.Alti10sNrTape = graphics.ImagePanel(texture, batchImageRenderer, self.layer,(0,0),[28,51],[768,2048-1771], "G1000AltimeterBackground")
		self.Alti10sNrTape.resize((28,51))
		#("G1000Altimeter/G1000Alti_10s_tape",(0,0),[24,48],[0,24.5], self.testMode)
		#self.Alti10sNrTape.setTranslateTexture(True)
		#self.Alti10sNrTape.enableTranslation (self.XPlaneDataDispatcher,(20,5),[ [0,0],[100,95]],conversionFunctions.returnAlti10s)
		self.addItem(self.Alti10sNrTape, (6,0), False)	
		
		'''
		self.altiSelectedAltitude = graphics.NumberTextField10kraised(G1000_fonts.FONT_LARGE_TURQUOISE,G1000_fonts.FONT_MED_TURQUOISE,fontSize10y_adjust)
		self.addItem(self.altiSelectedAltitude, (21,302), False)
		'''
		
	def returnAltiSelectDifference(self,selectedAltitude,XPlaneDataDispatcher):
		altitude = self.XPlaneDataDispatcher.getData(20,5)
		return (selectedAltitude - altitude)
	
	def setAltiBarTextGrads(self):
		altitude = self.XPlaneDataDispatcher.getData(20,5)
		#print "altitude: ", altitude
		if self.testMode == True:
			altitude = D(self.testValue)
		
		selectedAltitude = self.XPlaneDataDispatcher.getData(118,3)
		self.altiSelectedAltitude.setNumber(selectedAltitude)
		
		altitude100 = D(altitude)//D(100)*100
		#print '************ altitude100', altitude100
		
		self.altiMarking0.setNumber(altitude100)
		self.altiMarking_h1.setNumber(altitude100+100)
		self.altiMarking_h2.setNumber(altitude100+200)
		self.altiMarking_h3.setNumber(altitude100+300)
		self.altiMarking_h4.setNumber(altitude100+400)
		self.altiMarking_b1.setNumber(altitude100-100)
		self.altiMarking_b2.setNumber(altitude100-200)
		self.altiMarking_b3.setNumber(altitude100-300)
		
		#[ [0,0],[100,45]],conversionFunctions.returnAlti10s
		y_translation = conversionFunctions.returnAlti10s(altitude,self.XPlaneDataDispatcher)*0.45
		self.altiMarking0.y = self.altiMarking0.orig_y - y_translation
		self.altiMarking_h1.y = self.altiMarking_h1.orig_y - y_translation
		self.altiMarking_h2.y = self.altiMarking_h2.orig_y - y_translation
		self.altiMarking_h3.y = self.altiMarking_h3.orig_y - y_translation
		self.altiMarking_h4.y = self.altiMarking_h4.orig_y - y_translation
		self.altiMarking_b1.y = self.altiMarking_b1.orig_y - y_translation
		self.altiMarking_b2.y = self.altiMarking_b2.orig_y - y_translation
		self.altiMarking_b3.y = self.altiMarking_b3.orig_y - y_translation
		
	
	def returnAltitude100sDigit(self, altitude):
		#print "altitude passed to me: ", altitude
		#21514.15	21.51415	0.51415	0.51415	5.1415	5
		returnValue = int(((abs(float(altitude)/1000))%1)*10)
		#print "return value: ", returnValue
		return returnValue
	
	def draw(self):
		'''
		self.setAltiBarTextGrads()

		VVI = self.XPlaneDataDispatcher.getData(4,2)
		if self.testMode == True:
			VVI = self.testValue
			
		#print "VVI:", VVI
		if abs(VVI)<100:
			self.VSILabel.setVisible(False)
		else:
			self.VSILabel.setVisible(True)
		y_translation = VVI*28*4/self.maxVVI
		if VVI>self.maxVVI:
			y_translation = self.maxVVI*28*4/self.maxVVI
		if VVI<-self.maxVVI:
			y_translation = -self.maxVVI*28*4/self.maxVVI
			
		self.VSILabel.y = self.VSILabel.orig_y + y_translation
		'''
		super(G1000Altimeter,self).draw()

