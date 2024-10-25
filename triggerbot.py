import bettercam
import keyboard
import pygetwindow as gw
from colorama import init as colorama_init, Fore
import numpy as np
import time
from PIL import ImageGrab
from pynput.mouse import Button, Controller


class Enemy:
    def __init__(self, xmin, xmax, ymin, ymax):

        self.head_width = xmax - xmin
        self.head_height = self.head_width * 1.5
        self.head_xcenter = xmin + (self.head_width / 2)
        self.head_ycenter = ymin + (self.head_height / 2)
        self.body_width = self.head_width * 2
        self.body_height = ymax - ymin + self.head_height
        self.body_xcenter = self.head_xcenter
        self.body_ycenter = ymin + self.head_height + (self.body_height / 2)

    def __str__(self):
        return (f'Head: x: {self.head_xcenter}, y: {self.head_ycenter}, w: {self.head_width}, h: {self.head_height}, '
                f'Body: x: {self.body_xcenter}, y: {self.body_ycenter}, w: {self.body_width}, h: {self.body_height}')


def check_for_yellow(screenshot):

    # Initializing color bounds for yellow
    lower_yellow = np.array([200, 200, 0])
    upper_yellow = np.array([255, 255, 100])

    yellow = (
            (screenshot[:, :, 0] >= lower_yellow[0]) & (screenshot[:, :, 0] <= upper_yellow[0]) &
            (screenshot[:, :, 1] >= lower_yellow[1]) & (screenshot[:, :, 1] <= upper_yellow[1]) &
            (screenshot[:, :, 2] >= lower_yellow[2]) & (screenshot[:, :, 2] <= upper_yellow[2])
    )

    return np.column_stack(np.where(yellow))


def select():
    global camera, select_uses, loop, start, fps, delay, interval, hold, gun_select

    if select_uses == 0:
        print(f'{Fore.LIGHTYELLOW_EX}[i] Welcome. Press {Fore.LIGHTWHITE_EX}alt + p{Fore.LIGHTYELLOW_EX} '
              f'to return to this menu once in-game to {Fore.LIGHTMAGENTA_EX}change gun or check FPS.{Fore.RESET}')
        print('')
    elif select_uses == 1:
        print(Fore.LIGHTYELLOW_EX)
        print(f'[i] FPS: {int(fps / (time.perf_counter() - start))}. ')
        print(Fore.LIGHTGREEN_EX)
        print(f'[?] FPS seem slow? Refer to the GitHub repository: '
              f'{Fore.LIGHTBLUE_EX}https://github.com/Thegladster/val-triggerbot')
    else:
        print(Fore.LIGHTYELLOW_EX)
        print(f'[i] FPS: {int(fps / (time.perf_counter() - start))}{Fore.RESET}')
    try:
        win = gw.getWindowsWithTitle('VALORANT')[0]

        if not win.isMinimized:
            win.minimize()

    except Exception as e:
        print(f'{Fore.RED}Error {e}: Make sure the VALORANT application is open prior to use.')
        print('')
        win = None

    gun_dict = {
        'classic': [2, 6.75, False],
        'shorty': [1, 3.33, False],
        'frenzy': [3, 10, True],
        'ghost': [2, 5, False],
        'sheriff': [1, 2, False],
        'stinger': [3, 16, True],
        'spectre': [3, 13.33, True],
        'bucky': [1, 1.1, False],
        'judge': [1, 3.5, False],
        'bulldog': [2, 10, True],
        'guardian': [1, 3, False],
        'phantom': [2, 8, True],
        'vandal': [3, 10, True],
        'marshal': [1, 1.5, False],
        'outlaw': [1, 2.75, False],
        'op': [1, 0.6, False],
        'operator': [1, 0.6, False],
        'ares':  [3, 13, True],
        'odin': [3, 12, True],
        'jett': [2, 6, True],
        'neon': [8, 12, True]
    }

    gun_select = input(f'{Fore.LIGHTGREEN_EX}Enter which gun you are using here in \033[4mall lowercase:\033[0m ')

    if gun_select in gun_dict:
        print(f'{Fore.LIGHTYELLOW_EX}[i] Using {Fore.LIGHTGREEN_EX}{gun_select}{Fore.LIGHTYELLOW_EX}.{Fore.RESET}')
        select_uses += 1
        start = time.perf_counter()
        fps = 0

        interval, delay, hold = gun_dict[gun_select]
        delay = (1 / delay)
        return

    elif gun_select == 'exit':
        loop = 0
        return

    print(Fore.LIGHTYELLOW_EX)
    print('⚠  Not a valid gun.')
    print(Fore.RESET)
    select()


# Necessary initializations
colorama_init()
select_uses = 0
loop = 1
fps = 0
start = time.perf_counter()
interval = 1
delay = 0.1
hold = False
crosshair_offset = 0
dist_last = None
blocked = False
mouse = Controller()
gun_select = 'classic'

# Region initialization
shot = ImageGrab.grab()
w, h = shot.size
center = (w / 2, h / 2)

# Change variables depending on the size of the screenshot you want to be taken
width = 100
height = 200

# Sets image in the center with given width and height
left, top, right, bottom = center[0] - width / 2, center[1] - height / 2, center[0] + width / 2, center[1] + height / 2
left, top, right, bottom = int(left), int(top), int(right), int(bottom)
region = (left, top, right, bottom)
print(region)

# Select menu (yes, I know the text is clunky but at least it looks cool)
select()

camera = bettercam.create(output_idx=0, device_idx=0, region=region)
keyboard.add_hotkey('alt+p', select)

while loop:
    frame = camera.grab()

    if frame is None:
        continue

    # FPS counter adjustment
    fps += 1

    # Finds all yellow points
    coordinates = check_for_yellow(frame)

    if len(coordinates) > 0:
        min_y = np.min(coordinates[:, 0])
        max_y = np.max(coordinates[:, 0])

        # Creates a subset of points that rest below the head but above the torso
        subset = coordinates[coordinates[:, 0] < (min_y + 15)]
        x_values = subset[:, 1]

        # Finds the max and min x of these head values
        max_x = np.max(x_values)
        min_x = np.min(x_values)

        enemy = Enemy(min_x, max_x, min_y, max_y)

        if abs(enemy.head_xcenter - width / 2) < enemy.head_width / 2 and abs(enemy.head_ycenter - height / 2) < enemy.head_height / 2:

            if hold:
                mouse.press(Button.left)
                time.sleep(delay * (interval - 1) + 0.05)
                mouse.release(Button.left)
                time.sleep(delay * interval * 1.5)
            else:
                for i in range(interval):
                    mouse.press(Button.left)
                    mouse.release(Button.left)
                    time.sleep(delay)

        elif abs(enemy.body_xcenter - width / 2) < enemy.body_width / 2 and abs(enemy.body_ycenter - height / 2) < enemy.body_height / 2:

            if hold:
                mouse.press(Button.left)
                time.sleep(delay * interval + 0.05)
                mouse.release(Button.left)
                time.sleep(delay * interval * 1.5)
            else:
                if gun_select == 'op' or gun_select == 'operator':
                    for i in range(interval):
                        mouse.press(Button.left)
                        mouse.release(Button.left)
                        time.sleep(delay)
                else:
                    for i in range(interval + 1):
                        mouse.press(Button.left)
                        mouse.release(Button.left)
                        time.sleep(delay)


print('Thanks for stopping by!')
