from lib.general.pyGaugesPanel import *
from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3
from lib.graphics import fonts

def drawInstruments():
	
	airspeedIndicator.setTestValue(testGaugesPanel.testValue)
	altimeter.setTestValue(testGaugesPanel.testValue)
	vario.setTestValue(testGaugesPanel.testValue)
	gyro.setTestValue(testGaugesPanel.testValue)
	artHorizon.setTestValue(testGaugesPanel.testValue)
	turnCoord.setTestValue(testGaugesPanel.testValue)
	
	VOR1.setTestValue(testGaugesPanel.testValue)
	VOR2.setTestValue(testGaugesPanel.testValue)
	
	
	annunciatorPanel.draw()
	
	fuelGauge.draw()
	oilGauge.draw()
	vacAmpGauge.draw()
	fuelFlowGauge.draw()
	
	artHorizon.draw()
	airspeedIndicator.draw()
	altimeter.draw()
	vario.draw()
	gyro.draw()
	turnCoord.draw()
	
	VOR1.draw()
	VOR2.draw()
	ADF.draw()
	RPM.draw()
	
	Compass.draw()
	PitchTrimSlider.draw()
	batchImageRenderer.render()
	
	#airportPlatesBrowser.draw()
	

#********************************************************************************************
#
# Initialise Panel - do not use any Open GL functions or calls before this
#  there should be no need to change this section.
#
#********************************************************************************************
testGaugesPanel = pyGaugesPanel()
testGaugesPanel.initDisplay()
testGaugesPanel.initXPlaneDataServer()

testGaugesPanel.setDrawCallback(drawInstruments)

#********************************************************************************************
#
# Initialise your instruments in this section 
#
#********************************************************************************************
#------------------------------------------------------------------------------------------
#	Load Textures
#------------------------------------------------------------------------------------------
standard6Texture = 	OpenGL3lib.GL_Texture("data/c172_text_standard6.png")
compassTexture =	OpenGL3lib.GL_Texture("data/gen_compass.png")
sliderTexture = 	OpenGL3lib.GL_Texture("data/gen_slider.png")
#------------------------------------------------------------------------------------------
#	Instruments position
#------------------------------------------------------------------------------------------
standardInstrumentSize = (300,300)
smallGaugeSize =(200,200)

std6_orig = [170,670]
VOR_ADF_orig = [1100,680]
RPM_pos=[970,130]
ANNUNCIATOR_pos = [620,860]
ANNUNCIATOR_size = (446,66)
Compass_pos = [1340,735]

ZOOM_STD6 =  0.97
std6_xgrid = 300
std6_ygrid = 300

ZOOM_VORADF = 0.94
voradf_ygrid = 290

smallgauges_orig = [110,105]
smallgauges_xgrid = 200
smallgauges_ygrid = 200


ASI_pos = [std6_orig[0],std6_orig[1]]
AH_pos=[std6_orig[0]+std6_xgrid,std6_orig[1]]
ALT_pos = [std6_orig[0]+std6_xgrid*2,std6_orig[1]]
TC_pos=[std6_orig[0],std6_orig[1]-std6_ygrid]
DG_pos=[std6_orig[0]+std6_xgrid,std6_orig[1]-std6_ygrid]
VSI_pos=[std6_orig[0]+std6_xgrid*2,std6_orig[1]-std6_ygrid]

VOR1_pos=[VOR_ADF_orig[0],VOR_ADF_orig[1]]
VOR2_pos=[VOR_ADF_orig[0],VOR_ADF_orig[1]-voradf_ygrid]
ADF_pos=[VOR_ADF_orig[0]+196,VOR_ADF_orig[1]-voradf_ygrid-245]

OIL_pos = [smallgauges_orig[0],smallgauges_orig[1]]
AMP_VAC_pos= [smallgauges_orig[0]+smallgauges_xgrid,smallgauges_orig[1]]
FUEL_pos = [smallgauges_orig[0]+smallgauges_xgrid*2,smallgauges_orig[1]] 
FUELFLOW_pos = [smallgauges_orig[0]+smallgauges_xgrid*3,smallgauges_orig[1]]



#------------------------------------------------------------------------------------------
#	Import Instruments
#------------------------------------------------------------------------------------------
from instruments import C172_AnnunciatorPanel
from instruments import C172_FuelFlowGauge
from instruments import C172_AmpVacGauge
from instruments import C172_OilPressTempGauge
from instruments import C172_FuelGauge

from instruments import C172_AirspeedIndicator
from instruments import C172_Altimeter
from instruments import C172_VSI_Indicator
from instruments import C172_DirectionalGyro
from instruments import C172_ArtificialHorizon
from instruments import C172_TurnCoordinator
from instruments import C172_VOR
from instruments import C172_ADF
from instruments import C172_RPM_Indicator
from instruments import GenCompass
from instruments import AirportPlatesBrowser
from instruments import Gen_SliderIndicator

#------------------------------------------------------------------------------------------
#	Initialise Instruments
#------------------------------------------------------------------------------------------
XPlaneDataServer = testGaugesPanel.XPlaneDataServer

XPlaneDataServer.requestXPDref(301, "sim/cockpit/radios/nav1_dme_dist_m[0]")
XPlaneDataServer.requestXPDref(302, "sim/cockpit/radios/nav1_obs_degt[0]")
XPlaneDataServer.requestXPDref(303, "sim/cockpit/misc/compass_indicated[0]")
XPlaneDataServer.requestXPDref(304, "sim/cockpit/radios/nav1_freq_hz[0]")
XPlaneDataServer.requestXPDref(305, "sim/cockpit/radios/nav_type[0]")
XPlaneDataServer.requestXPDref(306, "sim/cockpit2/gauges/actuators/artificial_horizon_adjust_deg_pilot[0]")
XPlaneDataServer.requestXPDref(307, "sim/cockpit2/gauges/indicators/turn_rate_roll_deg_pilot[0]")
XPlaneDataServer.requestXPDref(308, "sim/cockpit2/gauges/indicators/heading_vacuum_deg_mag_pilot[0]")
XPlaneDataServer.requestXPDref(309, "sim/cockpit2/gauges/indicators/compass_heading_deg_mag[0]")
XPlaneDataServer.requestXPDref(321, "sim/cockpit2/controls/elevator_trim[0]")

batchImageRenderer = OpenGL3lib.GL_BatchImageRenderer(10) # create a batch renderer with 10 layers

annunciatorPanel = 	C172_AnnunciatorPanel.C172_AnnunciatorPanel		(ANNUNCIATOR_pos, 	ANNUNCIATOR_size,		XPlaneDataServer, batchImageRenderer, 	standard6Texture)

fuelFlowGauge = 	C172_FuelFlowGauge.C172_FuelFlowGauge			(FUELFLOW_pos,		smallGaugeSize, 		XPlaneDataServer, batchImageRenderer, 	standard6Texture)	#calibrated
vacAmpGauge = 		C172_AmpVacGauge.C172_AmpVacGauge				(AMP_VAC_pos,		smallGaugeSize, 		XPlaneDataServer, batchImageRenderer, 	standard6Texture)	#calibrated
oilGauge = 			C172_OilPressTempGauge.C172_OilPressTempGauge	(OIL_pos,			smallGaugeSize, 		XPlaneDataServer, batchImageRenderer, 	standard6Texture)	#calibrated
fuelGauge = 		C172_FuelGauge.C172_FuelGauge					(FUEL_pos,			smallGaugeSize, 		XPlaneDataServer, batchImageRenderer, 	standard6Texture)	#calibrated

airspeedIndicator = C172_AirspeedIndicator.C172_AirspeedIndicator	(ASI_pos,			standardInstrumentSize, XPlaneDataServer, batchImageRenderer, 	standard6Texture, ZOOM_STD6)	#calibrated
altimeter = 		C172_Altimeter.C172_Altimeter					(ALT_pos,			standardInstrumentSize, XPlaneDataServer, batchImageRenderer, 	standard6Texture, ZOOM_STD6)	#calibrated
vario = 			C172_VSI_Indicator.C172_VSI_Indicator			(VSI_pos,			standardInstrumentSize, XPlaneDataServer, batchImageRenderer, 	standard6Texture, ZOOM_STD6)	#calibrated
gyro = 				C172_DirectionalGyro.C172_DirectionalGyro		(DG_pos,			standardInstrumentSize, XPlaneDataServer, batchImageRenderer, 	standard6Texture, ZOOM_STD6)	#calibrated
artHorizon = 		C172_ArtificialHorizon.C172_ArtificialHorizon	(AH_pos,			standardInstrumentSize, XPlaneDataServer, batchImageRenderer, 	standard6Texture, ZOOM_STD6)	#calibrated
turnCoord = 		C172_TurnCoordinator.C172_TurnCoordinator		(TC_pos,			standardInstrumentSize, XPlaneDataServer, batchImageRenderer, 	standard6Texture, ZOOM_STD6)

VOR1 = 				C172_VOR.C172_VOR								(VOR1_pos,			standardInstrumentSize, XPlaneDataServer, batchImageRenderer, standard6Texture, "172 VOR1", "VOR1", ZOOM_VORADF)	#calibrated
VOR2 = 				C172_VOR.C172_VOR								(VOR2_pos,			standardInstrumentSize, XPlaneDataServer, batchImageRenderer, standard6Texture, "172 VOR2", "VOR2", ZOOM_VORADF)	#calibrated
ADF = 				C172_ADF.C172_ADF								(ADF_pos,			standardInstrumentSize, XPlaneDataServer, batchImageRenderer, standard6Texture, ZOOM_VORADF)		#calibrated
RPM = 				C172_RPM_Indicator.C172_RPM_Indicator			(RPM_pos,			(280,280)			  , XPlaneDataServer, batchImageRenderer, standard6Texture, 0.9)		#calibrated

Compass = 			GenCompass.GenCompass							(Compass_pos,		(120,66)			  , XPlaneDataServer, batchImageRenderer, compassTexture)

PitchTrimSlider = 	Gen_SliderIndicator.Gen_SliderIndicator			((1350,500),		(100,30), 				XPlaneDataServer, batchImageRenderer, sliderTexture)
PitchTrimSlider.setPointerDataref((321,0))

#airportPlatesBrowser = AirportPlatesBrowser.AirportPlatesBrowser([1000,testGaugesPanel.frameBufferHeight-950], [570,840], testGaugesPanel, batchImageRenderer)

#airspeedIndicator.setTestMode(True)
#altimeter.setTestMode(True)
#vario.setTestMode(True)
#gyro.setTestMode(True)
#artHorizon.setTestMode(True)
#turnCoord.setTestMode(True)

#VOR1.setTestMode(True)
#VOR2.setTestMode(True)


batchImageRenderer.fillBuffers()


testGaugesPanel.run()



