from PIL import Image
import sys

nrImagesPerLine = 16
x_offset = 2
x_spacing = 122
y_spacing = 66

compassImages = []
for i in range(0,361):
	imgIndex = '{:03.0f}'.format(i)
	compassImages.append(Image.open("data/azimut/gen_azimut"+imgIndex+"-1.png"))

texture = Image.new("RGBA", (2048, 2048))
for i in range (0,361):
	x = i%nrImagesPerLine
	y = i//nrImagesPerLine
	print "i: ", i, " x: ", x, " y: ", y 
	texture.paste(compassImages[i], (x_offset+x*x_spacing,y*y_spacing))

texture.save("output_texture.png")