import numpy as np
import gizeh as gz
import moviepy.editor as mpy

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
		surface = gizeh.Surface(board.W, board.H)
		topItems = board.top()
		widths = [topItems[i].value * board.graphWPer / (100 * topItems[0].value) for i in range(len(topItems))]
		height = (board.H * board.graphHPer) / (100 * len(topItems))
		cur_x, cur_y = board.graphBeg()
		for item in len(topItems):
			
			cur_x += height
			pass
		return surface.get_npimage()


	clip = mpy.VideoClip(make_frame, duration=duration)
	clip.write_videofile('./out/' + data + '.mp4', fps=FPS)

	clip.ipython_display(fps=FPS, width=W, autoplay=1, loop=1)