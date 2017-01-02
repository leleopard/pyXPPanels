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
	
	#GL_PIL_Font.draw("abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0.123456789+-:/test PIL",200,100)
	#GL_Normal_Font.draw("0.123456789+-:/test non PIL",200,200)
	
	

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

NAVCOMM_BK165_1 	= BendixKing_NAVCOMM_KX165A.BK_NAVCOMM_KX165A 	(NAVCOMM_BK165_1_POS, 	ALT_SIZE, XPlaneDataServer, batchImageRenderer, RadioStackTexture, 1 )
NAVCOMM_BK165_2 	= BendixKing_NAVCOMM_KX165A.BK_NAVCOMM_KX165A 	(NAVCOMM_BK165_2_POS, 	ALT_SIZE, XPlaneDataServer, batchImageRenderer, RadioStackTexture, 2 )
DME_KN6X 			= BendixKing_DME_KN6X.BK_DME_KN6X 				(DME_KN6X_POS, 			ALT_SIZE, XPlaneDataServer, batchImageRenderer, RadioStackTexture )
ADF_KR87 			= BendixKing_ADF_KR87.BK_ADF_KR87 				(BK_ADF_KR87_POS, 		ALT_SIZE, XPlaneDataServer, batchImageRenderer, RadioStackTexture )
XPDR_KT70 			= BendixKing_XPDR_KT70.BK_XPDR_KT70 			(BK_XPDR_KT70_POS, 		ALT_SIZE, XPlaneDataServer, batchImageRenderer, RadioStackTexture )

batchImageRenderer.fillBuffers()

#GL_PIL_Font = OpenGL3lib.GL_Font("data/fonts/ttf-bitstream-vera-1.10/Vera.ttf",20,(211,62,33))
#GL_PIL_Font = OpenGL3lib.GL_Font("data/fonts/DS-Digital-ItalicST.ttf",40,(211,62,33))
#GL_Normal_Font = OpenGL3lib.GL_Font_OLD_PYGAME("data/fonts/DS-Digital-ItalicST.ttf",40,(211,62,33))


RadioStack_Panel.run()



