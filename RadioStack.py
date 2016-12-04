# displays a Bendix King radio stack
from lib.general.pyGaugesPanel import *
from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3
from lib.graphics import fonts


def drawInstruments():
	
	batchImageRenderer.render()
	NAVCOMM_BK165_1.draw()
	NAVCOMM_BK165_2.draw()
	DME_KN6X.draw()
	ADF_KR87.draw()
	
	

#********************************************************************************************
#
# Initialise Panel - do not use any Open GL functions or calls before this
#  there should be no need to change this section.
#
#********************************************************************************************
RadioStack_Panel = pyGaugesPanel()
RadioStack_Panel.initDisplay()
RadioStack_Panel.initXPlaneDataServer()
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
NAVCOMM_BK165_1_POS = (50,600)
NAVCOMM_BK165_2_POS = (50,500)
DME_KN6X_POS = (50,400)
BK_ADF_KR87_POS = (50,300)

ALT_SIZE = (125,325)
#------------------------------------------------------------------------------------------
#	Import Instruments
#------------------------------------------------------------------------------------------
from instruments import BendixKing_NAVCOMM_KX165A
from instruments import BendixKing_DME_KN6X
from instruments import BendixKing_ADF_KR87


#------------------------------------------------------------------------------------------
#	Initialise Instruments
#------------------------------------------------------------------------------------------
XPlaneDataServer = RadioStack_Panel.XPlaneDataServer
batchImageRenderer = OpenGL3lib.GL_BatchImageRenderer(10) # create a batch renderer with 10 layers

NAVCOMM_BK165_1 = BendixKing_NAVCOMM_KX165A.BK_NAVCOMM_KX165A (NAVCOMM_BK165_1_POS, ALT_SIZE, XPlaneDataServer, batchImageRenderer, RadioStackTexture, 1 )
NAVCOMM_BK165_2 = BendixKing_NAVCOMM_KX165A.BK_NAVCOMM_KX165A (NAVCOMM_BK165_2_POS, ALT_SIZE, XPlaneDataServer, batchImageRenderer, RadioStackTexture, 2 )
DME_KN6X = BendixKing_DME_KN6X.BK_DME_KN6X (DME_KN6X_POS, ALT_SIZE, XPlaneDataServer, batchImageRenderer, RadioStackTexture )
ADF_KR87 = BendixKing_ADF_KR87.BK_ADF_KR87 (BK_ADF_KR87_POS, ALT_SIZE, XPlaneDataServer, batchImageRenderer, RadioStackTexture )

batchImageRenderer.fillBuffers()


RadioStack_Panel.run()



