# displays a Bendix King radio stack
from lib.general import pyXPPanel
from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3
from lib.graphics import fonts


def drawInstruments():
	
	batchImageRenderer.render()
	NAVCOMM_BK165_1.draw()
	NAVCOMM_BK165_2.draw()
	DME_KN6X.draw()
	ADF_KR87.draw()
	XPDR_KT70.draw()
	


#********************************************************************************************
#
# Initialise Panel - do not use any Open GL functions or calls before this
#  there should be no need to change this section.
#
#********************************************************************************************
RadioStack_Panel = pyXPPanel.pyXPPanel()
RadioStack_Panel.initArduinoSerialConnection()

RadioStack_Panel.setDrawCallback(drawInstruments)

#********************************************************************************************
#
# Initialise your instruments in this section 
#
#********************************************************************************************
#------------------------------------------------------------------------------------------
#	Load Textures
#------------------------------------------------------------------------------------------
RadioStackTexture =	OpenGL3lib.GL_Texture("data/2048_Radio_Stack_text.png")
#------------------------------------------------------------------------------------------
#	Instruments position
#------------------------------------------------------------------------------------------
NAVCOMM_BK165_1_POS 	= (35,670)
NAVCOMM_BK165_2_POS 	= (35,470)
DME_KN6X_POS 			= (25,337)
BK_ADF_KR87_POS 		= (25,240)
BK_XPDR_KT70_POS 		= (50,110)

ALT_SIZE = (125,325)
#------------------------------------------------------------------------------------------
#	Import Instruments
#------------------------------------------------------------------------------------------
from instruments import BendixKing_NAVCOMM_KX165A
from instruments import BendixKing_DME_KN6X
from instruments import BendixKing_ADF_KR87
from instruments import BendixKing_XPDR_KT70

#------------------------------------------------------------------------------------------
#	Initialise Instruments
#------------------------------------------------------------------------------------------
XPlaneDataServer = RadioStack_Panel.XPlaneDataServer
batchImageRenderer = OpenGL3lib.GL_BatchImageRenderer(10) # create a batch renderer with 10 layers

#XPlaneUDPServer.pyXPUDPServer.requestXPDref(310, "sim/cockpit2/radios/actuators/com1_power[0]")
#XPlaneUDPServer.pyXPUDPServer.requestXPDref(311, "sim/cockpit2/radios/actuators/com2_power[0]")
#XPlaneUDPServer.pyXPUDPServer.requestXPDref(312, "sim/cockpit2/radios/actuators/dme_power[0]")
#XPlaneUDPServer.pyXPUDPServer.requestXPDref(313, "sim/cockpit/radios/adf1_stdby_freq_hz[0]")
#XPlaneUDPServer.pyXPUDPServer.requestXPDref(314, "sim/cockpit2/radios/actuators/adf1_power[0]")
#XPlaneUDPServer.pyXPUDPServer.requestXPDref(315, "sim/time/total_flight_time_sec[0]")
#XPlaneUDPServer.pyXPUDPServer.requestXPDref(316, "sim/cockpit2/clock_timer/elapsed_time_minutes[0]")
#XPlaneUDPServer.pyXPUDPServer.requestXPDref(317, "sim/cockpit2/clock_timer/elapsed_time_seconds[0]")
#XPlaneUDPServer.pyXPUDPServer.requestXPDref(318, "sim/cockpit2/radios/actuators/transponder_code[0]")
#XPlaneUDPServer.pyXPUDPServer.requestXPDref(319, "sim/cockpit2/radios/actuators/transponder_mode[0]")
#XPlaneUDPServer.pyXPUDPServer.requestXPDref(320, "sim/cockpit/radios/transponder_light[0]")


NAVCOMM_BK165_1 	= BendixKing_NAVCOMM_KX165A.BK_NAVCOMM_KX165A 	(NAVCOMM_BK165_1_POS, 	ALT_SIZE, batchImageRenderer, RadioStackTexture, 1 )
NAVCOMM_BK165_2 	= BendixKing_NAVCOMM_KX165A.BK_NAVCOMM_KX165A 	(NAVCOMM_BK165_2_POS, 	ALT_SIZE, batchImageRenderer, RadioStackTexture, 2 )
DME_KN6X 			= BendixKing_DME_KN6X.BK_DME_KN6X 				(DME_KN6X_POS, 			ALT_SIZE, batchImageRenderer, RadioStackTexture )
ADF_KR87 			= BendixKing_ADF_KR87.BK_ADF_KR87 				(BK_ADF_KR87_POS, 		ALT_SIZE, batchImageRenderer, RadioStackTexture )
XPDR_KT70 			= BendixKing_XPDR_KT70.BK_XPDR_KT70 			(BK_XPDR_KT70_POS, 		ALT_SIZE, batchImageRenderer, RadioStackTexture )

batchImageRenderer.fillBuffers()


RadioStack_Panel.run()



