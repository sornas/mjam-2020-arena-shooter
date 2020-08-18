#
# The offical LiTHe kod code skeleton for PyGame development.
# 2020 by Edvard Thörnros
#
# The aim of this file is to give a collection of usable functions
# and structures to be used as a jumping off point. Feel free
# to change and distribute!
#
# Functions that start with an underscore, are probably not
# interesting to read, they are functions that build other
# more usable functions.

import pygame as pg
# For smaller cheat sheet see:
#   https://www.lithekod.se/pygame.html
# For official pygame documentation see:
#   https://www.pygame.org/docs/

# math has sin, cos and other interesting things.
import math

#
# Input handling
#

def _event_is(event: pg.event, kind: str) -> bool:
    """Internal function to check the kind of pygame event"""
    return pg.event.event_name(event.type) == kind


current_frame_held_buttons = set()
last_frame_held_buttons = None
def process_events():
    """Tells the game what buttons are pressed."""
    running = True
    global last_frame_held_buttons
    last_frame_held_buttons = current_frame_held_buttons.copy()
    for event in pg.event.get():
        if _event_is(event, "Quit"):
            running = False
        elif _event_is(event, "KeyDown"):
            current_frame_held_buttons.add(event.key)
        elif _event_is(event, "KeyUp"):
            current_frame_held_buttons.remove(event.key)
        elif _event_is(event, "MouseButtonUp"):
            ...
        elif _event_is(event, "MouseButtonDown"):
            ...
        elif _event_is(event, "MouseMotion"):
            ...
    return running


def _to_keycode(key):
    """
        Takes a keycode or a character and converts it to a keycode

        A keycode is a number that uniquely identifies a keyboard key.
        And a character is what you get when typing that key on the keyboard.
    """
    if type(key) == str:
        if len(key) != 1:
            raise "error"
        return ord(key.lower())
    return key


def key_down(key):
    """
        Takes a key, that's either a keycode or a character,
        and says if it's down or not
    """
    keycode = _to_keycode(key)
    return keycode in current_frame_held_buttons


def key_released(key):
    """
        Takes a key, that's either a keycode or a character,
        and says if it was released this frame.
    """
    keycode = _to_keycode(key)
    return (keycode not in current_frame_held_buttons) and \
           (keycode in last_frame_held_buttons)


def key_pressed(key):
    """
        Takes a key, that's either a keycode or a character,
        and says if it was pressed down this frame.
    """
    keycode = _to_keycode(key)
    return (keycode in current_frame_held_buttons) and \
           (keycode not in last_frame_held_buttons)


#
# Simple sprite drawing
#

def draw_transformed(img, pos, scale=(1., 1.), degrees=0):
    """
        Draw img centered at position, scale the image and then rotate it in
        degrees before drawing.
    """
    if scale[0] != 1. or scale[1] != 1.:
        w, h = img.get_size()
        w = int(w * scale[0])
        h = int(h * scale[1])
        img = pg.transform.scale(img, (w, h))
    if degrees:
        # Pygame rotates CCW in degrees, for some reason.
        img = pg.transform.rotate(img, -degrees)
    w, h = img.get_size()
    window = pg.display.get_surface()
    window.blit(img, (int(pos[0] - w / 2.0), int(pos[1] - h / 2.0)))


def clear_screen(color):
    """Fill the screen with color"""
    window = pg.display.get_surface()
    top_left = (0, 0)
    bottom_right = pg.display.get_surface().get_size()
    pg.draw.rect(window, color, (top_left, bottom_right))


#
# Main loop
# Do your stuff here!
# :D
#

teapot = pg.image.load("teapot.png")

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FRAMERATE = 60
DELTA = 1 / FRAMERATE
def main():
    """The program starts here"""
    pg.init()
    pg.display.init()

    # Sets the screen resolution.
    pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    frame_clock = pg.time.Clock()

    time = 0
    num_teapots = 1
    # See what buttons are pressed this frame, and continue if we haven't quit.
    while process_events():
        # Tell Pygame we're on a new frame, with the given framerate
        # set it to zero to unlimit.
        frame_clock.tick(FRAMERATE)
        time += DELTA
        # See what buttons are pressed this frame.
        process_events()

        if key_pressed("A"):
            num_teapots += 1

        for i in range(num_teapots):
            r = 100
            a = i * 1 / 5 + time
            x = math.cos(a) * r + SCREEN_WIDTH / 2
            y = math.sin(a) * r + SCREEN_WIDTH / 2
            draw_centered(teapot, (x, y), (0.5, 2.0), a * 180 / math.pi)

        # Update the display
        pg.display.flip()
        clear_screen(pg.Color(0, 0, 0))

    pg.display.quit()
    pg.quit()

# This has to be at the bottom, because of python reasons.
if __name__ == "__main__":
    main()
