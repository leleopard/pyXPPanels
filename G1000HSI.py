import XPlaneUDPServer
import XPinstrument
import conversionFunctions
import logging
import OpenGLlib
import decimal
D = decimal.Decimal
import G1000_fonts

class G1000HSI(XPinstrument.STinstrument):
	XPlaneDataDispatcher = None
	
	def __init__(self,position, size, XPlaneDataDispatcher, name = "G1000HSI"):
		XPinstrument.STinstrument.__init__(self,position, size, name)
		
		self.testMode = False
		self.XPlaneDataDispatcher = XPlaneDataDispatcher
		
		#-------------------------------------------------------------------------------------------------
		# Compass Rose / Heading Bug
		#-------------------------------------------------------------------------------------------------
		self.G1000HSICompassRose = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_compassrose")
		self.addImage(self.G1000HSICompassRose, (0,0), False)
		self.G1000HSICompassRose.enableRotation (XPlaneDataDispatcher,(17,3),[ [-380,380],[0,0],[360,-360]])

		self.G1000HSIHeadingBug = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_headingbug")
		self.addImage(self.G1000HSIHeadingBug, (0,0), False)
		self.G1000HSIHeadingBug.enableRotation (XPlaneDataDispatcher,(118,1),[ [-360,-360],[360,360]],conversionFunctions.addNondriftCompassHeadingToValue)
		
		#-------------------------------------------------------------------------------------------------
		# Selected Heading box 
		#-------------------------------------------------------------------------------------------------
		selectedHdg_x = 17
		selectedHdg_y = 275
		
		self.G1000HSIselectedHeadingBox = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_headingbox")
		self.addImage(self.G1000HSIselectedHeadingBox, (selectedHdg_x-2,selectedHdg_y-1), False)
		
		self.G1000HSIselectedHeadingTxt = XPinstrument.TextField(G1000_fonts.FONT_VSMALL_WHITE)
		self.G1000HSIselectedHeadingTxt.setText("HDG")
		self.addImage(self.G1000HSIselectedHeadingTxt, (selectedHdg_x,selectedHdg_y), False)
		
		self.G1000HSIselectedHeading = XPinstrument.TextField(G1000_fonts.FONT_SMALL_TURQUOISE)
		self.G1000HSIselectedHeading.setTextFormat(XPinstrument.TXT_FMT_3DIG_PREC0_0PADDED)
		self.G1000HSIselectedHeading.setDisplayUnit(chr(176))
		self.G1000HSIselectedHeading.setTextDataSource(XPlaneDataDispatcher,(118,1))
		self.addImage(self.G1000HSIselectedHeading, (selectedHdg_x+27,selectedHdg_y), False)
		
		#-------------------------------------------------------------------------------------------------
		# VOR1
		#-------------------------------------------------------------------------------------------------
		self.G1000HSIVOR1 = XPinstrument.STinstrument([0,0],(320,320),"G1000HSIVOR1")
		self.addImage(self.G1000HSIVOR1, (0,0), False)
		
		self.G1000HSIVOR1Txt = XPinstrument.TextField(G1000_fonts.FONT_SMALL_GREEN)
		self.G1000HSIVOR1Txt.setText("VOR1")
		self.G1000HSIVOR1.addImage(self.G1000HSIVOR1Txt, (115,180), False)
		
		self.G1000HSIVOR1pointer = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_VOR1pointer")
		self.G1000HSIVOR1.addImage(self.G1000HSIVOR1pointer, (0,0), False)
		self.G1000HSIVOR1pointer.enableRotation (XPlaneDataDispatcher,(98,0),[ [-380,-380],[380,380]],conversionFunctions.addNondriftCompassHeadingToValue)
		
		self.G1000HSIVOR1CDI = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_VOR1CDI")
		self.G1000HSIVOR1.addImage(self.G1000HSIVOR1CDI, (0,0), False)
		self.G1000HSIVOR1CDI.enableRotation (XPlaneDataDispatcher,(98,0),[ [-380,-380],[380,380]],conversionFunctions.addNondriftCompassHeadingToValue)
		self.G1000HSIVOR1CDI.enableTranslation (XPlaneDataDispatcher,(99,5),[ [-2.5,-2.5*27],[2.5,2.5*27]],False,None,90)
		
		self.G1000HSIVOR1TOpointer = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_VOR1TOpointer")
		self.G1000HSIVOR1.addImage(self.G1000HSIVOR1TOpointer, (0,0), False)
		self.G1000HSIVOR1TOpointer.enableRotation (XPlaneDataDispatcher,(98,0),[ [-380,-380],[380,380]],conversionFunctions.addNondriftCompassHeadingToValue)
		self.G1000HSIVOR1TOpointer.toggleVisibility(XPlaneDataDispatcher,(98,2), conversionFunctions.NAV_TO_Toggle)
		
		self.G1000HSIVOR1FROMpointer = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_VOR1FROMpointer")
		self.G1000HSIVOR1.addImage(self.G1000HSIVOR1FROMpointer, (0,0), False)
		self.G1000HSIVOR1FROMpointer.enableRotation (XPlaneDataDispatcher,(98,0),[ [-380,-380],[380,380]],conversionFunctions.addNondriftCompassHeadingToValue)
		self.G1000HSIVOR1FROMpointer.toggleVisibility(XPlaneDataDispatcher,(98,2), conversionFunctions.NAV_FR_Toggle)

		#-------------------------------------------------------------------------------------------------
		# VOR1 Selected Course box 
		#-------------------------------------------------------------------------------------------------
		selectedHdg_x = 230
		selectedHdg_y = 275
		
		self.G1000HSIVOR1selectedCourseBox = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_headingbox")
		self.G1000HSIVOR1.addImage(self.G1000HSIVOR1selectedCourseBox, (selectedHdg_x-2,selectedHdg_y-1), False)
		
		self.G1000HSIVOR1selectedCourseTxt = XPinstrument.TextField(G1000_fonts.FONT_VSMALL_WHITE)
		self.G1000HSIVOR1selectedCourseTxt.setText("CRS")
		self.G1000HSIVOR1.addImage(self.G1000HSIVOR1selectedCourseTxt, (selectedHdg_x,selectedHdg_y), False)
		
		self.G1000HSIVOR1selectedCourse = XPinstrument.TextField(G1000_fonts.FONT_SMALL_GREEN)
		self.G1000HSIVOR1selectedCourse.setTextFormat(XPinstrument.TXT_FMT_3DIG_PREC0_0PADDED)
		self.G1000HSIVOR1selectedCourse.setDisplayUnit(chr(176))
		self.G1000HSIVOR1selectedCourse.setTextDataSource(XPlaneDataDispatcher,(98,0))
		self.G1000HSIVOR1.addImage(self.G1000HSIVOR1selectedCourse, (selectedHdg_x+27,selectedHdg_y), False)
		
		#-------------------------------------------------------------------------------------------------
		# VOR2
		#-------------------------------------------------------------------------------------------------
		self.G1000HSIVOR2 = XPinstrument.STinstrument([0,0],(320,320),"G1000HSIVOR2")
		self.addImage(self.G1000HSIVOR2, (0,0), False)
		
		self.G1000HSIVOR2Txt = XPinstrument.TextField(G1000_fonts.FONT_SMALL_GREEN)
		self.G1000HSIVOR2Txt.setText("VOR2")
		self.G1000HSIVOR2.addImage(self.G1000HSIVOR2Txt, (115,180), False)
		
		self.G1000HSIVOR2pointer = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_VOR2pointer")
		self.G1000HSIVOR2.addImage(self.G1000HSIVOR2pointer, (0,0), False)
		self.G1000HSIVOR2pointer.enableRotation (XPlaneDataDispatcher,(98,4),[ [-380,-380],[380,380]],conversionFunctions.addNondriftCompassHeadingToValue)
		
		self.G1000HSIVOR2CDI = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_VOR2CDI")
		self.G1000HSIVOR2.addImage(self.G1000HSIVOR2CDI, (0,0), False)
		self.G1000HSIVOR2CDI.enableRotation (XPlaneDataDispatcher,(98,4),[ [-380,-380],[380,380]],conversionFunctions.addNondriftCompassHeadingToValue)
		self.G1000HSIVOR2CDI.enableTranslation (XPlaneDataDispatcher,(100,5),[ [-2.5,-2.5*27],[2.5,2.5*27]],False,None,90)
		
		self.G1000HSIVOR2TOpointer = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_VOR1TOpointer")
		self.G1000HSIVOR2.addImage(self.G1000HSIVOR2TOpointer, (0,0), False)
		self.G1000HSIVOR2TOpointer.enableRotation (XPlaneDataDispatcher,(98,4),[ [-380,-380],[380,380]],conversionFunctions.addNondriftCompassHeadingToValue)
		self.G1000HSIVOR2TOpointer.toggleVisibility(XPlaneDataDispatcher,(98,6), conversionFunctions.NAV_TO_Toggle)
		
		self.G1000HSIVOR2FROMpointer = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_VOR1FROMpointer")
		self.G1000HSIVOR2.addImage(self.G1000HSIVOR2FROMpointer, (0,0), False)
		self.G1000HSIVOR2FROMpointer.enableRotation (XPlaneDataDispatcher,(98,4),[ [-380,-380],[380,380]],conversionFunctions.addNondriftCompassHeadingToValue)
		self.G1000HSIVOR2FROMpointer.toggleVisibility(XPlaneDataDispatcher,(98,6), conversionFunctions.NAV_FR_Toggle)
		
		#-------------------------------------------------------------------------------------------------
		# VOR2 Selected Course box 
		#-------------------------------------------------------------------------------------------------
		selectedHdg_x = 230
		selectedHdg_y = 275
		
		self.G1000HSIVOR2selectedCourseBox = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_headingbox")
		self.G1000HSIVOR2.addImage(self.G1000HSIVOR2selectedCourseBox, (selectedHdg_x-2,selectedHdg_y-1), False)
		
		self.G1000HSIVOR2selectedCourseTxt = XPinstrument.TextField(G1000_fonts.FONT_VSMALL_WHITE)
		self.G1000HSIVOR2selectedCourseTxt.setText("CRS")
		self.G1000HSIVOR2.addImage(self.G1000HSIVOR2selectedCourseTxt, (selectedHdg_x,selectedHdg_y), False)
		
		self.G1000HSIVOR2selectedCourse = XPinstrument.TextField(G1000_fonts.FONT_SMALL_GREEN)
		self.G1000HSIVOR2selectedCourse.setTextFormat(XPinstrument.TXT_FMT_3DIG_PREC0_0PADDED)
		self.G1000HSIVOR2selectedCourse.setDisplayUnit(chr(176))
		self.G1000HSIVOR2selectedCourse.setTextDataSource(XPlaneDataDispatcher,(98,4))
		self.G1000HSIVOR2.addImage(self.G1000HSIVOR2selectedCourse, (selectedHdg_x+27,selectedHdg_y), False)
		
		#-------------------------------------------------------------------------------------------------
		# Static Compass Rose 
		#-------------------------------------------------------------------------------------------------
		self.G1000HSIStaticCompassRose = XPinstrument.InstrumentImage("G1000HSI/G1000HSI_staticcompassrose")
		self.addImage(self.G1000HSIStaticCompassRose, (0,0), False)
		
		#-------------------------------------------------------------------------------------------------
		# Current Heading box 
		#-------------------------------------------------------------------------------------------------
		self.G1000HSIcurrentHeading = XPinstrument.TextField(G1000_fonts.FONT_LARGE_WHITE)
		self.G1000HSIcurrentHeading.setTextFormat(XPinstrument.TXT_FMT_3DIG_PREC0_0PADDED)
		self.G1000HSIcurrentHeading.setDisplayUnit(chr(176))
		self.G1000HSIcurrentHeading.setTextDataSource(XPlaneDataDispatcher,(17,3))
		self.addImage(self.G1000HSIcurrentHeading, (141,288), False)
		
		
	def setVORvisibility(self):
		NAVsource = int(self.XPlaneDataDispatcher.getData(107,3))
		NAV1_ntype = int(self.XPlaneDataDispatcher.getData(99,0))
		NAV2_ntype = int(self.XPlaneDataDispatcher.getData(100,0))
		
		self.G1000HSIVOR1.setVisible(False)
		self.G1000HSIVOR2.setVisible(False)
		
		if (NAVsource == 0) and (NAV1_ntype !=0) :	#VOR1
			self.G1000HSIVOR1.setVisible(True)
		if (NAVsource == 1) and (NAV2_ntype !=0) :	#VOR1
			self.G1000HSIVOR2.setVisible(True)
			
		
	def draw(self):
		self.setVORvisibility()
		
		super(G1000HSI,self).draw()

