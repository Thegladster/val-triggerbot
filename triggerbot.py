import bettercam
import time
from PIL import ImageGrab
import numpy as np
import pygetwindow as gw
import keyboard


class Head:
    def __init__(self, xmin, xmax, ymax):

        # In the case that only half the head or multiple enemies are in frame
        if xmax - xmin > 150 or xmax - xmin < 10:
            self.width = 30
        else:
            self.width = xmax - xmin

        self.height = self.width
        self.xcenter = xmin + (self.width / 2)
        self.ycenter = ymax - (self.height / 2)

    def __str__(self):
        return f'x: {self.xcenter}, y: {self.ycenter}, w: {self.width}, h: {self.height}'


def check_for_yellow(screenshot):

    # Initializing color bounds for yellow
    lower_yellow = np.array([230, 230, 0])
    upper_yellow = np.array([255, 255, 100])

    yellow = (
            (screenshot[:, :, 0] >= lower_yellow[0]) & (screenshot[:, :, 0] <= upper_yellow[0]) &
            (screenshot[:, :, 1] >= lower_yellow[1]) & (screenshot[:, :, 1] <= upper_yellow[1]) &
            (screenshot[:, :, 2] >= lower_yellow[2]) & (screenshot[:, :, 2] <= upper_yellow[2])
    )

    return np.column_stack(np.where(yellow))


def select():
    global interval, loop, delay, f, start

    end = time.perf_counter() - start

    # FPS reporter
    fps = f / end
    print(f'FPS: {fps}')

    try:
        win = gw.getWindowsWithTitle('VALORANT')[0]

        if win.isMinimized:
            pass
        else:
            win.minimize()

    except Exception as e:
        win = 0
        print(f'Open the VALORANT window before starting this project. Error {e}.')
        pass

    menu_select = input('Choose what gun you are using (all lowercase), or type "exit" to exit this program. ')

    if menu_select == 'exit':
        loop = 0
        return

    guns_list = ['classic', 'shorty', 'frenzy', 'ghost', 'sheriff', 'stinger', 'spectre', 'bucky', 'judge', 'bulldog',
                 'guardian', 'phantom', 'vandal', 'marshal', 'outlaw', 'op', 'operator', 'ares', 'odin']
    intervals_list = [3, 1, 4, 1, 1, 5, 5, 1, 1, 3, 2, 3, 2, 1, 2, 1, 1, 4, 12]
    rounds_list = [6.75, 3.33, 10, 6.75, 4, 16, 13.33, 1.1, 3.5, 10, 5.25, 11, 9.75, 1.5, 2.75, 0.6, 0.6, 13, 12]

    if menu_select in guns_list:
        index = guns_list.index(menu_select)
        interval = intervals_list[index]
        rounds = rounds_list[index]

        print(f'Using gun {menu_select}.')

        delay = (interval / rounds) / interval

        win.restore()
        win.maximize()

        # FPS reset
        f = 0
        start = time.perf_counter()

    else:
        print('Not a valid statement.')
        select()
        return


# First variable initialization
loop = 1
interval = 1
delay = 0
f = 0

# Grabbing image through screenshot to find size of monitor
shot = ImageGrab.grab()
w, h = shot.size
center = [w / 2, h / 2]

# Change variables depending on the size of the screenshot you want to be taken
width = 500
height = 15

# Sets image in the center with given width and height
left, top, right, bottom = center[0] - width/2, center[1] - (height/2), center[0] + width/2, center[1] + (height/2)
left, top, right, bottom = int(left), int(top), int(right), int(bottom)
region = (left, top, right, bottom)
print(region)

# Camera initialization
camera = bettercam.create(device_idx=0, output_idx=0, region=region)
keyboard.add_hotkey('alt+p', select)

# Select menu for gun
start = 0
select()

while loop:

    # Frame 1
    frame = camera.grab()

    if frame is None:
        continue

    # FPS reporter
    f += 1

    # Finds all yellow points
    coordinates = check_for_yellow(frame)

    # Given that there is yellow, finds distance
    if len(coordinates) > 0:
        min_y, min_x = np.min(coordinates, axis=0)
        max_y, max_x = np.max(coordinates, axis=0)

        head = Head(min_x, max_x, max_y)

        # Finds distance from crosshair
        a = head.xcenter - width / 2
        b = head.ycenter - height / 2

        # Pythagorean theorem came in clutch for once
        c = (a ** 2 + b ** 2) ** 0.5
        max_dist = abs(head.width / 2)

        if c <= max_dist:
            for i in range(interval):
                keyboard.press_and_release('0')
                time.sleep(delay)

            time.sleep(delay * interval)
            continue

print('Program exited.')
