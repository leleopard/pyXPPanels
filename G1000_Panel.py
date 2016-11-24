import sys, pygame, getopt
import math
import ConfigParser

from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGLlib

import XPlaneUDPServer
import XPinstrument
import logging

#------------------------------------------------------------------------------------------
#	Logging configuration
#------------------------------------------------------------------------------------------
FORMAT= '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

#------------------------------------------------------------------------------------------
#	Load Config file
#------------------------------------------------------------------------------------------
configFile = "./config.ini"

try:
	opts, args = getopt.getopt(sys.argv[1:],"c:")
except getopt.GetoptError:
	logging.error("No args passed")

for opt, arg in opts:
	if opt == '-c':
		logging.info('Config file provided')
		configFile = arg

Config = ConfigParser.ConfigParser()
Config.read(configFile)

#------------------------------------------------------------------------------------------
#	Network configuration
#------------------------------------------------------------------------------------------
IP = Config.get("Network","IP")
Port = Config.getint("Network","Port")
logging.info('Listening for XPlane UDP data on IP %s Port %s',IP,Port)

#------------------------------------------------------------------------------------------
#	Graphics configuration
#------------------------------------------------------------------------------------------
fullscreen = Config.getboolean("Graphics","Fullscreen")
ScreenWidth = Config.getint("Graphics","ScreenWidth")
ScreenHeight = Config.getint("Graphics","ScreenHeight")
maxFPS = Config.getint("Graphics","MaxFPS")

XPlaneDataDispatcher = XPlaneUDPServer.XPlaneUDPServer((IP,Port))

OpenGLlib.initializeDisplay(ScreenWidth,ScreenHeight,fullscreen)
clock = pygame.time.Clock()
# Start the network listener 
XPlaneDataDispatcher.start()
import conversionFunctions
import G1000_fonts

import G1000AirspeedIndicator
import G1000Altimeter
import G1000HSI

#------------------------------------------------------------------------------------------
#	Instruments position
#------------------------------------------------------------------------------------------
standardInstrumentSize = (314,314)

#------------------------------------------------------------------------------------------
#	G1000
#------------------------------------------------------------------------------------------

#																					 pos    w   h    x   y
#G1000Font = "data/fonts/Glass-Gauge.ttf"
G1000Font = "data/fonts/ProFontWindows.ttf"
FONT_SIZE_SMALL = 12
FONT_SIZE_MED = 17
TXT_COLOR_WHITE = (255,255,255)
TXT_COLOR_PINK = (254,0,254)
TXT_COLOR_GREY = (128,128,128)

TXT_FMT_3DIG_PREC0_0PADDED = '{:03.0f}'
TXT_FMT_3DIG_PREC2 = '{:06.2f}'
TXT_FMT_3DIG_PREC3 = '{:07.3f}'

G1000Horizon = XPinstrument.InstrumentImage("G1000_horizon",(0,0),[835,626],[606,713], False)
G1000PitchScale = XPinstrument.InstrumentImage("G1000_pitchscale",(0,0),[215,210],[875,1013],False)
G1000BankIndicator = XPinstrument.InstrumentImage("G1000_bankindicator",(0,0),[835,626],[606,713], False)
G1000Bug = XPinstrument.InstrumentImage("G1000_bug",(0,0),[835,626],[606,713])


G1000topBar = XPinstrument.InstrumentImage("G1000_topbar_background",(0,0))

#----------------------------------------------------
#	TRK angle

G1000TRKangle = XPinstrument.TextField(G1000_fonts.FONT_LARGE_PINK)
G1000TRKangle.setTextFormat(TXT_FMT_3DIG_PREC0_0PADDED)
G1000TRKangle.setDisplayUnit(chr(176))
G1000TRKangle.setTextDataSource(XPlaneDataDispatcher,(17,3))

NAV_COM_TEXT_WHITE = G1000_fonts.FONT_LARGE_WHITE
NAV_COM_TEXT_GREY = G1000_fonts.FONT_LARGE_GREY

#----------------------------------------------------
#	NAV 1
G1000NAV1Frequ = XPinstrument.TextField(NAV_COM_TEXT_WHITE)
G1000NAV1Frequ.setTextFormat(TXT_FMT_3DIG_PREC2)
G1000NAV1Frequ.setTextDataSource(XPlaneDataDispatcher,(97,0),conversionFunctions.divideby100)
G1000NAV1FrequStdby = XPinstrument.TextField(NAV_COM_TEXT_GREY)
G1000NAV1FrequStdby.setTextFormat(TXT_FMT_3DIG_PREC2)
G1000NAV1FrequStdby.setTextDataSource(XPlaneDataDispatcher,(97,1),conversionFunctions.divideby100)

#----------------------------------------------------
#	NAV 2
G1000NAV2Frequ = XPinstrument.TextField(NAV_COM_TEXT_WHITE)
G1000NAV2Frequ.setTextFormat(TXT_FMT_3DIG_PREC2)
G1000NAV2Frequ.setTextDataSource(XPlaneDataDispatcher,(97,4),conversionFunctions.divideby100)
G1000NAV2FrequStdby = XPinstrument.TextField(NAV_COM_TEXT_GREY)
G1000NAV2FrequStdby.setTextFormat(TXT_FMT_3DIG_PREC2)
G1000NAV2FrequStdby.setTextDataSource(XPlaneDataDispatcher,(97,5),conversionFunctions.divideby100)

#----------------------------------------------------
#	COM 1
G1000COM1Frequ = XPinstrument.TextField(NAV_COM_TEXT_WHITE)
G1000COM1Frequ.setTextFormat(TXT_FMT_3DIG_PREC3)
G1000COM1Frequ.setTextDataSource(XPlaneDataDispatcher,(96,0),conversionFunctions.divideby100)
G1000COM1FrequStdby = XPinstrument.TextField(NAV_COM_TEXT_GREY)
G1000COM1FrequStdby.setTextFormat(TXT_FMT_3DIG_PREC3)
G1000COM1FrequStdby.setTextDataSource(XPlaneDataDispatcher,(96,1),conversionFunctions.divideby100)

#----------------------------------------------------
#	COM 2
G1000COM2Frequ = XPinstrument.TextField(NAV_COM_TEXT_WHITE)
G1000COM2Frequ.setTextFormat(TXT_FMT_3DIG_PREC3)
G1000COM2Frequ.setTextDataSource(XPlaneDataDispatcher,(96,3),conversionFunctions.divideby100)
G1000COM2FrequStdby = XPinstrument.TextField(NAV_COM_TEXT_GREY)
G1000COM2FrequStdby.setTextFormat(TXT_FMT_3DIG_PREC3)
G1000COM2FrequStdby.setTextDataSource(XPlaneDataDispatcher,(96,4),conversionFunctions.divideby100)


G1000Horizon.setRotateTexture(True)
G1000Horizon.setTranslateTexture(True)
G1000Horizon.enableRotation (XPlaneDataDispatcher,(17,1),[ [-180,-180],[180,180]])
G1000Horizon.enableTranslation (XPlaneDataDispatcher,(17,0),[ [-70,-398],[70,398]],False,True)
G1000Horizon.setRotationCenter((981,1109))

G1000PitchScale.setRotateTexture(True)
G1000PitchScale.setTranslateTexture(True)
G1000PitchScale.enableRotation (XPlaneDataDispatcher,(17,1),[ [-180,-180],[180,180]])
G1000PitchScale.enableTranslation (XPlaneDataDispatcher,(17,0),[ [-70,-398],[70,398]],False,True)
G1000PitchScale.setRotationCenter((981,1109))

G1000BankIndicator.setRotateTexture(True)
G1000BankIndicator.enableRotation (XPlaneDataDispatcher,(17,1),[ [-180,-180],[180,180]])
G1000BankIndicator.setRotationCenter((981,1109))

G1000 = XPinstrument.STinstrument([0,0],(835,626),"G1000")
G1000.addImage(G1000Horizon, (200,200), False)
G1000.addImage(G1000PitchScale, (470,500), False)
G1000.addImage(G1000BankIndicator, (200,200), False)

G1000.addImage(G1000Bug,(200,200), False)
G1000.addImage(G1000topBar,(200,781), False)

#--- NAV
G1000.addImage(G1000NAV1Frequ, (247,803), False)
G1000.addImage(G1000NAV1FrequStdby, (338,803), False)
G1000.addImage(G1000NAV2Frequ, (247,782), False)
G1000.addImage(G1000NAV2FrequStdby, (338,782), False)

#--- COM
G1000.addImage(G1000COM1Frequ, (825,803), False)
G1000.addImage(G1000COM1FrequStdby, (915,803), False)
G1000.addImage(G1000COM2Frequ, (825,782), False)
G1000.addImage(G1000COM2FrequStdby, (915,782), False)

G1000.addImage(G1000TRKangle, (770,803), False)

VNE = 163 # never exceed speed
VSO = 40 # stall speed, flaps extended, power off
VSI = 48 # stall speed, flaps retracted, power off
VFE = 90 # max flaps extended speed
VNO = 129 # max structural cruising speed (yellow)

Vx = 62 # best angle of climb
Vy = 74 # bext climb speed
Vr = 55 # take off speed
Vg = 68 # Best glide speed

G1000AirspeedIndicator = G1000AirspeedIndicator.G1000AirspeedIndicator([324,432],(95,304),XPlaneDataDispatcher,VNE,VSO,VSI,VFE,VNO, Vx, Vy, Vr, Vg)
jetVSI = True
G1000Altimeter = G1000Altimeter.G1000Altimeter([773,432],(142,324),XPlaneDataDispatcher,jetVSI)
G1000HSI = G1000HSI.G1000HSI([415,188],[320,320],XPlaneDataDispatcher)


charset = ""
for i in range(32,256):
	charset+= chr(i)
	
#------------------------------------------------------------------------------------------
#	MAIN LOOP
#------------------------------------------------------------------------------------------

testValue = 0.0
running = True

while running:
	try:
		#print "pygame main loop running..."
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_KP_PLUS:
					testValue +=1
				if event.key == pygame.K_KP_MINUS:
					testValue -=1
				if event.key == pygame.K_UP:
					testValue +=10
				if event.key == pygame.K_DOWN:
					testValue -=10
				if event.key == pygame.K_PAGEUP:
					testValue +=100
				if event.key == pygame.K_PAGEDOWN:
					testValue -=100
		
		clock.tick(150)
		text = "FPS: {0:.2f}".format(clock.get_fps())
		print testValue	
		#G1000Horizon.setTestValue(testValue)
		#G1000PitchScale.setTestValue(testValue)
		#G1000BankIndicator.setTestValue(testValue)
		G1000Altimeter.setTestValue(testValue)
		G1000AirspeedIndicator.setTestValue(testValue)
		#XPlaneDataDispatcher.printData(3)
		pygame.display.set_caption(text)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		#OpenGLlib.refresh2d(ScreenWidth,ScreenHeight)
		
		G1000.draw()
		G1000AirspeedIndicator.draw()
		G1000Altimeter.draw()
		G1000HSI.draw()
		
		
		pygame.display.flip()
	except KeyboardInterrupt:
		running = False

logging.info("Quitting")		
XPlaneDataDispatcher.quit()
logging.info("quitting pygame")
pygame.display.quit()
logging.info("bye")
