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
        returns True if the corresponding key is pressed.
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

def draw_transformed(img, position, scale=(1., 1.), degrees=0):
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
    window.blit(img, (int(position[0] - w / 2.0), int(position[1] - h / 2.0)))


def clear_screen(color):
    """Fill the screen with color"""
    window = pg.display.get_surface()
    top_left = (0, 0)
    bottom_right = pg.display.get_surface().get_size()
    pg.draw.rect(window, color, (top_left, bottom_right))

#
# Simple physics and collision
#

def overlap_data(a, b):
    """
        Given that a and b overlap, extracts the shortest direction to move
        along and the penetration.

        returns -> normal, depth
        (normal points from a)
    """
    # This code is based on SAT (the shortest distance is along one normal).
    delta = a.centerx - b.centerx, a.centery - b.centery
    span = (a.width + b.width) / 2, (a.height + b.height) / 2

    # Pick the smallest overlapping axis
    overlap = span[0] - abs(delta[0]), span[1] - abs(delta[1])
    depth = min(overlap)

    # Inline helper
    sign = lambda x: 1 if x > 0 else -1

    if abs(overlap[0]) < abs(overlap[1]):
        normal = sign(delta[0]), 0
    else:
        normal = 0, sign(delta[1])

    return normal, depth


def solve_rect_overlap(a, b, vel_a=(0, 0), vel_b=(0, 0), mass_a=1, mass_b=1, bounce=0):
    """
        Solves the collision between a and b, with the mass and velocity as specified.
        A solved collision has no overlap and velocities that do not point into eachother.

        vel  - is the velocity of the body, a direction and a speed.
        mass - is how much each body weighs, if set to 0 they cannot move.
        bounce - is how bouncy the collision is. (For "correct" behaviour > 0.0, < 1.0)
    """
    dot = lambda v, u: v[0] * u[0] + v[1] * u[1]
    add = lambda v, u: (v[0] + u[0], v[1] + u[1])
    scale = lambda v, s: (v[0] * s, v[1] * s)

    normal, depth = overlap_data(a, b)
    if depth < 0: return a, b, vel_a, vel_b, False

    # Positional correction
    total_mass = mass_a + mass_b
    if total_mass != 0:
        effect_a = mass_a / total_mass
        a.centerx = int(a.centerx + normal[0] * depth * effect_a)
        a.centery = int(a.centery + normal[1] * depth * effect_a)

        effect_b = mass_a / total_mass
        b.centerx = int(b.centerx - normal[0] * depth * effect_b)
        b.centery = int(b.centery - normal[1] * depth * effect_b)

    # Velocity correction
    relative_v = (1 + bounce) * (dot(vel_a, normal) - dot(vel_b, normal))
    if total_mass != 0 and relative_v < 0:
        vel_a = add(vel_a, scale(normal, -relative_v * mass_a / total_mass))
        vel_b = add(vel_b, scale(normal,  relative_v * mass_b / total_mass))

    return a, b, vel_a, vel_b, True


def damping(vel, damp=0.1):
    """Slows down an object by damp factor per second."""
    fac = damp ** DELTA
    return vel[0] * fac, vel[1] * fac

#
# Main loop
# Do your stuff here!
# :D
#

# Asset dictionary for holding all your assets.
assets = {}
def init():
    """ A function for loading all your assets,
        this is since audio assets in particlular
        can at their earliest be loaded here.
    """
    assets["teapot"] = pg.image.load("teapot.png")
    assets["plong"] = pg.mixer.Sound("plong.wav")


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FRAMERATE = 60
DELTA = 1 / FRAMERATE
def main():
    """The program starts here"""
    pg.init()
    pg.display.init()
    pg.mixer.init()

    init()

    # Sets the screen resolution.
    pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    frame_clock = pg.time.Clock()

    rect_a = pg.Rect(10, 10, 100, 100)
    vel_a = (0, 0)
    rect_b = pg.Rect(250, 250, 50, 100)
    vel_b = (0, 0)

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

        if key_pressed("A") or key_pressed(pg.K_LEFT):
            assets["plong"].play()
            num_teapots += 1

        for i in range(num_teapots):
            r = 100
            a = i * 1 / 5 + time
            x = math.cos(a) * r + SCREEN_WIDTH / 2
            y = math.sin(a) * r + SCREEN_WIDTH / 2
            draw_transformed(assets["teapot"], (x, y), (0.5, 2.0), a * 180 / math.pi)

        if pg.mouse.get_pressed()[0]:
            vel_a = ((rect_a.centerx - pg.mouse.get_pos()[0]) / -DELTA,
                     (rect_a.centery - pg.mouse.get_pos()[1]) / -DELTA)
            rect_a.center = pg.mouse.get_pos()
        rect_a, rect_b, vel_a, vel_b, hit = solve_rect_overlap(rect_a, rect_b, vel_a, vel_b, bounce=1.0)

        print(vel_a, vel_b)
        vel_b = damping(vel_b, 0.1)
        rect_b.x += int(vel_b[0] * DELTA)
        rect_b.y += int(vel_b[1] * DELTA)

        if not pg.mouse.get_pressed()[0]:
            rect_a.x += int(vel_a[0] * DELTA)
            rect_a.y += int(vel_a[1] * DELTA)

        window = pg.display.get_surface()
        pg.draw.rect(window, pg.Color(255, 200, 200), rect_a)
        if hit:
            pg.draw.rect(window, pg.Color(200, 255, 255), rect_b)
        else:
            pg.draw.rect(window, pg.Color(200, 0, 255), rect_b)

        # Update the display
        pg.display.flip()
        clear_screen(pg.Color(0, 0, 0))

    pg.mixer.quit()
    pg.display.quit()
    pg.quit()

# This has to be at the bottom, because of python reasons.
if __name__ == "__main__":
    main()
