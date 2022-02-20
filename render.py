import numpy as np
import gizeh as gz
import moviepy.editor as mpy
import cairo
from PIL import Image


FPS = 30
FONT_FAMILY = "Lato"
TEXT_COLOR = (0,0,0)
FONT_SIZE = 25

def resizeImage(image, basewidth, baseheight):
	img = Image.open(image)
	img = img.resize((basewidth, baseheight), Image.ANTIALIAS)
	img.save(image)


if __name__ == "__main__":
	if sys.argc < 3:
		print("Correct format: render.py <data> <duration>")
		exit(1)
	data = sys.argv[1]
	duration = (int)sys.argv[2]
	dataProcessor = DataProcessor(data)
	state = dataProcessor.state

	def make_frame(t):
		board = state.currentBoard(t)
		surface = gizeh.Surface(board.W, board.H)
		topItems = board.top()
		widths = [topItems[i].value * board.barPer / (100 * topItems[0].value) for i in range(len(topItems))]
		height = (board.H * board.graphHPer) / (100 * len(topItems))
		cur_x, cur_y = board.graphBeg()
		for i in len(topItems):
			# Rectangle for bar
			bar = gz.rectangle(lx=widths[i], ly=height*0.95, xy=(cur_x + board.W * widths[i] / (2 * 100), cur_y + height*0.95/2), fill=topItems[i].color)

			# Resize the icon to required size
			resizeImage(topItems[i].icon, (self.W * self.iconPer) / 100, height*0.95)

			# Convert the image to image pattern
			image_surface = cairo.ImageSurface.create_from_png(topItems[i].icon)
			im = 0+numpy.frombuffer(image_surface.get_data(), numpy.uint8)
			im.shape = (image_surface.get_height(), image_surface.get_width(), 4)
			im = im[:,:,[2,1,0,3]]
			gizeh_pattern = gizeh.ImagePattern(im)

			# Rectangle for icon
			icon = gz.rectangle(lx=im.shape[1]*2, ly=im.shape[0]*2, xy=(cur_x + widths[i] + (board.sepPer + board.iconPer/2) * board.W / 100, cur_y + height*0.95/2), fill=gizeh_pattern)


			# Text
			text = gz.text(topItems[i].value, fontfamily=FONT_FAMILY, fontsize=FONT_SIZE, fill=TEXT_COLOR, xy=(cur_x + widths[i] + (2*board.sepPer + board.iconPer + board.valuePer/2) * board.W / 100, cur_y + height*0.95/2))

			# Name
			name = gz.text(topItems[i].name, fontfamily=FONT_FAMILY, fontsize=FONT_SIZE, fill=TEXT_COLOR, xy=(cur_x - board.sepPer * board.W / 200, cur_y + height*0.95/2), h_align='right')

			group = gz.group([name, bar, icon, text])
			group.draw(surface)
			cur_x += height

		return surface.get_npimage()


	clip = mpy.VideoClip(make_frame, duration=duration)
	clip.write_videofile('./out/' + data + '.mp4', fps=FPS)

	clip.ipython_display(fps=FPS, width=W, autoplay=1, loop=1)