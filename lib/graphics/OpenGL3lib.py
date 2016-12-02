import pygame
import os
import math
import logging
import itertools
import copy 
 
import sys
import platform
import ctypes
import numpy as np

import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu
from OpenGL.GL.shaders import *
from PIL import Image

np.set_printoptions(threshold=np.nan)

COLOR_WHITE 	= (1.0,1.0,1.0,1.0)
COLOR_PINK 		= (1.0,0,1.0,1.0)
COLOR_GREY 		= (0.5,0.5,0.5,1.0)
COLOR_TURQUOISE = (0,1.0,1.0,1.0)
COLOR_RED 		= (1.0,0,0,1.0)
COLOR_GREEN 	= (0,213.0/255.0,0,1.0)
COLOR_BLUE 		= (0.0,0,1.0,1.0)
COLOR_BLACK 	= (0.0,0.0,0.0,1.0)

screenWidth = 0
screenHeight = 0

PROJ_MATRIX = np.identity(4)
PROJ_MATRIX[0,3] = -1.0
PROJ_MATRIX[1,3] = -1.0

class IdentityMatrix():
	def __init__(self):
		self.identity = np.identity(4)
	def returnIdentity(self):
		return self.identity

#IDENTITY_MATRIX = IdentityMatrix()
IDENTITY_MATRIX = np.identity(4)

def returnOpenGLcoord(pygameCoord):
	global screenHeight
	
	return (pygameCoord[0],screenHeight-pygameCoord[1])

def initializeDisplay(w, h, fullscreen, backgroundColor =(0,0,0)):
	
	pygame.display.init()
	
	PROJ_MATRIX[0,0] = 2.0/w
	PROJ_MATRIX[1,1] = 2.0/h

	print ("Projection Matrix: \n", PROJ_MATRIX)
	
	global screenWidth
	global screenHeight
	
	screenWidth = w
	screenHeight = h
	
	displayOptions = "pygame.OPENGL|pygame.HWSURFACE|pygame.DOUBLEBUF"
	if fullscreen == True :
		pygame.display.set_mode((w,h), pygame.OPENGL|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
	else:
		pygame.display.set_mode((w,h), pygame.OPENGL|pygame.HWSURFACE|pygame.DOUBLEBUF)
	
	pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS,4)
	pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES,4)
	#glut.glutInitDisplayMode(glut.GLUT_3_2_CORE_PROFILE | glut.GLUT_DOUBLE | glut.GLUT_RGBA )
	print("GL version:",gl.glGetString(gl.GL_VERSION))
	gl.glClearColor(backgroundColor[0], backgroundColor[1], backgroundColor[2], 1.0)
	gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
	gl.glShadeModel(gl.GL_SMOOTH)
	# this puts us in quadrant 1, rather than quadrant 4
	gl.glViewport(0, 0, w, h)
	glu.gluOrtho2D(0, w, 0, h)
	
	# set up texturing
	gl.glEnable(gl.GL_TEXTURE_2D)
	gl.glEnable(gl.GL_BLEND)
	gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

def reshape(width,height):

	gl.glViewport(0, 0, width, height)
	glu.gluOrtho2D(0, width, 0, height)
	
	PROJ_MATRIX[0,0] = 2.0/width
	PROJ_MATRIX[1,1] = 2.0/height

	print ("Projection Matrix: \n", PROJ_MATRIX)
	

# Build & activate program
# --------------------------------------

def buildProgram(vertex_code,fragment_code):

	# Request a program and shader slots from GPU
	program  = gl.glCreateProgram()
	vertex   = gl.glCreateShader(gl.GL_VERTEX_SHADER)
	fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

	# Set shaders source
	gl.glShaderSource(vertex, [vertex_code])
	gl.glShaderSource(fragment, [fragment_code])

	# Compile shaders
	gl.glCompileShader(vertex)
	gl.glCompileShader(fragment)

	message = gl.glGetShaderInfoLog(vertex)
	print("Vertex shader compilation messages: ", message)
	logging.info('Vertex shader message: %s', message)
	message = gl.glGetShaderInfoLog(fragment)
	logging.info('Fragment shader message: %s' % message)
	# Attach shader objects to the program
	gl.glAttachShader(program, vertex)
	gl.glAttachShader(program, fragment)

	# Build program
	gl.glLinkProgram(program)
	
	linkstatus = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
	if linkstatus != gl.GL_TRUE:
		print( gl.glGetProgramInfoLog(program).decode('ASCII'))

	# Get rid of shaders (no more needed)
	gl.glDetachShader(program, vertex)
	gl.glDetachShader(program, fragment)

	# Make program the default program
	gl.glUseProgram(program)
	
	return program
	

def buildProgramBuffer(program, data):
	# Build data
	# --------------------------------------
	


	# Build buffer
	# --------------------------------------

	# Request a buffer slot from GPU
	buffer = gl.glGenBuffers(1)

	# Make this buffer the default one
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

	# Upload data
	gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)


	# Bind attributes
	# --------------------------------------
	stride = data.strides[0]
	offset = ctypes.c_void_p(0)
	print ("offset: ",offset)
	loc = gl.glGetAttribLocation(program, "position")
	gl.glEnableVertexAttribArray(loc)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
	gl.glVertexAttribPointer(loc, 3, gl.GL_FLOAT, False, stride, offset)

	offset = ctypes.c_void_p(data.dtype["position"].itemsize)
	print ("offset: ",offset)
	loc = gl.glGetAttribLocation(program, "color")
	gl.glEnableVertexAttribArray(loc)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
	gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)
	
	return buffer

class GL_Texture():

	def __init__(self,imagefile, CLAMPTOBORDER = False):
		self.texture = gl.glGenTextures(1)
		self.loadImageToTexture(imagefile, CLAMPTOBORDER)
		
	def loadImageToTexture(self, imagefile, CLAMPTOBORDER = False):
		self.name = imagefile
		logging.debug("loading image file to texture: %s", imagefile)
		imagefilePath = os.path.join(os.path.dirname(__file__), '../../',imagefile)
		im = Image.open(imagefilePath)
		
		try:
			# get image meta-data (dimensions) and data
			self.width, self.height, textureData = im.size[0], im.size[1], im.tobytes("raw", "RGBA", 0, -1)
		except SystemError:
			# has no alpha channel, synthesize one, see the
			# texture module for more realistic handling
			self.width, self.height, textureData = im.size[0], im.size[1], im.tobytes("raw", "RGBX", 0, -1)
		
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
		gl.glPixelStorei (gl.GL_UNPACK_ALIGNMENT, 1)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		
		if CLAMPTOBORDER == True:
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_BORDER)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_BORDER)
		
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, textureData)
		
	

def returnTranslationMatrix(dx,dy,dz=0):
	matrix = np.identity(4)
	
	transVector = np.array([dx,dy,dz,1])
	matrix[:,3] = transVector
	#print "trans matrix: ", matrix
	return matrix

def returnRotationMatrix(angle):
	angleRad = math.radians(angle)
	matrix = np.identity(4)
	cos = math.cos(angleRad)
	sin = math.sin(angleRad)
	
	matrix[0,0] = cos
	matrix[0,1] = -sin
	matrix[1,0] = sin
	matrix[1,1] = cos
	
	#print "trans matrix: ", matrix
	return matrix
	
class GL_BatchImageRenderer():

	def __init__(self, nrlayers):
		logging.info("*************************************")
		logging.info("* Initialise batch image renderer ")
		logging.info("*************************************")
		
		self.maxImagesPerBuffer = 140
		self.layersContent =[]
		self.layerBufferIDs = []
		self.layersVertexData = [nrlayers]
		self.initShaders()
		self.program = buildProgram(self.vertex_code,self.fragment_code)
		
		for i in range (0, nrlayers):
			self.layersContent.append({})
			self.layerBufferIDs.append({})
			logging.info("layersContent table: %s", self.layersContent)
		
		self.data = np.zeros(6, [("position", np.float32, 4), 
								 ("color",    np.float32, 4),
								 ("texCoord", np.float32, 2),
								 ("imageIndex", np.int32,   1) ])
		
		VAO_ID = gl.glGenVertexArrays(1)
		gl.glBindVertexArray(VAO_ID)
		
		self.buffer = self.buildBuffer(self.data)
		self.bindAttributes(self.buffer)
		self.bindUniforms()
		
		
	def initShaders(self):
		self.vertex_code = """
		#version 330
		in int imageIndex;
		in vec4 position;
		in vec4 color;
		in vec2 texCoord;
		
		out vec4 v_color;
		out vec2 v_texCoord;
		
		uniform mat4 modelMatrix[""" + str(self.maxImagesPerBuffer) + """];
		uniform mat3 textMatrix[""" + str(self.maxImagesPerBuffer) + """];
		uniform mat4 projectionMatrix;
		
		void main() {
			gl_Position = projectionMatrix*modelMatrix[imageIndex]*position;
			
			//gl_Position = modelMatrix[imageIndex]*position;
			v_color = color;
			vec3 t_coord = vec3(texCoord, 1.0);
			v_texCoord = vec2(textMatrix[imageIndex]*t_coord);
		} """
		logging.info("Vertex shader code:%s", self.vertex_code)
		self.fragment_code = """
		#version 330
		in vec4 v_color;
		in vec2 v_texCoord;
		out vec4 fragColor;
		
		uniform sampler2D tex;

		void main() {
			fragColor = texture(tex, v_texCoord);
		} """
	
	def buildBuffer(self,data):
		newbuffer = gl.glGenBuffers(1)												# Request a buffer slot from GPU
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, newbuffer)								# Select the buffer
		gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_STATIC_DRAW) 	# Upload data
		return newbuffer

	def bindAttributes(self, buffer):
		DEBUG = True
		# Bind attributes
		# --------------------------------------
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
		
		stride = self.data.strides[0]
		offset = ctypes.c_void_p(0)
		loc = gl.glGetAttribLocation(self.program, "position")
		if DEBUG == True:
			print ("offset: ",offset)
			print ("Attribute position location: ", loc)
		gl.glEnableVertexAttribArray(loc)
		gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, gl.GL_FALSE, stride, offset)

		#offset = ctypes.c_void_p(self.data.dtype["position"].itemsize)
		#loc = gl.glGetAttribLocation(self.program, "color")
		#if DEBUG == True:
		#	print "offset: ",offset
		#	print "Attribute color location: ", loc
		#gl.glEnableVertexAttribArray(loc)
		#gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, gl.GL_FALSE, stride, offset)

		offset = ctypes.c_void_p(self.data.dtype["position"].itemsize+self.data.dtype["color"].itemsize)
		loc = gl.glGetAttribLocation(self.program, "texCoord")
		if DEBUG == True:
			print ("offset: ",offset)
			print ("Attribute texCoord location: ", loc)
		gl.glEnableVertexAttribArray(loc)
		#gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
		gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, offset)
		
		offset = ctypes.c_void_p(self.data.dtype["position"].itemsize+self.data.dtype["color"].itemsize+self.data.dtype["texCoord"].itemsize)
		loc = gl.glGetAttribLocation(self.program, "imageIndex")
		if DEBUG == True:
			print ("offset: ",offset)
			print ("Attribute imageIndex location: ", loc)
		if loc != -1:
			gl.glEnableVertexAttribArray(loc)
			#gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
			gl.glVertexAttribIPointer(loc, 1, gl.GL_INT, stride, offset)
		
		
	def bindUniforms(self):
		# Bind uniforms
		# --------------------------------------
		self.modelMatrixLoc = gl.glGetUniformLocation(self.program, "modelMatrix")
		logging.info("modelMatrixLoc[0]: %s", self.modelMatrixLoc)
		modelMatrixLoc2 = gl.glGetUniformLocation(self.program, "modelMatrix[1]")
		logging.info("modelMatrixLoc[1]: %s", modelMatrixLoc2)
		
		self.modelMatrixLocationsTable = []
		for i in range (0, self.maxImagesPerBuffer):
			if sys.platform.startswith('darwin') :  
				self.modelMatrixLocationsTable.append(self.modelMatrixLoc+i*4)  # on OS X for some reason ?!?
			else:
				self.modelMatrixLocationsTable.append(self.modelMatrixLoc+i)	# on PC
		
		logging.info("model Matrix location table:%s",self.modelMatrixLocationsTable)
		
		self.textMatrixLoc = gl.glGetUniformLocation(self.program, "textMatrix")
		
		self.textMatrixLocationsTable = []
		for i in range (0, self.maxImagesPerBuffer):
			if sys.platform.startswith('darwin') :  
				self.textMatrixLocationsTable.append(self.textMatrixLoc+i*3)  # on OS X for some reason ?!?
			else:
				self.textMatrixLocationsTable.append(self.textMatrixLoc+i)	# on PC
		
		self.projMatrixLoc = gl.glGetUniformLocation(self.program, "projectionMatrix")
		print ("projMatrixLoc location: ", self.projMatrixLoc)
		
		
	def addImageToRenderQueue(self, GL_Image, layer = 0):
		
		logging.info("adding image %s to render queue on layer %s", GL_Image.name ,layer)
		# first test if the texture ID is in that layer
		if not self.layersContent[layer].get(GL_Image.texture): # if it is not yet create it and populate with empty list
			self.layersContent[layer][GL_Image.texture] = []
			self.layerBufferIDs[layer][GL_Image.texture] = [0,0,0]
		
		self.layersContent[layer][GL_Image.texture].append(GL_Image)
		#logging.info("layersContent table: %s", self.layersContent)
		
	def fillBuffers(self):
		logging.info("GL_BatchImageRenderer: fillBuffers")
		# the idea is to create one buffer per layer and texture group
		gl.glUseProgram(self.program)
		for layer in range (0 , len(self.layersContent)): 				# loop layers
			for textID in self.layersContent[layer] : 					# loop textures dict in the layer
				numberImages = len(self.layersContent[layer][textID])
				print( "Fill buffers, layer", layer, "text ID: ", textID, "Number images:", numberImages)
				if numberImages > 0:	# no point creating a buffer if there are no images in this 
					currentImgTable = self.layersContent[layer][textID]
					bufferdata = self.layersContent[layer][textID][0].data # start filling the buffer with the data from the first image
					print ("Current Image table: ", currentImgTable) 
					imageID = currentImgTable[0].id
					print ("imageID:",imageID)
					modelMatrix = currentImgTable[0].modelMatrix
					print ("model matrix:\n", modelMatrix)
					gl.glUniformMatrix4fv(self.modelMatrixLocationsTable[imageID], 1, gl.GL_TRUE, modelMatrix )
					textMatrix = currentImgTable[0].textMatrix
					gl.glUniformMatrix3fv(self.textMatrixLocationsTable[imageID], 1, gl.GL_TRUE, textMatrix )
					
					if numberImages >1:
						for j in range(1, numberImages): # now loop each GL_Image in the layer and that texture
							#print ("image j:",j)
							bufferdata = np.vstack((bufferdata,self.layersContent[layer][textID][j].data))
							imageID = currentImgTable[j].id
							#print ("imageID:",imageID)
							modelMatrix = currentImgTable[j].modelMatrix
							#print ("model matrix:\n", modelMatrix)
							gl.glUniformMatrix4fv(self.modelMatrixLocationsTable[imageID], 1, gl.GL_TRUE, modelMatrix )
							textMatrix = currentImgTable[j].textMatrix
							gl.glUniformMatrix3fv(self.textMatrixLocationsTable[imageID], 1, gl.GL_TRUE, textMatrix )

					
					logging.info("GL_BatchImageRenderer: Creating buffer for layer %s, texture ID %s", layer, textID)
					#print "Buffer data: \n", bufferdata
					VAO_ID = gl.glGenVertexArrays(1)
					gl.glBindVertexArray(VAO_ID)
					
					bufferID = self.buildBuffer(bufferdata)
					
					self.bindAttributes(bufferID)
					self.layerBufferIDs[layer][textID][0] = bufferID
					self.layerBufferIDs[layer][textID][1] = VAO_ID
					self.layerBufferIDs[layer][textID][2] = bufferdata
					gl.glBindVertexArray( 0 )
					logging.debug("GL_BatchImageRenderer: Buffer ID: %s",bufferID)
		
		logging.debug("GL_BatchImageRenderer: layerBufferIDs table content: ")
		logging.debug( self.layerBufferIDs)
		

	def render(self):

		gl.glUseProgram(self.program)
		gl.glUniformMatrix4fv(self.projMatrixLoc, 1, gl.GL_TRUE, PROJ_MATRIX)
		
		layersContent = self.layersContent
		
		for layer in range (0 , len(layersContent)): # loop layers

			for textID in layersContent[layer] : # loop textures dict in the layer
				gl.glBindTexture(gl.GL_TEXTURE_2D, textID)
				
				currentImgTable = layersContent[layer][textID]
				nrImages = len(currentImgTable)

				if nrImages > 0 :
					VAO_ID = self.layerBufferIDs[layer][textID][1]
					gl.glBindVertexArray(VAO_ID)

					for j in range(0, nrImages): # now loop the images in the layer and text dictionary
						if currentImgTable[j].needRefresh == True:
							imageID = currentImgTable[j].id
							modelMatrix = currentImgTable[j].modelMatrix
							gl.glUniformMatrix4fv(self.modelMatrixLocationsTable[imageID], 1, gl.GL_TRUE, modelMatrix )
							textMatrix = currentImgTable[j].textMatrix
							gl.glUniformMatrix3fv(self.textMatrixLocationsTable[imageID], 1, gl.GL_TRUE, textMatrix )
					#logging.info("BatchRenderer::render(), layer %s, images %s", layer,nrImages)
					gl.glDrawArrays(gl.GL_TRIANGLES, 0, nrImages*6)
					gl.glBindVertexArray(0)
		
	
class GL_Image:
	id_generator = itertools.count(0)
	
	def __init__(self, GLtexture,cliprect = None,cliprect_origin = None):
		self.id = next(self.id_generator)
		logging.info("*************************************")
		logging.info("* Initialise image %s, ID: %s", GLtexture.name, self.id)
		logging.info("*************************************")
		self.GLtexture = GLtexture
		self.name = GLtexture.name
		self.texture = GLtexture.texture
		self.width = GLtexture.width
		self.height = GLtexture.height
		self.modelMatrix = np.identity(4)
		
		self.textMatrix = np.identity(3)
		
		self.visible = True
		self.needRefresh = True
		
		self.textClipRect_px = cliprect
		self.text_width = 1.0
		self.text_height = 1.0
		self.text_originx = 0.0
		self.text_originy = 0.0
	
		if cliprect_origin !=None:
			self.text_originx = float(cliprect_origin[0])/float(self.width)
			self.text_originy = float(cliprect_origin[1])/float(self.height)
			
		if cliprect !=None:
			self.text_width 	= float(self.text_originx + cliprect[0])/float(self.width)
			self.text_height	= float(self.text_originy + cliprect[1])/float(self.height)
		
		logging.debug("Loaded texture GL ID: %s , width: %s, height: %s", self.texture,self.width,self.height)
		
		self.data = np.zeros(6, [("position", np.float32, 4), 
								 ("color",    np.float32, 4),
								 ("texCoord", np.float32, 2),
								 ("imageIndex",       np.int32,   1) ])
								 
		self.data['color']    = [ (1,0,0,1), 
								  (0,1,0,1), 
								  (0,0,1,1), 
								  (1,1,0,1), 
								  (0,0,1,1), 
								  (1,1,0,1) ]
		#self.data['position'] = [ (0,0),   (0,gl_height),   (gl_width,0),   (gl_width,gl_height)   ]
		self.data['position'] = [ (-self.width/2 , -self.height/2 , 0.0 , 1.0),
								  (-self.width/2 ,  self.height/2 , 0.0 , 1.0),
								  ( self.width/2 , -self.height/2 , 0.0 , 1.0),
								  ( self.width/2 , -self.height/2 , 0.0 , 1.0),
								  ( self.width/2 ,  self.height/2 , 0.0 , 1.0),
								  (-self.width/2 ,  self.height/2 , 0.0 , 1.0),  ]
		self.data['texCoord'] = [ (self.text_originx					,	self.text_originy					),
								  (self.text_originx					,	self.text_originy+self.text_height	),   
								  (self.text_originx+self.text_width	,	self.text_originy					),
								  (self.text_originx+self.text_width	,	self.text_originy					),
								  (self.text_originx+self.text_width	,	self.text_originy+self.text_height	),
								  (self.text_originx					,	self.text_originy+self.text_height	)   ]
		self.data['imageIndex'] = [ (self.id),
							(self.id),   
							(self.id),
							(self.id),
							(self.id),
							(self.id)   ]

	def resize(self,width,height):
		self.width = width
		self.height = height
		self.data['position'] = [ (-self.width/2 , -self.height/2 , 0.0 , 1.0),
								  (-self.width/2 ,  self.height/2 , 0.0 , 1.0),
								  ( self.width/2 , -self.height/2 , 0.0 , 1.0),
								  ( self.width/2 , -self.height/2 , 0.0 , 1.0),
								  ( self.width/2 ,  self.height/2 , 0.0 , 1.0),
								  (-self.width/2 ,  self.height/2 , 0.0 , 1.0),  ]
	
	def translateTexture(self, textureTranslation):
		
		self.textMatrix[0,2] = textureTranslation[0]
		self.textMatrix[1,2] = textureTranslation[1]
		
		print ("OpenGL lib Image translate texture", self.textMatrix)
	
	def draw(self, position=None, width=None, height=None, color=None, rotation=None, rotationCenter=None, textureTranslation = None, textureRotation = 0.0, textureZoom = None, textureRotationCenter = None):
		
		transMatrix = np.identity(4)
		textMatrix = np.identity(3)
		
		if self.visible == True:
			if rotation !=	 None:
				if rotationCenter !=None:	# translate the model to the rotation center
					transMatrix[0,3] = -float(rotationCenter[0])
					transMatrix[1,3] = -float(rotationCenter[1])
					
					#print "modelMatrix after rot center translation: \n", transMatrix
				rotationMatrix = np.identity(4)
				cos = math.cos(-rotation)
				sin = math.sin(-rotation)
				
				rotationMatrix[0,0] = cos
				rotationMatrix[0,1] = -sin
				rotationMatrix[1,0] = sin
				rotationMatrix[1,1] = cos
				transMatrix = np.dot(rotationMatrix, transMatrix) # rotate the model 
				#print "modelMatrix after rotation: \n", transMatrix
				if rotationCenter !=None:
					rotCenterTransMat = returnTranslationMatrix(float(rotationCenter[0]),float(rotationCenter[1]))
					transMatrix = np.dot(rotCenterTransMat, transMatrix)  # replace the model to the center
					#print "modelMatrix after rot center translation: \n", transMatrix
			
			if position != None:
				if rotationCenter == None:	# then I have not messed with the translation matrix already and can update it direct
					transMatrix[0,3] = position[0]
					transMatrix[1,3] = position[1]
				else:	# otherwise need to do a dot product
					trMatrix = np.identity(4)
					trMatrix[0,3] = position[0]
					trMatrix[1,3] = position[1]
					transMatrix = np.dot(trMatrix, transMatrix)
				
				#print "modelMatrix after translation: \n", transMatrix
			
			if textureRotation != 0.0:
				if textureRotationCenter !=None:	# translate the model to the rotation center
					textMatrix[0,2] = - float(textureRotationCenter[0])/self.GLtexture.width
					textMatrix[1,2] = - float(textureRotationCenter[1])/self.GLtexture.height
				else:
					textMatrix[0,2] = -self.text_originx - self.text_width/2
					textMatrix[1,2] = -self.text_originy - self.text_height/2
				
				rotationMatrix = np.identity(3)
				cos = math.cos(-textureRotation)
				sin = math.sin(-textureRotation)
				#aspectRatio = float(self.GLtexture.width)/self.GLtexture.height
				#print ("aspect ratio:",aspectRatio)
				
				rotationMatrix[0,0] = cos #aspectRatio
				rotationMatrix[0,1] = -sin #*aspectRatio
				rotationMatrix[1,0] = sin # * aspectRatio
				rotationMatrix[1,1] = cos  #/ aspectRatio
				
				textMatrix = np.dot(rotationMatrix, textMatrix) # rotate the texture 
				
				
				translateBackMat = np.identity(3)
				if textureRotationCenter !=None:	# translate the model to the rotation center
					translateBackMat[0,2] =  float(textureRotationCenter[0])/self.GLtexture.width
					translateBackMat[1,2] =  float(textureRotationCenter[1])/self.GLtexture.height
				else:
					translateBackMat[0,2] = self.text_originx+self.text_width/2
					translateBackMat[1,2] = self.text_originy+self.text_height/2
					
				textMatrix = np.dot(translateBackMat, textMatrix)
				
				#print ("textMatrix after rotation\n", textMatrix)
				
				
			if textureZoom != None:
				textMatrix = textMatrix*textureZoom
				#print "textMatrix after zoom", textureZoom, textMatrix
			
			if textureTranslation != None:
				#textMatrix[0,2] = (float(textureTranslation[0])/self.textClipRect_px[0])*self.text_width
				#textMatrix[1,2] = float(textureTranslation[1])/self.textClipRect_px[1]*self.text_height
				translateTextMat = np.identity(3)
				translateTextMat[0,2] = float(textureTranslation[0])/self.GLtexture.width
				translateTextMat[1,2] = float(textureTranslation[1])/self.GLtexture.height
				
				#print("texture width,height:",self.GLtexture.width,self.GLtexture.height)
				
				textMatrix = np.dot(translateTextMat, textMatrix)
				#print "image id ", self.id,self.name, "translating texture: \n", self.textMatrix
				#print "textMatrix after text translation", textMatrix
		else:
			transMatrix[0,3] = screenWidth * 3
			transMatrix[1,3] = screenHeight *3
		self.modelMatrix = transMatrix
		self.textMatrix = textMatrix
		

class GL_rectangle:
	vertex_code = """
    #version 330
    in vec4 position;
    in vec4 color;
    
    uniform mat4 transMat;
    uniform mat4 projMatrix;

    out vec4 v_color;
    
    void main()
    {
        gl_Position = projMatrix*transMat*position;
        v_color = color;
    } """

	fragment_code = """
    #version 330
    in vec4 v_color;
    out vec4 outColor;
    
    void main()
    {
        outColor = v_color;
    } """
	
	def __init__(self, width, height, linewidth = 1, color = COLOR_GREEN):
		self.width = width
		self.height = height
		self.color = color
		
		self.program = buildProgram(self.vertex_code,self.fragment_code)
		logging.info("Init GL_Rectangle, width: %s, height: %s", self.width,self.height)
		
		self.data = np.zeros(4, [("position", np.float32, 4), 
								 ("color",    np.float32, 4) ])
		
		self.data['color']    = [ (color[0],color[1],color[2],1),
								  (color[0],color[1],color[2],1),
								  (color[0],color[1],color[2],1),
								  (color[0],color[1],color[2],1) ]

		self.data['position'] = [ (-self.width/2 , -self.height/2 , 0.0 , 1.0),
								  (-self.width/2 ,  self.height/2 , 0.0 , 1.0),
								  ( self.width/2 ,  self.height/2 , 0.0 , 1.0),
								  ( self.width/2 , -self.height/2 , 0.0 , 1.0)  ]
		
		self.VAO_ID = gl.glGenVertexArrays(1)
		gl.glBindVertexArray(self.VAO_ID)
		
		self.buffer = gl.glGenBuffers(1)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)	# Make this buffer the default one
		gl.glBufferData(gl.GL_ARRAY_BUFFER, self.data.nbytes, self.data, gl.GL_STATIC_DRAW)

		# Bind attributes
		# --------------------------------------
		stride = self.data.strides[0]
		offset = ctypes.c_void_p(0)
		loc = gl.glGetAttribLocation(self.program, "position")
		gl.glEnableVertexAttribArray(loc)
		gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)

		offset = ctypes.c_void_p(self.data.dtype["position"].itemsize)
		loc = gl.glGetAttribLocation(self.program, "color")
		gl.glEnableVertexAttribArray(loc)
		gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)
		
		# Bind uniforms
		# --------------------------------------
		loc = gl.glGetUniformLocation(self.program, "scale")
		gl.glUniform1f(loc, 1.0)
		self.transMatLoc = gl.glGetUniformLocation(self.program, "transMat")
		self.projMatrixLoc = gl.glGetUniformLocation(self.program, "projMatrix")
		
	def draw(self, x, y, angle = 0):
		gl.glUseProgram(self.program)
		gl.glBindVertexArray(self.VAO_ID)
		
		modMatrix = IDENTITY_MATRIX
		transMatrix = returnTranslationMatrix(float(x+self.width/2),float(y+self.height/2))
		modMatrix = np.dot(transMatrix, modMatrix)
		
		gl.glUniformMatrix4fv(self.transMatLoc, 1, gl.GL_TRUE, modMatrix)
		gl.glUniformMatrix4fv(self.projMatrixLoc, 1, gl.GL_TRUE, PROJ_MATRIX)
		
		gl.glDrawArrays(gl.GL_LINE_LOOP, 0, 4)

class GL_Filled_Rectangle:
	vertex_code = """
    #version 330
    in vec4 position;
    in vec4 color;
    
    uniform mat4 transMat;
    uniform mat4 projMatrix;

    out vec4 v_color;
    
    void main()
    {
        gl_Position = projMatrix*transMat*position;
        v_color = color;
    } """

	fragment_code = """
    #version 330
    in vec4 v_color;
    out vec4 outColor;
    
    void main()
    {
        outColor = v_color;
    } """
	
	def __init__(self, width, height, linewidth = 1, color = COLOR_GREEN):
		self.width = width
		self.height = height
		self.color = color
		
		self.program = buildProgram(self.vertex_code,self.fragment_code)
		logging.info("Init GL_Rectangle, width: %s, height: %s", self.width,self.height)
		
		self.data = np.zeros(6, [("position", np.float32, 4), 
								 ("color",    np.float32, 4) ])
		
		self.data['color']    = [ (color[0],color[1],color[2],color[3]),
								  (color[0],color[1],color[2],color[3]),
								  (color[0],color[1],color[2],color[3]),
								  (color[0],color[1],color[2],color[3]),
								  (color[0],color[1],color[2],color[3]),
								  (color[0],color[1],color[2],color[3]) ]

		self.data['position'] = [ (-self.width/2 , -self.height/2 , 0.0 , 1.0),
								  (-self.width/2 ,  self.height/2 , 0.0 , 1.0),
								  ( self.width/2 , -self.height/2 , 0.0 , 1.0),
								  ( self.width/2 , -self.height/2 , 0.0 , 1.0),
								  ( self.width/2 ,  self.height/2 , 0.0 , 1.0),
								  (-self.width/2 ,  self.height/2 , 0.0 , 1.0),  ]
		
		self.VAO_ID = gl.glGenVertexArrays(1)
		gl.glBindVertexArray(self.VAO_ID)
		
		self.buffer = gl.glGenBuffers(1)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)	# Make this buffer the default one
		gl.glBufferData(gl.GL_ARRAY_BUFFER, self.data.nbytes, self.data, gl.GL_STATIC_DRAW)

		# Bind attributes
		# --------------------------------------
		stride = self.data.strides[0]
		offset = ctypes.c_void_p(0)
		loc = gl.glGetAttribLocation(self.program, "position")
		gl.glEnableVertexAttribArray(loc)
		gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)

		offset = ctypes.c_void_p(self.data.dtype["position"].itemsize)
		loc = gl.glGetAttribLocation(self.program, "color")
		gl.glEnableVertexAttribArray(loc)
		gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)
		
		# Bind uniforms
		# --------------------------------------
		loc = gl.glGetUniformLocation(self.program, "scale")
		gl.glUniform1f(loc, 1.0)
		self.transMatLoc = gl.glGetUniformLocation(self.program, "transMat")
		self.projMatrixLoc = gl.glGetUniformLocation(self.program, "projMatrix")
		
	def draw(self, x, y, angle = 0):
		gl.glUseProgram(self.program)
		gl.glBindVertexArray(self.VAO_ID)
		
		modMatrix = IDENTITY_MATRIX
		transMatrix = returnTranslationMatrix(float(x+self.width/2),float(y+self.height/2))
		modMatrix = np.dot(transMatrix, modMatrix)
		
		gl.glUniformMatrix4fv(self.transMatLoc, 1, gl.GL_TRUE, modMatrix)
		gl.glUniformMatrix4fv(self.projMatrixLoc, 1, gl.GL_TRUE, PROJ_MATRIX)
		
		gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
		

class GL_Font:
	vertex_code = """
    #version 330
    in vec4 position;
    in vec2 texCoord;
    
    uniform mat4 projMatrix;

    out vec2 v_texCoord;
    
    void main()
    {
        gl_Position = projMatrix*position;
        v_texCoord = texCoord;
    } """

	fragment_code = """
    #version 330
    in vec2 v_texCoord;
    out vec4 outColor;
    uniform sampler2D tex;

    void main()
    {
        outColor = texture(tex, v_texCoord);
    } """

	def __init__(self,fontName,fontSize, fontColor = (255,255,255), antialias = True, fontKerning = 0):
		logging.debug('GL_Font_3 - initialising font %s ',fontName)
		self.antialias = antialias
		self.fontColor = fontColor
		self.fontKerning = fontKerning
		pygame.font.init()
		if not pygame.font.get_init():
			logging.error ('Could not render font.')
			return -1
		fontPath = os.path.join(os.path.dirname(__file__), '../../',fontName)
		self.font = pygame.font.Font(fontPath,fontSize)
		self.char = []
		self.textWidth = 0
		self.textHeight = 0
		self.charWidth = 0
		self.displayString = ""
		self.x = 0
		self.y = 0
		
		# render each character
		for ch in range(32,177):
			letter_render = self.font.render(chr(ch), self.antialias, self.fontColor)
			letter = pygame.image.tostring(letter_render, 'RGBA', 1)
			letter_w, letter_h = letter_render.get_size()
			
			if letter_h > self.textHeight:
				self.textHeight = letter_h
			if letter_w > self.charWidth:
				self.charWidth = letter_w
				
			self.char.append((letter_w,letter_h,letter))
		
		self.textWidth = self.charWidth*len(self.char)
		
		logging.debug("Loaded all characters, texture height = %s, texture width = %s", self.textHeight, self.textWidth)
		# create a texture to hold all characters - we will fill it later
		self.texture = gl.glGenTextures(1)
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.textWidth, self.textHeight, 0, gl.GL_RGBA,
			gl.GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
		
		x = 0
		for ch in range(0,len(self.char)):
			gl.glTexSubImage2D(gl.GL_TEXTURE_2D, 0, x, 0, self.char[ch][0], self.char[ch][1], gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.char[ch][2])
			x += self.charWidth
		
		self.program = buildProgram(self.vertex_code,self.fragment_code)
		self.VAO_ID = gl.glGenVertexArrays(1)
		gl.glBindVertexArray(self.VAO_ID)
		# Request a buffer slot from GPU
		self.buffer = gl.glGenBuffers(1)
		
		self.data = np.zeros(6, [("position", np.float32, 4),
								 ("texCoord", np.float32, 2) ])
								 
		self.data['position'] = [ (-self.textWidth/2 +600, -self.textHeight/2 +200, 0.0 , 1.0),
								  (-self.textWidth/2 +600,  self.textHeight/2 +200, 0.0 , 1.0),
								  ( self.textWidth/2 +600, -self.textHeight/2 +200, 0.0 , 1.0),
								  ( self.textWidth/2 +600, -self.textHeight/2 +200, 0.0 , 1.0),
								  ( self.textWidth/2 +600,  self.textHeight/2 +200, 0.0 , 1.0),
								  (-self.textWidth/2 +600,  self.textHeight/2 +200, 0.0 , 1.0),  ]
		self.data['texCoord'] = [ (0,0),
								  (0,1),   
								  (1,0),
								  (1,0),
								  (1,1),
								  (0,1)   ]
								  
		self.bindAttributes(self.buffer)
		self.bindUniforms()
		gl.glUniformMatrix4fv(self.projMatrixLoc, 1, gl.GL_TRUE, PROJ_MATRIX)
		
		gl.glBindVertexArray(0)
		
		logging.info('GL_Font - initialision of font %s complete',fontName)

	def bindUniforms(self):
		# Bind uniforms
		# --------------------------------------
		
		self.projMatrixLoc = gl.glGetUniformLocation(self.program, "projMatrix")
		print ("projMatrixLoc location: ", self.projMatrixLoc)
		
	def bindAttributes(self, buffer):
		DEBUG = False
		# Bind attributes
		# --------------------------------------
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
		
		stride = self.data.strides[0]
		offset = ctypes.c_void_p(0)
		loc = gl.glGetAttribLocation(self.program, "position")
		if DEBUG == True:
			print ("offset: ",offset)
			print ("Attribute position location: ", loc)
		gl.glEnableVertexAttribArray(loc)
		gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, gl.GL_FALSE, stride, offset)

		offset = ctypes.c_void_p(self.data.dtype["position"].itemsize)
		loc = gl.glGetAttribLocation(self.program, "texCoord")
		if DEBUG == True:
			print ("offset: ",offset)
			print ("Attribute texCoord location: ", loc)
		gl.glEnableVertexAttribArray(loc)
		#gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
		gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, gl.GL_FALSE, stride, offset)
		
		
	def draw(self,s,x,y):
		#print "drawing string ", s
		gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
		gl.glUseProgram(self.program)
		gl.glBindVertexArray(self.VAO_ID)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
		
		#s = str(s)
		s = str(s).encode('ascii', 'ignore').decode('ascii')
		length = len(s)
		if self.displayString != s or x != self.x or y != self.y:		# only refresh the buffer if the string has changed or position moved
			#print "string needs redrawn", s
			i = 0
			
			self.data = np.zeros(6, [("position", np.float32, 4),
									 ("texCoord", np.float32, 2) ])
			
			chardata = np.zeros(6, [("position", np.float32, 4),
									 ("texCoord", np.float32, 2) ])
			
			charTextWidth = float(self.charWidth)/self.textWidth
			charY = y
			
			for i in range(0,length):
				char = s[i]
				charcode = ord(char)-32
				charX = x + (self.charWidth + self.fontKerning)*i
				
				chardata['position'] = [ (charX						, charY						, 0.0 , 1.0),		# bottom left
										( charX						, charY + self.textHeight	, 0.0 , 1.0),		# top left
										( charX + self.charWidth	, charY						, 0.0 , 1.0),		# bottom right
										( charX + self.charWidth	, charY						, 0.0 , 1.0),		# bottom right
										( charX + self.charWidth	, charY + self.textHeight	, 0.0 , 1.0),		# top right
										( charX						, charY + self.textHeight	, 0.0 , 1.0),  ]	# top left
				charTextX = charcode*charTextWidth
				
				chardata['texCoord'] = [ (charTextX					,0.0	),		# bottom left
										 (charTextX					,1.0	),		# top left
										 (charTextX+charTextWidth	,0.0	),		# bottom right
										 (charTextX+charTextWidth	,0.0	),		# bottom right
										 (charTextX+charTextWidth	,1.0	),		# top right
										 (charTextX					,1.0	) ]		# top left
				
				self.data = np.vstack((self.data ,chardata))	# add the character to the buffer stack
			
			gl.glBufferData(gl.GL_ARRAY_BUFFER, self.data.nbytes, self.data, gl.GL_DYNAMIC_DRAW)
			self.displayString = s
			self.x = x
			self.y = y
		gl.glUniformMatrix4fv(self.projMatrixLoc, 1, gl.GL_TRUE, PROJ_MATRIX)
		gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6*(length+1))
		gl.glBindVertexArray(0)
		
class GL_Image_OLD:
	vertex_code = """
    uniform float scale;
    attribute vec4 position;
    attribute vec4 color;
    attribute vec2 texCoord;
    
    uniform mat4 transMat;
    uniform mat4 projMatrix;

    varying vec4 v_color;
    varying vec2 v_texCoord;
    
    void main()
    {
        gl_Position = projMatrix*transMat*position;
        v_color = color;
        v_texCoord = texCoord;
    } """

	fragment_code = """
    varying vec4 v_color;
    varying vec2 v_texCoord;
    
    uniform sampler2D tex;

    void main()
    {
        gl_FragColor = texture(tex, v_texCoord);
    } """
	
	def __init__(self, GLtexture,cliprect = None,origin = None):
		logging.info("*************************************")
		logging.info("* Initialise image %s", GLtexture.name)
		logging.info("*************************************")
		self.name = GLtexture.name
		self.texture = GLtexture.texture
		self.width = GLtexture.width
		self.height = GLtexture.height
		
		self.program = buildProgram(self.vertex_code,self.fragment_code)
		logging.info("Loaded texture GL ID: %s , width: %s, height: %s", self.texture,self.width,self.height)
		
		self.data = np.zeros(6, [("position", np.float32, 4), 
								 ("color",    np.float32, 4),
								 ("texCoord", np.float32, 2) ])
								 
		self.data['color']    = [ (1,0,0,1), 
								  (0,1,0,1), 
								  (0,0,1,1), 
								  (1,1,0,1), 
								  (0,0,1,1), 
								  (1,1,0,1) ]
		#self.data['position'] = [ (0,0),   (0,gl_height),   (gl_width,0),   (gl_width,gl_height)   ]
		self.data['position'] = [ (-self.width/2 , -self.height/2 , 0.0 , 1.0),
								  (-self.width/2 ,  self.height/2 , 0.0 , 1.0),
								  ( self.width/2 , -self.height/2 , 0.0 , 1.0),
								  ( self.width/2 , -self.height/2 , 0.0 , 1.0),
								  ( self.width/2 ,  self.height/2 , 0.0 , 1.0),
								  (-self.width/2 ,  self.height/2 , 0.0 , 1.0),  ]
		self.data['texCoord'] = [ (0,0),
								  (0,1),   
								  (1,0),
								  (1,0),
								  (1,1),
								  (0,1)   ]
		
		print ("self.data['position',0]", self.data['position'][0])
		print ("self.data['position',1]", self.data['position'][1])
		print ("self.data['position',2]", self.data['position'][2])
		print ("self.data['position',3]", self.data['position'][3])
		# Build buffer
		# --------------------------------------

		# Request a buffer slot from GPU
		self.buffer = gl.glGenBuffers(1)

		# Make this buffer the default one
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)

		# Upload data
		gl.glBufferData(gl.GL_ARRAY_BUFFER, self.data.nbytes, self.data, gl.GL_STATIC_DRAW)


		# Bind attributes
		# --------------------------------------
		stride = self.data.strides[0]
		offset = ctypes.c_void_p(0)
		print ("offset: ",offset)
		loc = gl.glGetAttribLocation(self.program, "position")
		gl.glEnableVertexAttribArray(loc)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
		gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)

		offset = ctypes.c_void_p(self.data.dtype["position"].itemsize)
		print ("offset: ",offset)
		loc = gl.glGetAttribLocation(self.program, "color")
		gl.glEnableVertexAttribArray(loc)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
		gl.glVertexAttribPointer(loc, 4, gl.GL_FLOAT, False, stride, offset)

		offset = ctypes.c_void_p(self.data.dtype["position"].itemsize+self.data.dtype["color"].itemsize)
		print ("offset: ",offset)
		loc = gl.glGetAttribLocation(self.program, "texCoord")
		gl.glEnableVertexAttribArray(loc)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
		gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)

		# Bind uniforms
		# --------------------------------------
		loc = gl.glGetUniformLocation(self.program, "scale")
		gl.glUniform1f(loc, 1.0)
		self.transMatLoc = gl.glGetUniformLocation(self.program, "transMat")
		self.projMatrixLoc = gl.glGetUniformLocation(self.program, "projMatrix")
		self.abspos=None
		self.relpos=None
		self.color=(1,1,1,1)
		self.rotation=0
		self.rotationCenter=None
		self.rotateTexture = False
		self.translateTexture = False
		self.scissorBoxOrigin = None
		self.scissorBoxSize = None

	def resize(self,width,height):
		self.texture.resize(width,height)
		self.width = self.texture.width
		self.height = self.texture.height
	
	def addScissorBox(self,box_origin, box_size):
		self.scissorBoxOrigin = box_origin
		self.scissorBoxSize = box_size
	
	def setRotateTexture(self,rotateTexture):
		self.rotateTexture = rotateTexture
	
	def setTranslateTexture(self,translateTexture):
		self.translateTexture = translateTexture
	
		
	def draw(self, position=None, width=None, height=None, color=None, rotation=None, rotationCenter=None):
		#print "data buffer:", self.data
		
		modMatrix = np.identity(4)
		if rotation != None:
			if rotationCenter !=None:	# translate the model to the rotation center
				rotCenterTransMat = returnTranslationMatrix(-float(rotationCenter[0]),-float(rotationCenter[1]))
				modMatrix = np.dot(rotCenterTransMat, modMatrix)
				#print "modMatrix after rot center translation: \n", modMatrix
			
			modMatrix = np.dot(returnRotationMatrix(-rotation), modMatrix) # rotate the model 
			
			if rotationCenter !=None:
				rotCenterTransMat = returnTranslationMatrix(float(rotationCenter[0]),float(rotationCenter[1]))
				modMatrix = np.dot(rotCenterTransMat, modMatrix)  # replace the model to the center
				#print "modMatrix after rot center translation: \n", modMatrix
		
		if position != None:
			transMatrix = returnTranslationMatrix(float(position[0]),float(position[1]))
			modMatrix = np.dot(transMatrix, modMatrix)
			#print "modMatrix after translation: \n", modMatrix
		
		#modMatrix = np.dot(projMatrix, modMatrix)
		
		#print "mod matrix after applying projection: \n", modMatrix
		#print "vert pos 1", np.dot(modMatrix, self.data['position'][0])
		#print "vert pos 2", np.dot(modMatrix, self.data['position'][1])
		#print "vert pos 3", np.dot(modMatrix, self.data['position'][2])
		#print "vert pos 4", np.dot(modMatrix, self.data['position'][3])
		
		
		gl.glUniformMatrix4fv(self.transMatLoc, 1, gl.GL_TRUE, modMatrix)
		gl.glUniformMatrix4fv(self.projMatrixLoc, 1, gl.GL_TRUE, PROJ_MATRIX)
		
		
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer)
		gl.glUseProgram(self.program)
		gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)
		
