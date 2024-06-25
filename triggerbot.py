import dxcam
from PIL import Image, ImageGrab
import pygetwindow as gw
import time
import keyboard
import sys


# Takes initial screenshot and finds dimensions
screenshot = ImageGrab.grab()
width, height = screenshot.size
center = [width / 2, height / 2]

# Edit depending on offset from center
offset = 25
left, top, right, bottom = (center[0] - offset, center[1] - offset, center[0] + offset, center[1] + offset)
left, top, right, bottom = int(left), int(top), int(right), int(bottom)
region = (left, top, right, bottom)

# Activates VALORANT window
try:
    win = gw.getWindowsWithTitle('VALORANT')[0]

    if win == gw.getWindowsWithTitle('valorant-triggerbot-v3')[0]:
        win = gw.getWindowsWithTitle('VALORANT')[1]

except Exception as e:
    print(f'Error: {e}. Open the VALORANT application before running this project.')
    sys.exit()

win.restore()
time.sleep(0.5)

# Camera initialization and FPS init
camera = dxcam.create(device_idx=0, output_idx=0, output_color='RGB')
a, start = 1, time.time()

# Checks if yellow is within the nxn square around the crosshair
while not keyboard.is_pressed('9'):

    found = 0
    frame = camera.grab(region=region)

    # Checks if frame is NoneType (i.e. no changes since last grab)
    if frame is None:
        continue

    try:
        frame = Image.fromarray(frame)
    except Exception as e:
        print(f'Error {e}.')
        continue

    for i in range(offset * 2):
        for j in range(offset * 2):

            rgb = frame.getpixel((i, j))

            if rgb[0] > 240 and rgb[1] > 240 and rgb[2] < 100:
                if not keyboard.is_pressed('w') and not keyboard.is_pressed('a') and not keyboard.is_pressed('s') and not keyboard.is_pressed('d'):
                    keyboard.press_and_release('0')
                    found = 1

        a += 1

        if found:
            time.sleep(0.5)
            break

end = time.time()
FPS = (a / (end - start))
print(f'Average FPS: {round(FPS)}')
