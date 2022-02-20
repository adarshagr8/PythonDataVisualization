import numpy as np
import gizeh as gz
import moviepy.editor as mpy

W, H = 1920, 1080
FPS = 30

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

	clip = mpy.VideoClip(make_frame, duration=duration)
	clip.write_videofile('./out/' + data + '.mp4', fps=FPS)

	clip.ipython_display(fps=FPS, width=W, autoplay=1, loop=1)