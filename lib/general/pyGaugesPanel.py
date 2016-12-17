
#**************************************************************************************************************************
#
#   Imports
#
#**************************************************************************************************************************
import sys, getopt

LOGGING_LEVEL = "INFO"
CONFIG_FILE = "./config.ini"

try:
	opts, args = getopt.getopt(sys.argv[1:],"c:l:")
except getopt.GetoptError:
	print("ERROR:No args passed")

for opt, arg in opts:
	if opt == '-l':
		LOGGING_LEVEL = arg
		print ("logging level:", LOGGING_LEVEL)
	if opt == '-c':
		print('Config file provided')
		CONFIG_FILE = arg
		
import logging
#------------------------------------------------------------------------------------------
#	Logging configuration
#------------------------------------------------------------------------------------------

LOGGING_FORMAT= '%(asctime)s %(levelname)-8s %(name)-20s %(funcName)-20s  %(message)s'
if LOGGING_LEVEL == "DEBUG": 
	logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)
else :
	logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
	
logging.info("#########################################################################################################")
logging.info("#")
logging.info("#                    STARTING UP")
logging.info("#")
logging.info("#########################################################################################################")


PYTHON_VERSION = sys.version_info[0] 
if PYTHON_VERSION == 3:
	from configparser import *
elif PYTHON_VERSION == 2:
	from ConfigParser import *

import OpenGL
OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_LOGGING = False
import OpenGL.GL as gl

from lib.glfw import glfw
import time

from lib.network import XPlaneUDPServer
from lib.arduinoSerial import arduinoSerial

from lib.graphics import OpenGL3lib as gl3lib
from lib.graphics import graphicsGL3
from lib.graphics import fonts


class pyGaugesPanel():
	width = 640
	height = 480
	fullscreen = False
	bufferSwapInterval = 1
	
	IP = "127.0.0.1"		# specify the address of the PC you are running this on
	Port = 49006	
	XPlaneDataServer = None
	arduinoSerialConnection = None
	
	drawCallbackFunc = None
	
	testValue = 0.0
	smallTestValueIncrement = 1.0
	
	def __init__(self):
		self.loadConfigFile(CONFIG_FILE)

	
	def loadConfigFile(self, configFile):
		Config = ConfigParser()
		Config.read(configFile)
		
		#------------------------------------------------------------------------------------------
		#	Graphics configuration
		#------------------------------------------------------------------------------------------
		self.fullscreen = Config.getboolean("Graphics","Fullscreen")
		self.monitorID = Config.getint("Graphics","MonitorID")
		self.width = Config.getint("Graphics","ScreenWidth")
		self.height = Config.getint("Graphics","ScreenHeight")
		self.bufferSwapInterval = Config.getint("Graphics","BufferSwapInterval")
		self.bgdColor_R = Config.getfloat("Graphics","BgdColor_R")
		self.bgdColor_G = Config.getfloat("Graphics","BgdColor_G")
		self.bgdColor_B = Config.getfloat("Graphics","BgdColor_B")
		
		#------------------------------------------------------------------------------------------
		#	Network configuration
		#------------------------------------------------------------------------------------------
		self.IP = Config.get("Network","IP")
		self.Port = Config.getint("Network","Port")
		self.XPlaneIP = Config.get("Network","XPlaneIP")
		self.XPlanePort = Config.getint("Network","XPlanePort")
		
		#------------------------------------------------------------------------------------------
		#	Arduino configuration
		#------------------------------------------------------------------------------------------
		try:
			self.ARD_PORT = Config.get("Arduino","PORT")
			self.ARD_BAUD = Config.getint("Arduino","BAUD")
		except :
			logging.warning ( "Arduino configuration section not found, please include if you want to connect an Arduino")
	
	def initDisplay(self):
		# Initialize the glfw library
		if not glfw.glfwInit():
			sys.exit()

		# Attempt to create a window in core OpenGL mode 
		glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MAJOR, 3)
		glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MINOR, 2)
		glfw.glfwWindowHint(glfw.GLFW_OPENGL_FORWARD_COMPAT, gl.GL_TRUE);
		glfw.glfwWindowHint(glfw.GLFW_OPENGL_PROFILE, glfw.GLFW_OPENGL_CORE_PROFILE)
		glfw.glfwWindowHint(glfw.GLFW_AUTO_ICONIFY, gl.GL_FALSE)
		
		logging.info("testing monitor")
		monitors = None
		#print ( glfw.glfwGetMonitors())
		if self.fullscreen == True:
			logging.info("I am full screen")
			monitors = glfw.glfwGetMonitors()
			logging.info("I have the monitors, %s", monitors)
			
			monitorVideoModes = glfw.glfwGetVideoModes(monitors[0])
			logging.info("monitorVideoModes: %s", monitorVideoModes)
			monitor_id = 0
			if self.monitorID >=0 and self.monitorID <len(monitors):
				monitor_id = self.monitorID
			
			#logging.info("Entering full screen, screen width: %s, height %s", monitorVideoMode[0], monitorVideoMode[1])
			self.window = glfw.glfwCreateWindow(self.width, self.height, str.encode("pyGaugesPanel"), monitors[monitor_id], None)
		else:
			self.window = glfw.glfwCreateWindow(self.width, self.height, str.encode("pyGaugesPanel"), None, None)
		
		if not self.window:
			logging.error("Could not create window, your version of OpenGL is not supported, exiting!")
			glfw.glfwTerminate()
			sys.exit()
	
		# Make the window's context current
		glfw.glfwMakeContextCurrent(self.window)
		self.backgroundColor =(self.bgdColor_R, self.bgdColor_G, self.bgdColor_B)
		
		logging.info("GL version: %s",gl.glGetString(gl.GL_VERSION))
		logging.info("GLSL version: %s",gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION))

		gl.glClearColor(self.backgroundColor[0], self.backgroundColor[1], self.backgroundColor[2], 1.0)
		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		
		glfw.glfwSwapInterval(self.bufferSwapInterval)
		
		# callback handlers
		glfw.glfwSetFramebufferSizeCallback(self.window, self.framebuffer_size_callback)
		
		glfw.glfwSetKeyCallback(self.window, self.on_key)
		self.keyCallBacks = []
		
		glfw.glfwSetCharCallback(self.window, self.on_char)
		self.charCallBacks = []
		
		glfw.glfwSetMouseButtonCallback(self.window, self.on_mouse_button)
		self.mouseButtonCallBacks = []
		
		glfw.glfwSetCursorPosCallback(self.window, self.on_cursor_pos)
		self.mouseCursorPosCallBacks = []
		
		glfw.glfwSetScrollCallback(self.window, self.scroll_callback)
		self.scrollCallBacks = []
		
		self.frameBufferWidth, self.frameBufferHeight = glfw.glfwGetFramebufferSize(self.window)
		logging.info("Framebuffer size: %sx%s",  self.frameBufferWidth, self.frameBufferHeight)
		gl3lib.screenWidth = self.frameBufferWidth
		gl3lib.screenHeight = self.frameBufferHeight
		gl3lib.PROJ_MATRIX[0,0] = 2.0/self.frameBufferWidth
		gl3lib.PROJ_MATRIX[1,1] = 2.0/self.frameBufferHeight
		
		fonts.initFonts()

	def initXPlaneDataServer(self):
		self.XPlaneDataServer = XPlaneUDPServer.XPlaneUDPServer((self.IP,self.Port), (self.XPlaneIP,self.XPlanePort))
		self.XPlaneDataServer.start()
	
	def initArduinoSerialConnection(self):
		self.arduinoSerialConnection = arduinoSerial.ArduinoSerial(self.ARD_PORT, self.ARD_BAUD, self.XPlaneDataServer)
		self.arduinoSerialConnection.start()
	
	def on_char(self, window, codepoint):
		for callback in self.charCallBacks:
			callback(codepoint)
			
	def registerCharCallback(self, charCallBack):
		self.charCallBacks.append(charCallBack)
	
	def on_key(self, window, key, scancode, action, mods):
		if key == glfw.GLFW_KEY_ESCAPE and action == glfw.GLFW_PRESS:
			glfw.glfwSetWindowShouldClose(window,1)
		
		if key == glfw.GLFW_KEY_KP_MULTIPLY and action == glfw.GLFW_PRESS:
			if self.smallTestValueIncrement == 1.0:
				self.smallTestValueIncrement = 0.1
			else:
				self.smallTestValueIncrement = 1.0
		
		if key == glfw.GLFW_KEY_KP_ADD and action == glfw.GLFW_PRESS:
			self.testValue += self.smallTestValueIncrement
		if key == glfw.GLFW_KEY_KP_SUBTRACT and action == glfw.GLFW_PRESS:
			self.testValue -= self.smallTestValueIncrement
		if key == glfw.GLFW_KEY_UP and action == glfw.GLFW_PRESS:
			self.testValue +=10
		if key == glfw.GLFW_KEY_DOWN and action == glfw.GLFW_PRESS:
			self.testValue -=10
		if key == glfw.GLFW_KEY_PAGE_UP and action == glfw.GLFW_PRESS:
			self.testValue +=100
		if key == glfw.GLFW_KEY_PAGE_DOWN and action == glfw.GLFW_PRESS:
			self.testValue -=100
		print("Test value: ", self.testValue)
		
		for callback in self.keyCallBacks:
			callback(key, scancode, action, mods)
			
	def registerKeyCallback(self, keyCallBack):
		self.keyCallBacks.append(keyCallBack)
	
	def on_cursor_pos(self, window, xpos, ypos):
		#logging.debug("cursor pos callback: x, y: %s, %s", xpos, ypos)
		for callback in self.mouseCursorPosCallBacks:
			callback(xpos, ypos)
			
	def registerMouseCursorPosCallback(self, mouseCursorPosCallBack):
		self.mouseCursorPosCallBacks.append(mouseCursorPosCallBack)
		
	def on_mouse_button(self, window, button, action, mods):
		#print("Mouse button callback:", button)
		for callback in self.mouseButtonCallBacks:
			callback(button, action, mods)
	
	def registerMouseButtonCallback(self, mouseButtonCallBack):
		self.mouseButtonCallBacks.append(mouseButtonCallBack)
	
	def scroll_callback(self, window, xoffset, yoffset):
		#print("Mouse scroll callback: x", xoffset, "y", yoffset)
		for callback in self.scrollCallBacks:
			callback(xoffset, yoffset)
			
	def registerScrollCallback(self, scrollCallBack):
		self.scrollCallBacks.append(scrollCallBack)
	
	def framebuffer_size_callback(self, window, width,  height):
		logging.debug("width, height: %s x %s", width, height )
		if self.fullscreen != True:
			self.frameBufferWidth = width
			self.frameBufferHeight = height
			gl.glViewport(0, 0, width, height)
			gl3lib.screenWidth = self.frameBufferWidth
			gl3lib.screenHeight = self.frameBufferHeight
			gl3lib.PROJ_MATRIX[0,0] = 2.0/width
			gl3lib.PROJ_MATRIX[1,1] = 2.0/height
	
	def setDrawCallback(self, drawCallbackFunc):
		self.drawCallbackFunc = drawCallbackFunc
		
	def run(self):

		lastFPStime = time.time()
		currentTime = lastFPStime
		counter = 0
		lastFPS = 0.0
		FPStext = "FPS:"

		# Loop until the user closes the window
		while not glfw.glfwWindowShouldClose(self.window):
			#print("render loop")# Render here
			#print("airspeed:", self.XPlaneDataServer.getData(3,0))

			counter += 1
			currentTime = time.time()
			if currentTime - lastFPStime >= 0.2:
				FPS = float(counter/(currentTime - lastFPStime))
				FPStext = "FPS:" + "{0:.2f}".format(FPS)
				#print(FPStext)
				lastFPStime = currentTime
				counter = 0
			glfw.glfwSetWindowTitle(self.window, str.encode(FPStext))
				
			gl.glClear(gl.GL_COLOR_BUFFER_BIT)

			if self.drawCallbackFunc != None:
				self.drawCallbackFunc()
			
			# Swap front and back buffers
			glfw.glfwSwapBuffers(self.window)
			# Poll for and process events
			glfw.glfwPollEvents()
		
		logging.info("Bye")
		if self.XPlaneDataServer != None:
			self.XPlaneDataServer.quit()
		
		if self.arduinoSerialConnection != None:
			self.arduinoSerialConnection.quit()
			
		glfw.glfwTerminate()
