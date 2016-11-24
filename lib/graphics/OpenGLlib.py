import pygame
import os
import math
import logging

from OpenGL.GL import *
from OpenGL.GLU import *

import decimal
D = decimal.Decimal

COLOR_WHITE 	= (1.0,1.0,1.0)
COLOR_PINK 		= (1.0,0,1.0)
COLOR_GREY 		= (0.5,0.5,0.5)
COLOR_TURQUOISE = (0,1.0,1.0)
COLOR_RED 		= (1.0,0,0)
COLOR_GREEN 	= (0,213.0/255.0,0)
COLOR_BLUE 		= (0.0,0,1.0)
screenWidth = 0
screenHeight = 0

def initializeDisplay(w, h, fullscreen, backgroundColor =(0,0,0)):
	pygame.display.init()
	
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
	#glEnable(GL_DEPTH_TEST)
	
	glClearColor(backgroundColor[0], backgroundColor[1], backgroundColor[2], 1.0)
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	# this puts us in quadrant 1, rather than quadrant 4
	glViewport(0, 0, w, h)
	gluOrtho2D(0, w, 0, h)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	# set up texturing
	glEnable(GL_TEXTURE_2D)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def returnOpenGLcoord(pygameCoord):
	global screenHeight
	
	return (pygameCoord[0],screenHeight-pygameCoord[1])
	
def loadImage(image):
	try:
		textureSurface = pygame.image.load(image)
	
		textureData = pygame.image.tostring(textureSurface, "RGBA", 1)

		width = textureSurface.get_width()
		height = textureSurface.get_height()

		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
			GL_UNSIGNED_BYTE, textureData)

		return texture, width, height
	except :
		logging.error("Could not load file %s",image)
		return -1
	
def delTexture(texture):
	glDeleteTextures(texture)

def createTexDL(texture, width, height,cliprect=None,origin=None):
	text_width = 1.0
	text_height = 1.0
	texoriginx = 0.0
	texoriginy = 0.0
	
	if origin !=None:
		texoriginx = float(origin[0])/float(width)
		texoriginy = float(origin[1])/float(height)
		
	if cliprect !=None:
		text_width = float(texoriginx + cliprect[0])/float(width)
		text_height =  float(texoriginy + cliprect[1])/float(height)
	
	#logging.debug("OpenGLLib:createTexDL:  texoriginx: %s texoriginy: %s text_width: %s text_height: %s height: %s width: %s", texoriginx, texoriginy, text_width, text_height, height, width)
	
	newList = glGenLists(1)
	glNewList(newList,GL_COMPILE)
	glBindTexture(GL_TEXTURE_2D, texture)
	glBegin(GL_QUADS)
	
	#texoriginx:  0.25 texoriginy:  0.165745856354 text_width:  0.696041666667 text_height:  0.691895851775 height:  905 width:  1200
	# Bottom Left Of The Texture and Quad
	glTexCoord2f(texoriginx, texoriginy); glVertex2f(0, 0)

	# Top Left Of The Texture and Quad
	glTexCoord2f(texoriginx, texoriginy+text_height); glVertex2f(0, (text_height)* height)

	# Top Right Of The Texture and Quad
	glTexCoord2f(texoriginx+text_width, texoriginy+text_height); glVertex2f( (text_width)* width, (text_height)* height)

	# Bottom Right Of The Texture and Quad
	glTexCoord2f(texoriginx+text_width, texoriginy); glVertex2f((text_width)* width, 0)
	glEnd()
	glEndList()

	return newList

def delDL(list):
	glDeleteLists(list, 1)

class GL_Texture:
	def __init__(s, texname=None, texappend=".png",cliprect = None,origin = None):
		s.filename = os.path.join('data', texname)
		s.filename += texappend
		s.cliprect = cliprect
		s.origin = origin

		s.texture, s.width, s.height = loadImage(s.filename)
		
		#logging.debug("OpenGLLib:GL_Texture:init: %s", s.filename)
		s.displaylist = createTexDL(s.texture, s.width, s.height,s.cliprect,s.origin)       
	
	def resize(self, new_width, new_height):
		#print "**************************************************************************"
		#print "Resizing: ", self.filename
		
		x_red_ratio = float(new_width)/float(self.width)
		y_red_ratio = float(new_height)/float(self.height)
		
		#print "x red ratio: ", x_red_ratio, "y red ratio: ", y_red_ratio
		#print "old width:", self.width,"old height:", self.height
		self.width = new_width
		self.height = new_height
		#print "new width:", self.width,"new height:", self.height
		
		if self.origin:
			self.origin[0] = self.origin[0] * x_red_ratio
			self.origin[1] = self.origin[1] * y_red_ratio
			#print "new origin: ", self.origin[0], self.origin[1]
			
		if self.cliprect:
			#print "old cliprect: ",  self.cliprect[0], self.cliprect[1]
			self.cliprect[0] = self.cliprect[0] * x_red_ratio
			self.cliprect[1] = self.cliprect[1] * y_red_ratio
			#print "new cliprect: ",  self.cliprect[0], self.cliprect[1]
		
		
		self.displaylist = createTexDL(self.texture, self.width, self.height, self.cliprect, self.origin)

	def __del__(self):
		if self.texture != None:
			delTexture(self.texture)
			self.texture = None
		if self.displaylist != None:
			delDL(self.displaylist)
			self.displaylist = None

	#def __repr__(s):
	#	return s.texture.__repr__()

class GL_Image:
	def __init__(self, texname,cliprect = None,origin = None):
		self.texture = GL_Texture(texname,".png",cliprect,origin)
		self.width = self.texture.width
		self.height = self.texture.height
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
	
		
	def draw(self, abspos=None, translation=[0,0], width=None, height=None, color=None, rotation=None, rotationCenter=None):
		
		if self.scissorBoxOrigin != None:
			glScissor(abspos[0]+self.scissorBoxOrigin[0], abspos[1]+self.scissorBoxOrigin[1], self.scissorBoxSize[0], self.scissorBoxSize[1])
			glEnable(GL_SCISSOR_TEST)
		
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		if abspos:
			glTranslate(abspos[0],abspos[1],0)
		
		if (self.translateTexture == True) or (self.rotateTexture == True):
			glMatrixMode(GL_TEXTURE)
		
		if (self.translateTexture == True):
			translation = (float (translation[0]) / float(self.width), float(translation[1]) / float(self.height))
			
		glTranslate(translation[0],translation[1],0)
		
		if rotation==None:
			rotation=self.rotation
		
		if rotation != 0: # reverse
			if rotationCenter == None:
				if self.rotateTexture == False:
					rotationCenter = (self.width / 2, self.height / 2)
				else:
					rotationCenter = (0.5,0.5)
			#print "rotation centre before: ", rotationCenter[0], rotationCenter[1]
			#print "width: ", self.width, "height: ", self.height
			if (rotationCenter != None) and (self.rotateTexture == True):
				rotationCenter = (float (rotationCenter[0]) / float(self.width), float(rotationCenter[1]) / float(self.height))
			
			#print "rotation centre: ", rotationCenter
			glTranslate(rotationCenter[0],rotationCenter[1],0)
			glRotate(rotation,0,0,-1)
			glTranslate(-rotationCenter[0],-rotationCenter[1],0)
	
		glCallList(self.texture.displaylist)
		glLoadIdentity()

		if self.scissorBoxOrigin != None:
			glDisable(GL_SCISSOR_TEST)

class GL_line:
	def __init__(self, length, width = 1, color = COLOR_GREEN):
		self.width = width
		self.color = color

		self.DL = glGenLists(1)
		
		glNewList(self.DL,GL_COMPILE)
		glDisable(GL_TEXTURE_2D)
		glColor3f(self.color[0],self.color[1],self.color[2]) # //blue color
		glBegin(GL_QUADS)
		glVertex2f(0, 0)					# Bottom Left Of The Texture and Quad
		glVertex2f(0, self.width)			# Top Left Of The Texture and Quad
		glVertex2f(length, self.width)		# Top Right Of The Texture and Quad
		glVertex2f(length, 0)
		glEnd()

		glColor3f(1.0,1.0,1.0) # 
		glEnable(GL_TEXTURE_2D)
		glEndList()
		
	def draw(self, x, y, angle = 0):
		glLoadIdentity()
		glTranslate(x,y,0)
		glCallList(self.DL)

class GL_rectangle:
	def __init__(self, width, height, linewidth = 1, color = COLOR_GREEN):
		self.width = width
		self.height = height
		self.color = color

		self.DL = glGenLists(1)
		
		glNewList(self.DL,GL_COMPILE)
		glDisable(GL_TEXTURE_2D)
		glColor3f(self.color[0],self.color[1],self.color[2]) # //blue color
		glBegin(GL_LINE_LOOP)
		glVertex2f(0, 0)					# Bottom Left 
		glVertex2f(0, self.height)			# Top Left 
		glVertex2f(self.width, self.height)		# Top Right 
		glVertex2f(self.width, 0)				# Bottom Right
		glEnd()

		glColor3f(1.0,1.0,1.0) # 
		glEnable(GL_TEXTURE_2D)
		glEndList()
		
	def draw(self, x, y, angle = 0):
		glLoadIdentity()
		glTranslate(x,y,0)
		glCallList(self.DL)

class GL_Font:
	def __init__(self,fontName,fontSize, fontColor = (255,255,255), antialias = True, fontKerning = 0):
		logging.info('GL_Font_3 - initialising font %s ',fontName)
		self.antialias = antialias
		self.fontColor = fontColor
		self.fontKerning = fontKerning
		pygame.font.init()
		if not pygame.font.get_init():
			print 'Could not render font.'
			return -1
		self.font = pygame.font.Font(fontName,fontSize)
		self.char = []

		for ch in range(32,177):
			self.char.append(self.CreateCharacter(chr(ch)))

		self.g_base = glGenLists(256);
		for ch in range(32,177):
			c=ch-32
			#print "char[",c,"] : ", self.char[c]

			glNewList(self.g_base+c,GL_COMPILE)					#  Start Building A List
			glBindTexture(GL_TEXTURE_2D, self.char[c][0])
			glBegin(GL_QUADS)								# Use A Quad For Each Character
			glTexCoord2f(0,0)								# Texture Coord (Bottom Left)
			glVertex2f(0,0)									# Vertex Coord (Bottom Left)
			
			glTexCoord2f(0,1.0)								# Texture Coord (Top Left)
			glVertex2f(0,self.char[c][2])					# Vertex Coord (Top Left)

			glTexCoord2f(1.0,1.0)								# Texture Coord (Top Right)
			glVertex2f(self.char[c][1],self.char[c][2])		# Vertex Coord (Top Right)
			
			glTexCoord2f(1.0,0)								# Texture Coord (Bottom Right)
			glVertex2f(self.char[c][1],0)					# Vertex Coord (Bottom Right)
			
			glEnd()											# Done Building Our Quad (Character)
			glTranslated(self.char[c][1]-self.fontKerning,0,0)							# Move To The Right Of The Character
			glEndList()				

		self.char = tuple(self.char)
		self.lw = self.char[ord('0')][1]
		self.lh = self.char[ord('0')][2]
		self.height = self.lh
		self.width = self.lw
		
		logging.info('GL_Font - initialision of font %s complete',fontName)
	
	def CreateCharacter(self, s):
		#print "creating character: ", s
		letter_render = self.font.render(s, self.antialias, self.fontColor)
		letter = pygame.image.tostring(letter_render, 'RGBA', 1)
		letter_w, letter_h = letter_render.get_size()
		#print "create texture.... width:", letter_w, "height:", letter_h
		letter_texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, letter_texture)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, letter_w, letter_h, 0, GL_RGBA,
		GL_UNSIGNED_BYTE, letter)

		return (letter_texture, letter_w, letter_h)

	def draw(self,s,x,y):
		s = str(s)
		i = 0
		lx = 0
		length = len(s)
		self.width = self.lw*length
		
		#glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslate(x,y,0)
		glListBase(self.g_base-32)
		glCallLists(length,GL_UNSIGNED_BYTE,s);
		
		

		