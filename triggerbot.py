import dxcam
from PIL import Image, ImageGrab
import pygetwindow as gw
import time
import keyboard

# Takes initial screenshot and finds dimensions
screenshot = ImageGrab.grab()
width, height = screenshot.size
center = [width / 2 + 30, height / 2 + 20] #  Offset helps with left-right flicking

# Edit depending on offset from center
offset = 10
left, top, right, bottom = (center[0] - offset, center[1] - offset, center[0] + offset, center[1] + offset)
left, top, right, bottom = int(left), int(top), int(right), int(bottom)
region = (left, top, right, bottom)

# Activates VALORANT window
try:
    gw.getWindowsWithTitle('VALORANT')[0]
except:
    print('Open the VALORANT application before running this project.')

win = gw.getWindowsWithTitle('VALORANT')[0]
win.minimize()
win.maximize()
time.sleep(1)

# Screenshot initialization
camera = dxcam.create()
camera.start(region=region, target_fps=90) # Do not set over 160 FPS

try:
    while not keyboard.is_pressed('9'):
        frame = camera.get_latest_frame()

        if frame is None:
            continue

        try:
            img = Image.fromarray(frame)
        except Exception as e:
            print(f'Error converting frame to image: {e}')
            continue

        found = False
        for i in range(offset * 2):
            for j in range(offset * 2):
                pixel_rgb = img.getpixel((i, j))

                if pixel_rgb[0] > 230 and pixel_rgb[1] > 230 and pixel_rgb[2] < 100:
                    if not keyboard.is_pressed('w') and not keyboard.is_pressed('a') and not keyboard.is_pressed('s') and not keyboard.is_pressed('d'):
                        
                        # Crouch spray (can edit depending on use)
                        keyboard.press('0')
                        keyboard.press('ctrl')
                        time.sleep(0.3)
                        keyboard.release('0')
                        keyboard.release('ctrl')
                        time.sleep(0.5)
                        found = True
                        
                        break
                if found:
                    break
            if found:
                break
finally:
    camera.stop()
    print("Camera stopped.")
