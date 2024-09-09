from lib.general import pyXPPanel
from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3
from lib.graphics import fonts

def drawInstruments():
	#annunciatorPanel.draw()
	artificialHorizon.draw()
	artificialHorizon.setTestValue(G1000_Panel.testValue)
	batchImageRenderer.render()
	altimeter.draw()
	
	#airportPlatesBrowser.draw()
	

#********************************************************************************************
#
# Initialise Panel - do not use any Open GL functions or calls before this
#  there should be no need to change this section.
#
#********************************************************************************************
G1000_Panel = pyXPPanel.pyXPPanel()
#G1000_Panel.initDisplay()
#G1000_Panel.initXPlaneDataServer()

G1000_Panel.setDrawCallback(drawInstruments)

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
G1000Texture =	OpenGL3lib.GL_Texture("data/G1000_2048_texture.png")
#------------------------------------------------------------------------------------------
#	Instruments position
#------------------------------------------------------------------------------------------
ANNUNCIATOR_pos = [793,1003]
ANNUNCIATOR_size = (446,66)
ART_HOR_POSITION = (500,450)
ART_HOR_SIZE = (835, 626)
ALT_POSITION = (720,533)
ALT_SIZE = (125,325)
#------------------------------------------------------------------------------------------
#	Import Instruments
#------------------------------------------------------------------------------------------
from instruments import C172_AnnunciatorPanel
from instruments import AirportPlatesBrowser
from instruments import G1000_ArtificialHorizon
from instruments import G1000Altimeter

#------------------------------------------------------------------------------------------
#	Initialise Instruments
#------------------------------------------------------------------------------------------
#XPlaneDataServer = G1000_Panel.XPlaneDataServer
batchImageRenderer = OpenGL3lib.GL_BatchImageRenderer(10) # create a batch renderer with 10 layers

artificialHorizon = G1000_ArtificialHorizon.G1000_ArtificialHorizon	( ART_HOR_POSITION, ART_HOR_SIZE, batchImageRenderer, G1000Texture )
#artificialHorizon.setTestMode(True)
#def __init__(self,position, size, XPlaneDataDispatcher, batchImageRenderer, texture, jetVSI = False, name = "G1000Altimeter"):
	
altimeter = G1000Altimeter.G1000Altimeter (ALT_POSITION, ALT_SIZE, batchImageRenderer, G1000Texture, True )
#annunciatorPanel = 	C172_AnnunciatorPanel.C172_AnnunciatorPanel		(ANNUNCIATOR_pos, 	ANNUNCIATOR_size,		XPlaneDataServer, batchImageRenderer, 	standard6Texture)

#airportPlatesBrowser = AirportPlatesBrowser.AirportPlatesBrowser([1000,G1000_Panel.frameBufferHeight-950], [570,840], G1000_Panel, batchImageRenderer)



batchImageRenderer.fillBuffers()


G1000_Panel.run()



