import bettercam
import keyboard
import pygetwindow as gw
from colorama import init as colorama_init, Fore
import numpy as np
import time
from PIL import ImageGrab


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
    lower_yellow = np.array([230, 230, 0])
    upper_yellow = np.array([255, 255, 100])

    yellow = (
            (screenshot[:, :, 0] >= lower_yellow[0]) & (screenshot[:, :, 0] <= upper_yellow[0]) &
            (screenshot[:, :, 1] >= lower_yellow[1]) & (screenshot[:, :, 1] <= upper_yellow[1]) &
            (screenshot[:, :, 2] >= lower_yellow[2]) & (screenshot[:, :, 2] <= upper_yellow[2])
    )

    return np.column_stack(np.where(yellow))


def select():
    global camera, select_uses, loop, start, fps, delay, interval

    if select_uses == 0:
        print(f'{Fore.LIGHTYELLOW_EX}[i] Welcome. Press {Fore.LIGHTWHITE_EX}alt + p{Fore.LIGHTYELLOW_EX} '
              f'to return to this menu once in-game to {Fore.MAGENTA}change gun or check FPS.{Fore.RESET}')
        print('')
    elif select_uses == 1:
        print(Fore.LIGHTYELLOW_EX)
        print(f'[i] FPS: {int(fps / (time.perf_counter() - start))}{Fore.RESET}')
        print(Fore.LIGHTCYAN_EX)
        print('[?] FPS seem slow (less than 80)? Refer to the GitHub repository: '
              'https://github.com/Thegladster/val-triggerbot')
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
        'classic': [2, 0, 6.75],
        'shorty': [1, 0, 3.33],
        'frenzy': [3, 0, 10],
        'ghost': [2, 0, 6.75],
        'sheriff': [1, 0.1, 4],
        'stinger': [3, 0, 16],
        'spectre': [3, 0, 13.33],
        'bucky': [1, 0, 1.1],
        'judge': [1, 0, 3.5],
        'bulldog': [2, 0, 10],
        'guardian': [2, 0, 5.25],
        'phantom': [2, 0, 11],
        'vandal': [2, 0, 9.75],
        'marshal': [1, 0, 1.5],
        'outlaw': [1, 0, 2.75],
        'op': [1, 0, 0.6],
        'operator': [1, 0, 0.6],
        'ares':  [3, 0, 13],
        'odin': [3, 0, 12]
    }

    gun_select = input(f'{Fore.LIGHTGREEN_EX}Enter which gun you are using here in \033[4mall lowercase:\033[0m ')

    if gun_select in gun_dict:
        print(f'{Fore.LIGHTYELLOW_EX}[i] Using {Fore.LIGHTGREEN_EX}{gun_select}{Fore.LIGHTYELLOW_EX}.{Fore.RESET}')
        select_uses += 1
        start = time.perf_counter()
        fps = 0

        win.maximize()
        (interval, extra_delay, delay) = gun_dict[gun_select]
        delay = (1 / delay) + extra_delay
        return

    elif gun_select == 'exit':
        loop = 0
        return

    print(Fore.RED)
    print('⚠ Not a valid gun.')
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

# Region initialization
shot = ImageGrab.grab()
w, h = shot.size
center = (w / 2, h / 2)

# Change variables depending on the size of the screenshot you want to be taken
width = 75
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
            for i in range(interval):
                keyboard.press_and_release('0')
                time.sleep(delay)

            time.sleep(delay)

        if abs(enemy.body_xcenter - width / 2) < enemy.body_width / 2 and abs(enemy.body_ycenter - height / 2) < enemy.body_height / 2:
            for i in range(interval + 1):
                keyboard.press_and_release('0')
                time.sleep(delay)

            time.sleep(delay)
            
print('Thanks for stopping by!')
