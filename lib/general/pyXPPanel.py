
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

## @brief This is the main class of the application: It initialises and creates the instrument panel window, holds all the instruments and manages the main loop. 
# The constructor will 1/ load the config.ini file 2/ Initialise the GLFW environment and OpenGL context 3/ initialise the UDP connectivity to XPLane.   
# The class also handles the keyboard and mouse callbacks and allows the user to register callbacks for these events which it will call at run time
# 
# Note the following keys are handled by the application by default:  
# ESCAPE : quit the application
# Keypad '*' 	: toggles the small increment by which the test value is changed (0.1 or 1.0)
# Keypad '+' 	: increase the test value by the small increment (0.1 or 1.0)
# Keypad '-' 	: decrease the test value by the small increment (0.1 or 1.0)
# up arrow 		: increase the test value by 10.0
# down arrow 	: decrease the test value by 10.0
# page up 		: increase the test value by 100.0
# page down		: decrease the test value by 100.0
#
# Simple Example:
#
# @code
# from lib.general import pyXPPanel
# myInstrumentPanel = pyXPPanel.pyXPPanel()		# initialises a new empty instrument panel. This will load the config file, initialise the openGL context and create a new window, and initialise UDP connectivity to XPlane. 
# # initialise instruments and add them to the panel
# myInstrumentPanel.run()		# start the application's main loop
# @endcode
#
class pyXPPanel():
	width = 640
	height = 480
	fullscreen = False
	bufferSwapInterval = 1
	
	IP = "127.0.0.1"		# specify the address of the PC you are running this on
	Port = 49006	
	XPlaneDataServer = None
	arduinoSerialConnection = None
	
	drawCallbackFuncs = []
	
	testValue = 0.0
	smallTestValueIncrement = 1.0
	
	#*******************************************************************************************************
	#
	# CONSTRUCTOR
	#
	#*******************************************************************************************************
	
	## constructor: Initialises a new empty instrument panel: load the config file, initialise the openGL context and create a new window, and initialise UDP connectivity to XPlane.
	# The config file allows to set the graphic options (window size/fullscreen etc), the network options for XPlane (IP, port....) and the arduino settings if connected to an arduino over USB
	# It is by default expected to be named config.ini, and located in the same folder as the main python script used to launch the application. 
	# A custom config file can be passed by argument to the script using option -c. for example: python myMainPanelScript.py -c myconfigfile.ini
	#
	
	def __init__(self):
		self._loadConfigFile(CONFIG_FILE)
		self._initDisplay() # initialise GLFW window and OpenGL context
		self._initXPlaneDataServer() # initialise UDP connectivity to XPlane
		

	#*******************************************************************************************************
	#
	# PRIVATE METHODS
	#
	#*******************************************************************************************************
	
	## Load the configuration file: private method called by the constructor, not intended to be called outside of the class.  
	# The config file is by default expected to be named config.ini, and located in the same folder as the main python script used to launch the application. 
	# A custom config file can be passed by argument to the script using option -c. for example: python myMainPanelScript.py -c myconfigfile.ini
	#
	def _loadConfigFile(self, configFile):
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
		self.XPlaneComputerName = Config.get("Network","XPlaneComputerName")
		
		#------------------------------------------------------------------------------------------
		#	Arduino configuration
		#------------------------------------------------------------------------------------------
		try:
			self.ARD_PORT = Config.get("Arduino","PORT")
			self.ARD_BAUD = Config.getint("Arduino","BAUD")
		except :
			logging.warning ( "Arduino configuration section not found, please include if you want to connect an Arduino")
	
	## Initialise and create the main window: Init the GLFW library, OpenGL context, display options and internal callbacks for keyboard and mouse events - Private method called by the constructor, do not call directly.  
	# the graphic options (window size/fullscreen etc) are defined in the config file
	#
	def _initDisplay(self):
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
		glfw.glfwSetFramebufferSizeCallback(self.window, self._framebuffer_size_callback)
		
		glfw.glfwSetKeyCallback(self.window, self._on_key)
		self.keyCallBacks = []
		
		glfw.glfwSetCharCallback(self.window, self._on_char)
		self.charCallBacks = []
		
		glfw.glfwSetMouseButtonCallback(self.window, self._on_mouse_button)
		self.mouseButtonCallBacks = []
		
		glfw.glfwSetCursorPosCallback(self.window, self._on_cursor_pos)
		self.mouseCursorPosCallBacks = []
		
		glfw.glfwSetScrollCallback(self.window, self._scroll_callback)
		self.scrollCallBacks = []
		
		self.frameBufferWidth, self.frameBufferHeight = glfw.glfwGetFramebufferSize(self.window)
		logging.info("Framebuffer size: %sx%s",  self.frameBufferWidth, self.frameBufferHeight)
		gl3lib.screenWidth = self.frameBufferWidth
		gl3lib.screenHeight = self.frameBufferHeight
		gl3lib.PROJ_MATRIX[0,0] = 2.0/self.frameBufferWidth
		gl3lib.PROJ_MATRIX[1,1] = 2.0/self.frameBufferHeight
		
		fonts.initFonts()
		
		# ADF ADF indicator
		self.receivingXPdataText = graphicsGL3.TextField(fonts.VERA_20PT_BOLD_ORANGE)
		self.receivingXPdataText.setText('-- !! Not receiving any data from XPlane !! --')
		self.receivingXPdataText.setBackgroundColor((1.0,1.0,1.0,0.75))
		self.receivingXPdataText.setPosition((20,20))

	## Initialise UDP connectivity to XPlane; Creates a new XPlaneUDPServer instance and starts it - Private method called by the constructor, not intended to be called outside of the class.  
	# the network options for XPlane (IP, port....) are defined in the config file
	#
	def _initXPlaneDataServer(self):
		XPlaneUDPServer.pyXPUDPServer.initialiseUDP((self.IP,self.Port), (self.XPlaneIP,self.XPlanePort), self.XPlaneComputerName)
		XPlaneUDPServer.pyXPUDPServer.start()
		self.XPlaneDataServer = XPlaneUDPServer.pyXPUDPServer
	
	## Private callback for the GLFW text input event: Will call all user callbacks registered via the registerCharCallback() method - Internal method, do not call directly.
	# the class registers this callback at construction time
	#
	def _on_char(self, window, codepoint):
		for callback in self.charCallBacks:
			callback(codepoint)
	
	## Private callback for the GLFW key event: Handles key presses to quit and set the test value (see details below) Also calls all user callbacks registered via the registerKeyCallback() method - Internal method, do not call directly.
	# the class registers this callback at construction time
	# ESCAPE : quit the application
	# Keypad '*' 	: toggles the small increment by which the test value is changed (0.1 or 1.0)
	# Keypad '+' 	: increase the test value by the small increment (0.1 or 1.0)
	# Keypad '-' 	: decrease the test value by the small increment (0.1 or 1.0)
	# up arrow 		: increase the test value by 10.0
	# down arrow 	: decrease the test value by 10.0
	# page up 		: increase the test value by 100.0
	# page down		: decrease the test value by 100.0
	#
	
	def _on_key(self, window, key, scancode, action, mods):
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
	
	## Private callback for the GLFW cursor position event: Will call all user callbacks registered via the registerMouseCursorPosCallback() method - Internal method, do not call directly.
	# the class registers this callback at construction time
	#
	def _on_cursor_pos(self, window, xpos, ypos):
		#logging.debug("cursor pos callback: x, y: %s, %s", xpos, ypos)
		for callback in self.mouseCursorPosCallBacks:
			callback(xpos, ypos)
	
	## Private callback for the GLFW mouse button event: Will call all user callbacks registered via the registerMouseButtonCallback() method - Internal method, do not call directly.
	# the class registers this callback at construction time
	#
	def _on_mouse_button(self, window, button, action, mods):
		#print("Mouse button callback:", button)
		for callback in self.mouseButtonCallBacks:
			callback(button, action, mods)
	
	## Private callback for the GLFW mouse scroll event: Will call all user callbacks registered via the registerScrollCallback() method - Internal method, do not call directly.
	# the class registers this callback at construction time
	#
	def _scroll_callback(self, window, xoffset, yoffset):
		#print("Mouse scroll callback: x", xoffset, "y", yoffset)
		for callback in self.scrollCallBacks:
			callback(xoffset, yoffset)
			
	## Private callback to handle a window resize event - Internal method, do not call directly.
	# the class registers this callback at construction time
	#
	def _framebuffer_size_callback(self, window, width,  height):
		logging.debug("width, height: %s x %s", width, height )
		if self.fullscreen != True:
			self.frameBufferWidth = width
			self.frameBufferHeight = height
			gl.glViewport(0, 0, width, height)
			gl3lib.screenWidth = self.frameBufferWidth
			gl3lib.screenHeight = self.frameBufferHeight
			gl3lib.PROJ_MATRIX[0,0] = 2.0/width
			gl3lib.PROJ_MATRIX[1,1] = 2.0/height
			
	#*******************************************************************************************************
	#
	# PUBLIC METHODS
	#
	#*******************************************************************************************************
	
	## Initialise USB connection to an Arduino Creates a new ArduinoSerial instance and starts it.   
	# the options for the Arduino connection (USB port, BAUD....) are defined in the config file
	#
	def initArduinoSerialConnection(self):
		self.arduinoSerialConnection = arduinoSerial.ArduinoSerial(self.ARD_PORT, self.ARD_BAUD, self.XPlaneDataServer)
		self.arduinoSerialConnection.start()
		
	## Register a callback for the GLFW text input event: Your callback function will be called if text is input and receive the Unicode code point.
	# @param charCallBack: user callback function for this event
	# The callback function receives Unicode code points for key events that would have led to regular text input and generally behaves as a standard text field on that platform
	# Example callback function: 
	# @code
	# def charCallback(codepoint):
	#	print(codepoint)
	# @endcode
	#
	def registerCharCallback(self, charCallBack):
		self.charCallBacks.append(charCallBack)
	
	## Register a callback for the GLFW key event: Your callback function will be called if a key is pressed. 
	# Refer to the GLFW documentation for full details http://www.glfw.org/docs/latest/input_guide.html#input_key
	# @param keyCallBack: user callback function for this event.
	# Example callback function: 
	# @code 
	# def keyCallBack(window, key, scancode, action, mods):
	# 	if key == glfw.GLFW_KEY_ESCAPE and action == glfw.GLFW_PRESS:   # ESCAPE key has been pressed 
	# @endcode
	#
	def registerKeyCallback(self, keyCallBack):
		self.keyCallBacks.append(keyCallBack)
	
	
	## Register a callback for the GLFW Cursor position event: Your callback function will be called at run time if the cursor position moves. 
	# The callback functions receives the cursor position, measured in screen coordinates but relative to the top-left corner of the window client area. On platforms that provide it, the full sub-pixel cursor position is passed on
	# Refer to the GLFW documentation for full details: http://www.glfw.org/docs/latest/input_guide.html#cursor_pos
	# @param mouseCursorPosCallBack: user callback function for this event.
	# Example callback function: 
	# @code
	# def mouseCursorPosCallback(xpos, ypos):
	# @endcode
	#
	def registerMouseCursorPosCallback(self, mouseCursorPosCallBack):
		self.mouseCursorPosCallBacks.append(mouseCursorPosCallBack)
		
	## Register a callback for the GLFW Mouse button event: Your callback function will be called at run time if the mouse is clicked. 
	# The callback function receives the mouse button, button action and modifier bits.
	# Refer to the GLFW documentation for full details: http://www.glfw.org/docs/latest/input_guide.html#input_mouse_button
	# @param mouseButtonCallBack: user callback function for this event.
	# Example callback function: 
	# @code
	# def mouseButtonCallBack(button, action, mods):
	# @endcode
	#
	def registerMouseButtonCallback(self, mouseButtonCallBack):
		self.mouseButtonCallBacks.append(mouseButtonCallBack)
	
	## Register a callback to be notified if the mouse is scrolled. 
	# The callback function receives two-dimensional scroll offsets.
	# Refer to the GLFW documentation for full details: http://www.glfw.org/docs/latest/input_guide.html#scrolling
	# @param scrollCallBack: user callback function for this event.
	# Example callback function: 
	# @code
	# def scrollCallBack(xoffset, yoffset):
	# @endcode
	#
	def registerScrollCallback(self, scrollCallBack):
		self.scrollCallBacks.append(scrollCallBack)
	
	## Register a callback function to be executed each time the main loop redraws the screen. 
	# @param drawCallbackFunc: user callback function.
	# 
	def setDrawCallback(self, drawCallbackFunc):
		self.drawCallbackFuncs.append(drawCallbackFunc)
	
	## Register a callback function to be executed each time the main loop redraws the screen. 
	# @param drawCallbackFunc: user callback function.
	# 
	def addDrawable(self, drawCallbackFunc):
		self.drawCallbackFuncs.append(drawCallbackFunc)
	
	
	## Starts the main application loop, call once all initialisation is done.
	# 
	def run(self):

		lastFPStime = time.time()
		currentTime = lastFPStime
		counter = 0
		lastFPS = 0.0
		FPStext = "FPS:"

		# Loop until the user closes the window
		while not glfw.glfwWindowShouldClose(self.window):
			
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

			for drawCallback in self.drawCallbackFuncs:
				drawCallback()
			
			if XPlaneUDPServer.pyXPUDPServer.XPalive == True:
				self.receivingXPdataText.setVisible(False)
			else:
				self.receivingXPdataText.setVisible(True)
			self.receivingXPdataText.draw()
			
			# Swap front and back buffers
			glfw.glfwSwapBuffers(self.window)
			# Poll for and process events
			glfw.glfwPollEvents()
		
		logging.info("Bye")
		XPlaneUDPServer.pyXPUDPServer.quit()
		
		if self.arduinoSerialConnection != None:
			self.arduinoSerialConnection.quit()
			
		glfw.glfwTerminate()
