import logging
import decimal
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
D = decimal.Decimal

from lib.graphics import fonts
from lib.graphics import OpenGL3lib
from lib.graphics import graphicsGL3

class Console(graphicsGL3.Window):
	
	def __init__(self,position, size, eventManager, batchImageRenderer, layer = 0):
		
		self.titleBarFont = OpenGL3lib.GL_Font("data/fonts/Envy-Code-R.ttf", fonts.FONT_SIZE_MED, fonts.TXT_COLOR_WHITE, True, 0)
		self.consoleFont = OpenGL3lib.GL_Font("data/fonts/Envy-Code-R.ttf", fonts.FONT_SIZE_SMALL, fonts.TXT_COLOR_WHITE, True, 0)
		
		graphicsGL3.Window.__init__(self,position, size, eventManager, self.titleBarFont, batchImageRenderer, layer, "Console Window")
		#self.clipping = True
		self.setTitleText("Loading...")
		
		self.textBox = graphicsGL3.TextBox((0,0),(self.width-2, self.height - self.titleBarHeight-2),eventManager,"data/fonts/Envy-Code-R.ttf", fonts.FONT_SIZE_MED, fonts.TXT_COLOR_WHITE)
		self.addItem(self.textBox,(1,1),False)
		
	def eventCallback(self,event):
		super(Console,self).eventCallback(event) # call windows evencallback method to handle mouse drag etc
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F1:
				self.setVisible ( not self.visible)
		
	def writeLine(self, s):
		self.textBox.writeLine(s)
	
	def refreshScreenAndDraw(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		self.draw()
		pygame.display.flip()
		
	def draw(self):
		super(Console,self).draw()
		
