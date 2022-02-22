import numpy as np
import sys
import gizeh as gz
import moviepy.editor as mpy
import cairo
from math import ceil
import requests
from DataProcessor import DataProcessor
from PIL import Image
import validators
from datetime import datetime

FPS = 30
FONT_FAMILY = "Lato"
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = 30
HEADER_SIZE = 50
DISPLAY_DATE_SIZE = 40
last = None
pi = 3.14
FAST_TICK_TIME = 1
SLOW_TICK_TIME = 4

def processImage(image, basewidth, baseheight, name):
    image_path = "./temp/" + name + ".png"
    if validators.url(image):
        response = requests.get(image)
        file = open(image_path, "wb")
        file.write(response.content)
        file.close()
    else:
        image_path = image
    img = Image.open(image_path)
    img = img.resize((int(basewidth), int(baseheight)), Image.ANTIALIAS)
    img.save(image_path)
    return image_path

def findRanks(top_items):
    ranks = {}
    for i in range(len(top_items)):
        ranks[top_items[i].name] = i
    return ranks

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Correct format: render.py <data> <duration> <title>")
        exit(1)
    data = sys.argv[1]
    duration = int(sys.argv[2])
    title = sys.argv[3]
    dataProcessor = DataProcessor(data)
    state = dataProcessor.state
    state.duration = duration
    state.printState()

    def make_frame(t):
        global last
        board = state.currentBoard(t)
        next_board = state.nextBoard(t)
        date = board[0]
        date_obj = datetime.strptime(date, '%Y-%m')
        display_date = date_obj.strftime("%b %Y")
        if next_board is None:
            return last
        surface = gz.Surface(width=board[1].W, height=board[1].H, bg_color=(1,1,1))

        top_items = board[1].top()
        unit_time = state.duration / state.count
        day_index = int(t // unit_time)
        height = (board[1].H * board[1].barLPer) / 100
        cur_x, cur_y = board[1].graphBeg()
        change_in_top = 0

        current_ranks = findRanks(top_items)
        next_ranks = findRanks(next_board[1].top())

        translate = {}

        for item, rank in current_ranks.items():
            if item in next_ranks:
                translate[item] = (next_ranks[item] - rank) * height
            else:
                translate[item] = board[1].H - (cur_y + height * rank)

        gizeh_patterns = {}
        bar_colors = {}
        for item in top_items:
            # Resize the icon to required size
            image_path = processImage(item.icon, (board[1].W * board[1].iconPer) / 100, height * 0.95, item.name)

            # Convert the image to image pattern
            image_surface = cairo.ImageSurface.create_from_png(image_path)
            im = 0 + np.frombuffer(image_surface.get_data(), np.uint8)
            im.shape = (image_surface.get_height(), image_surface.get_width(), 4)
            freq = np.bincount(im.reshape(len(im), -1))
            barColor = np.argmax(freq)
            bar_colors[item.name] = barColor
            im = im[:, :, [2, 1, 0, 3]]
            gizeh_pattern = gz.ImagePattern(im)
            gizeh_patterns[item.name] = gizeh_pattern

        for i in range(len(top_items)):
            date_obj = datetime.strptime(date, '%Y-%m')
            extraTime = t - unit_time * day_index
            difference = next_board[1].findItem(top_items[i].name).value - top_items[i].value
            change = int(ceil(difference * (extraTime / unit_time)))
            # print('dayindex = ', day_index, ', unit_time = ', unit_time, ', extraTime = ', extraTime, ', change = ', change, ', currentValue = ', top_items[i].value, ', nextValue = ', next_board[1].findItem(top_items[i].name).value)
            if i == 0:
                change_in_top = change

            width = board[1].barPer * board[1].W / 100
            if i != 0:
                width *= (top_items[i].value + change) / (top_items[0].value + change_in_top)

            # Rectangle for bar
            # print('Bar for', top_items[i].name, 'xy =', (cur_x + width / 2, cur_y + height * 0.95 / 2), ', lx = ',
            #       width, 'ly = ', height * 0.95)
            bar = gz.rectangle(lx=width,
                               ly=height * 0.95,
                               xy=(cur_x + width / 2,
                                   cur_y + height * 0.95 / 2),
                               fill=bar_colors[top_items[i].name])


            # Rectangle for icon
            # print('Icon for', top_items[i].name, 'xy =', (cur_x + width + (board[1].sepPer + board[1].iconPer / 2) * board[1].W / 100, cur_y + height * 0.95 / 2),
            #       ', lx = ', im.shape[1] * 2, 'ly = ', im.shape[0] * 2)
            icon = gz.rectangle(lx=im.shape[1] * 2,
                                ly=im.shape[0] * 2,
                                xy=(cur_x + width, cur_y),
                                fill=gizeh_patterns[top_items[i].name])

            # Value
            # print('Value for', top_items[i].name, 'xy =', (cur_x + width + (2 * board[1].sepPer + board[1].iconPer) * board[1].W / 100,
            #                    cur_y + height * 0.95 / 2), 'value = ', str(top_items[i].value + change))
            text = gz.text(str(top_items[i].value + change),
                           fontfamily=FONT_FAMILY,
                           fontsize=FONT_SIZE,
                           fill=TEXT_COLOR,
                           xy=(cur_x + width + (board[1].sepPer + board[1].iconPer) * board[1].W / 100,
                               cur_y + height * 0.95 / 2),
                           h_align='left')

            # Name
            # print('Value for', top_items[i].name, 'xy =', (cur_x - board[1].sepPer * board[1].W / 200,
            #        cur_y + height * 0.95 / 2), 'value = ', top_items[i].name)
            name = gz.text(top_items[i].name,
                           fontfamily=FONT_FAMILY,
                           fontsize=FONT_SIZE,
                           fill=TEXT_COLOR,
                           xy=(cur_x - board[1].sepPer * board[1].W / 200,
                               cur_y + height * 0.95 / 2),
                           h_align='right')

            # Title
            title_vector = gz.text(title, fontfamily=FONT_FAMILY, fontsize=HEADER_SIZE, fontweight="bold",
                            xy=(board[1].W / 2, (board[1].headerPer * board[1].H / 2) / 100))

            # Clock
            clock_center = (board[1].W * board[1].clockPosW / 100, board[1].H * board[1].clockPosH / 100)
            clock_circle = gz.circle(r=(board[1].circleRadius * board[1].W) / 100, xy=clock_center, fill=(1, 1, 1, 0), stroke_width=12, stroke=(0, 0, 0))
            inner_circle = gz.circle(r=(0.6 * board[1].W) / 100, xy=clock_center, fill=(0, 0, 0, 1))
            tick_1 = gz.polyline(points=[(board[1].W * board[1].clockPosW / 100 - (0.25 * board[1].W / 100),board[1].H * board[1].clockPosH / 100), (board[1].W * board[1].clockPosW / 100 + (0.25 * board[1].W / 100), board[1].H * board[1].clockPosH / 100),
                                         (board[1].W * board[1].clockPosW / 100, board[1].H * board[1].clockPosH / 100 - board[1].W * 4 / 100)], fill=(0, 0, 0), close_path=True, stroke_width=5)
            tick_2 = gz.polyline(points=[(board[1].W * board[1].clockPosW / 100 - (0.25 * board[1].W / 100), board[1].H * board[1].clockPosH / 100), (board[1].W * board[1].clockPosW / 100 + (0.25 * board[1].W / 100), board[1].H * board[1].clockPosH / 100),
                                         (board[1].W * board[1].clockPosW / 100, board[1].H * board[1].clockPosH / 100 - board[1].W * 4 / 100)], fill=(0, 0, 0), close_path=True, stroke_width=3)
            tick_2 = tick_2.rotate(2 * pi / 3, center=clock_center)

            tick_2 = tick_2.rotate(2 * pi * t / FAST_TICK_TIME, center=clock_center)
            tick_1 = tick_1.rotate(2 * pi * t / SLOW_TICK_TIME, center=clock_center)

            clock_circle.draw(surface)
            inner_circle.draw(surface)
            tick_1.draw(surface)
            tick_2.draw(surface)

            group = gz.Group([name, bar, icon, text])
            group = group.translate(xy=[0, translate[top_items[i].name] * extraTime / unit_time])
            group.draw(surface)
            title_vector.draw(surface)
            cur_y += height

        display_date_gz = gz.text(display_date, fontfamily=FONT_FAMILY, fontsize=DISPLAY_DATE_SIZE, fontweight="bold",
                                  xy=(board[1].W * board[1].clockPosW / 100, board[1].H * (board[1].clockPosH - 15) / 100))
        display_date_gz.draw(surface)

        ret = surface.get_npimage(transparent=True)
        ret[:,:,3] = 230
        last = ret
        return ret


    clip = mpy.VideoClip(make_frame, duration=duration + state.standstill)
    clip = mpy.VideoFileClip("out/temp.mp4")
    clip = clip.subclip(0, duration + state.standstill)

    graphics_clip_mask = mpy.VideoClip(lambda t: make_frame(t)[:, :, 3] / 255.0,
                                   duration=clip, ismask=True)
    graphics_clip = mpy.VideoClip(lambda t: make_frame(t)[:, :, :3],
                              duration=duration + state.standstill).set_mask(graphics_clip_mask)

    final_clip = mpy.CompositeVideoClip(
        [clip,
         graphics_clip],
        size=(1920, 1080)
    )

    audio = mpy.AudioFileClip("bg_audio.mp3")
    final_clip.audio = audio.audio_loop(duration=duration)
    final_clip.write_videofile('./out/' + '_'.join(title.split(' ')) + '.mp4', fps=FPS)

    # clip.ipython_display(fps=FPS, width=state.W, autoplay=1, loop=1)
