import numpy as np
import sys
import gizeh as gz
import moviepy.editor as mpy
import cairo
import DataProcessor
from PIL import Image

FPS = 30
FONT_FAMILY = "Lato"
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = 25

last = None


def resizeImage(image, basewidth, baseheight):
    img = Image.open(image)
    img = img.resize((basewidth, baseheight), Image.ANTIALIAS)
    img.save(image)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Correct format: render.py <data> <duration>")
        exit(1)
    data = sys.argv[1]
    duration = int(sys.argv[2])
    dataProcessor = DataProcessor(data)
    state = dataProcessor.state


    def make_frame(t):
        global last
        board = state.currentBoard(t)
        next_board = state.nextBoard(t)
        if next_board is None:
            return last
        surface = gz.Surface(board.W, board.H)
        top_items = board.top()
        unit_time = state.duration / state.count
        day_index = t / unit_time
        height = (board.H * board.graphHPer) / (100 * len(top_items))
        cur_x, cur_y = board.graphBeg()
        change_in_top = 0
        for i in len(top_items):
            extraTime = t - unit_time * day_index
            difference = next_board.findItem(top_items[i].name).value - top_items[i].value
            change = int(difference * (extraTime / unit_time))

            if i == 0:
                change_in_top = change

            width = board.barPer * board.W / 100
            if i != 0:
                width *= (top_items[i].value + change) / change_in_top

            # Rectangle for bar
            bar = gz.rectangle(lx=width,
                               ly=height * 0.95,
                               xy=(cur_x + width / 2,
                                   cur_y + height * 0.95 / 2),
                               fill=top_items[i].color)

            # Resize the icon to required size
            resizeImage(top_items[i].icon, (state.W * state.iconPer) / 100, height * 0.95)

            # Convert the image to image pattern
            image_surface = cairo.ImageSurface.create_from_png(top_items[i].icon)
            im = 0 + np.frombuffer(image_surface.get_data(), np.uint8)
            im.shape = (image_surface.get_height(), image_surface.get_width(), 4)
            im = im[:, :, [2, 1, 0, 3]]
            gizeh_pattern = gz.ImagePattern(im)

            # Rectangle for icon
            icon = gz.rectangle(lx=im.shape[1] * 2,
                                ly=im.shape[0] * 2,
                                xy=(cur_x + width + (board.sepPer + board.iconPer / 2) * board.W / 100,
                                    cur_y + height * 0.95 / 2),
                                fill=gizeh_pattern)

            # Value
            text = gz.text(top_items[i].value + change,
                           fontfamily=FONT_FAMILY,
                           fontsize=FONT_SIZE,
                           fill=TEXT_COLOR,
                           xy=(cur_x + width + (2 * board.sepPer + board.iconPer + board.valuePer / 2) * board.W / 100,
                               cur_y + height * 0.95 / 2))

            # Name
            name = gz.text(top_items[i].name,
                           fontfamily=FONT_FAMILY,
                           fontsize=FONT_SIZE,
                           fill=TEXT_COLOR,
                           xy=(cur_x - board.sepPer * board.W / 200,
                               cur_y + height * 0.95 / 2),
                           h_align='right')

            group = gz.group([name, bar, icon, text])
            group.draw(surface)
            cur_x += height

        last = surface.get_npimage()

        return surface.get_npimage()


    clip = mpy.VideoClip(make_frame, duration=duration + state.standstill)
    clip.write_videofile('./out/' + data + '.mp4', fps=FPS)

    clip.ipython_display(fps=FPS, width=state.W, autoplay=1, loop=1)
