import dxcam
import keyboard
import numpy as np
from PIL import ImageGrab
import time


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


# Initializing color bounds for yellow
lower_yellow = np.array([200, 200, 0])
upper_yellow = np.array([255, 255, 200])

# Grabbing image through screenshot to find size of monitor
shot = ImageGrab.grab()
w, h = shot.size
center = [w / 2, h / 2]

# Change variables depending on the size of the screenshot you want to be taken
width = 500
height = 10

# Sets image in the center with given width and height
left, top, right, bottom = center[0] - width / 2, center[1] - (height / 2), center[0] + width / 2, center[1] + (height / 2)
left, top, right, bottom = int(left), int(top), int(right), int(bottom)
region = (left, top, right, bottom)
print(region)

# Initializes DirectX camera
camera = dxcam.create(device_idx=0, output_idx=0, region=region)
camera.start(target_fps=120)

while not keyboard.is_pressed('9'):
    frame = camera.get_latest_frame()

    # Finds all yellow points
    coordinates = check_for_yellow(frame)

    # Given that there is yellow, finds maxes and mins
    if len(coordinates) > 0:
        min_y, min_x = np.min(coordinates, axis=0)
        max_y, max_x = np.max(coordinates, axis=0)

        # Sometimes the yellow on enemy head is only on one side or there are multiple enemies
        if max_x - min_x < 10 or max_x - min_x > 150:
            head = Head(min_x, min_y, min_x + 30, min_y + 30)
            x_distance, y_distance = abs(head.xcenter - width / 2), abs(head.ycenter - height / 2)
        else:
            head = Head(min_x, min_y, max_x, max_y)
            x_distance, y_distance = abs(head.xcenter - width / 2), abs(head.ycenter - height / 2)

        # Checks if crosshair is on head
        if x_distance < (head.width / 2) and y_distance < head.height / 2:
            keyboard.press_and_release('0')
            time.sleep(0.25)


print('Process over.')
camera.stop()
