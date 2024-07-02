import dxcam
import keyboard
import numpy as np
from PIL import ImageGrab
import time
import pygetwindow as gw

class Head:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.width = xmax - xmin
        self.height = ymax - ymin
        self.xcenter = xmin + (self.width / 2)
        self.ycenter = ymin + (self.height / 2)


def check_for_yellow(screenshot):
    yellow = (
            (screenshot[:, :, 0] >= lower_yellow[0]) & (screenshot[:, :, 0] <= upper_yellow[0]) &
            (screenshot[:, :, 1] >= lower_yellow[1]) & (screenshot[:, :, 1] <= upper_yellow[1]) &
            (screenshot[:, :, 2] >= lower_yellow[2]) & (screenshot[:, :, 2] <= upper_yellow[2])
    )

    return np.column_stack(np.where(yellow))


def select():
    global interval, loop, delay, rounds
    
    try:
        win = gw.getWindowsWithTitle('Command Prompt')[0]
    
        win.activate()
        time.sleep(0.1)
        win.restore()

    except Exception as e:
        print(e)

    menu_select = input('Choose what gun you are using (all lowercase), or type "exit" to exit this program. ')

    if menu_select == 'exit':
        loop = False

    elif menu_select == 'classic':
        interval = 3
        rounds = 6.75

    elif menu_select == 'shorty':
        interval = 1
        rounds = 3.33

    elif menu_select == 'frenzy':
        interval = 4
        rounds = 10

    elif menu_select == 'ghost':
        interval = 5
        rounds = 6.75

    elif menu_select == 'sheriff':
        interval = 1
        rounds = 4

    elif menu_select == 'stinger':
        interval = 5
        rounds = 16

    elif menu_select == 'spectre':
        interval = 5
        rounds = 13.33

    elif menu_select == 'bucky':
        interval = 1
        rounds = 1.1

    elif menu_select == 'judge':
        interval = 1
        rounds = 3.5

    elif menu_select == 'bulldog':
        interval = 3
        rounds = 10

    elif menu_select == 'guardian':
        interval = 3
        rounds = 5.25

    elif menu_select == 'phantom':
        interval = 4
        rounds = 11

    elif menu_select == 'vandal':
        interval = 3
        rounds = 9.75

    elif menu_select == 'marshal':
        interval = 1
        rounds = 1.5

    elif menu_select == 'outlaw':
        interval = 2
        rounds = 2.75

    elif menu_select == 'operator' or menu_select == 'op':
        interval = 1
        rounds = 0.6

    elif menu_select == 'ares':
        interval = 4
        rounds = 13

    elif menu_select == 'odin':
        interval = 12
        rounds = 12

    else:
        print('Not a valid statement.')
        select()

    delay = (interval / rounds) / interval


# Initializing color bounds for yellow
lower_yellow = np.array([230, 230, 0])
upper_yellow = np.array([255, 255, 100])

# Grabbing image through screenshot to find size of monitor
shot = ImageGrab.grab()
w, h = shot.size
center = [w / 2, h / 2]

# Change variables depending on the size of the screenshot you want to be taken
width = 250
height = 10

# Sets image in the center with given width and height
left, top, right, bottom = center[0] - width / 2, center[1] - (height / 2), center[0] + width / 2, center[1] + (height / 2)
left, top, right, bottom = int(left), int(top), int(right), int(bottom)
region = (left, top, right, bottom)
print(region)

# Simple initialization in case of undefined vars later on
loop = True
interval = 1
delay = 0

select()

# Initializes DirectX camera (FPS should not exceed 160)
camera = dxcam.create(device_idx=0, output_idx=0, region=region)
camera.start(target_fps=144, video_mode=True)

while loop:

    if keyboard.is_pressed('ctrl+p'):
        select()

    frame = camera.get_latest_frame()

    # Finds all yellow points
    coordinates = check_for_yellow(frame)

    # Given that there is yellow, finds maxes and minimums
    if len(coordinates) > 0:
        min_y, min_x = np.min(coordinates, axis=0)
        max_y, max_x = np.max(coordinates, axis=0)

        # Sometimes the yellow on enemy head is only on one side or there are multiple enemies
        if max_x - min_x < 10 or max_x - min_x > 150:

            # Just assumes that the head is 30 pixels by 30 pixels
            head = Head(min_x, min_y, min_x + 30, min_y + 30)
            x_distance, y_distance = abs(head.xcenter - width / 2), abs(head.ycenter - height / 2)
        else:
            head = Head(min_x, min_y, max_x, max_y)
            x_distance, y_distance = abs(head.xcenter - width / 2), abs(head.ycenter - height / 2)

        # Checks if crosshair is on head
        if x_distance < (head.width / 2) and y_distance < (head.height / 2):
            for i in range(interval):
                keyboard.press_and_release('0')
                time.sleep(delay)

            time.sleep(0.5)


print('Triggerbot completed.')
camera.stop()
