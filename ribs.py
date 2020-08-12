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

#
# Utility
#

running = True
def is_running():
    """Is the game currently running?"""
    return running


def quit_game():
    """Pull the brakes and stop the game!"""
    global running
    running = False


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
    global last_frame_held_buttons
    last_frame_held_buttons = current_frame_held_buttons.copy()
    for event in pg.event.get():
        if _event_is(event, "Quit"):
            quit_game()
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
# Main loop
# Do your stuff here!
# :D
#

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
def main():
    """The program starts here"""
    pg.init()
    pg.display.init()

    # Sets the screen resolution.
    pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    frame_clock = pg.time.Clock()

    while is_running():
        # Tell Pygame we're on a new frame, with the given framerate
        # set it to zero to unlimit.
        frame_clock.tick(60)
        # See what buttons are pressed this frame.
        process_events()

        if key_pressed("A"):
            print("Pressed the button")

        # Update the display
        pg.display.flip()

    pg.display.quit()
    pg.quit()

# This has to be at the bottom, because of python reasons.
if __name__ == "__main__":
    main()
