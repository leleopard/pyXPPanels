from PIL import Image
import sys
import os

out_width = 0
out_height = 0

images = []
for imageFile in sorted(os.listdir("airportPlateImages")):
	image = Image.open("airportPlateImages/"+imageFile)
	images.append(image)
	
	if image.size[0] > out_width:
		out_width = image.size[0]
	out_height += image.size[1]

print "Out width: ", out_width, "Out height: ", out_height

texture = Image.new("RGBA", (out_width, out_height))
x = 0
y = 0

for image in images:
	
	print " x: ", x, " y: ", y 
	texture.paste(image, (x,y))
	y += image.size[1]

texture.save("output_texture.png")