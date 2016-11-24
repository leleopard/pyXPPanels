import OpenGLlib

G1000FontName = "data/fonts/ProFontWindows.ttf"
FONT_SIZE_VSMALL 	= 11	#TURQUOISE WHITE
FONT_SIZE_SMALL 	= 13	# TURQUOISE WHITE
FONT_SIZE_MED 		= 15		
FONT_SIZE_LARGE 	= 17	#PINK WHITE GREY PINK WHITE GREY
FONT_SIZE_VLARGE 	= 20	# WHITE

TXT_COLOR_WHITE 	= (255,255,255)
TXT_COLOR_PINK 		= (254,0,254)
TXT_COLOR_GREY 		= (128,128,128)
TXT_COLOR_TURQUOISE = (0,255,255)
TXT_COLOR_GREEN = (0,213,0)

fontKerning = 1
antialias = True

#def __init__(self,fontName,fontSize, fontColor = (255,255,255), antialias = True, fontKerning = 0):
	
FONT_VSMALL_WHITE = 	OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_VSMALL, TXT_COLOR_WHITE, antialias, fontKerning)
FONT_VSMALL_TURQUOISE = OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_VSMALL, TXT_COLOR_TURQUOISE, antialias, fontKerning)

FONT_SMALL_WHITE = 		OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_SMALL, TXT_COLOR_WHITE, antialias, fontKerning+1)
FONT_SMALL_TURQUOISE = 	OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_SMALL, TXT_COLOR_TURQUOISE, antialias, fontKerning+1)
FONT_SMALL_GREEN =	 	OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_SMALL, TXT_COLOR_GREEN, antialias, fontKerning+1)

FONT_MED_WHITE = 		OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_MED, TXT_COLOR_WHITE, antialias, fontKerning)
FONT_MED_GREY = 		OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_MED, TXT_COLOR_GREY, antialias, fontKerning)
FONT_MED_TURQUOISE = 		OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_MED, TXT_COLOR_TURQUOISE, antialias, fontKerning)

FONT_LARGE_WHITE = 		OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_LARGE, TXT_COLOR_WHITE, antialias, fontKerning)
FONT_LARGE_PINK  = 		OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_LARGE, TXT_COLOR_PINK, antialias, fontKerning)
FONT_LARGE_GREY  = 		OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_LARGE, TXT_COLOR_GREY, antialias, fontKerning)
FONT_LARGE_TURQUOISE  = 		OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_LARGE, TXT_COLOR_TURQUOISE, antialias, fontKerning)

FONT_VLARGE_WHITE = 	OpenGLlib.GL_Font(G1000FontName, FONT_SIZE_VLARGE, TXT_COLOR_WHITE, antialias, fontKerning)
