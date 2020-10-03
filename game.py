import sys
import math

from ribs import *
from dataclasses import dataclass

# Asset dictionary for holding all your assets.
assets = {}
shots = []

def vec_len(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)

def clamp(val, low, high):
    return min(max(val, low), high)

@dataclass
class Shot:
    centerx = 0
    centery = 0
    size = 10
    width = height = size
    
    velocity = (0, 0)
    shooter_idx = 0

def update_shot(shot, delta):
    shot.centerx += shot.velocity[0] * delta
    shot.centery += shot.velocity[1] * delta
    return True

def draw_shot(shot):
    window = pg.display.get_surface()
    pg.draw.rect(window, pg.Color(30, 30, 100), (shot.centerx - shot.size / 2,
                                                 shot.centery - shot.size / 2,
                                                 shot.size,
                                                 shot.size))

@dataclass
class Player:
    centerx = 0
    centery = 0
    min_size = 1
    max_size = 20
    size = max_size
    width = height = size
    gesmol_speeed = 0.5
    small = False
    shot_timeout = 0
    idx = 0

    velocity = (0, 0)

    walk_acc = 1000.0
    max_speed = 250
    slow_down = 4
    shot_speed = 150
    shot_delay_start = 1/5

    key_up = None
    key_down = None
    key_left = None
    key_right = None
    key_shoot = None
    key_small = None

def update_player(player, delta):
    dx, dy = (0, 0)
    if key_down(player.key_left):
        dx -= 1
    if key_down(player.key_right):
        dx += 1
    if key_down(player.key_up):
        dy -= 1
    if key_down(player.key_down):
        dy += 1

    player.velocity = (player.velocity[0] + (dx * player.walk_acc * delta),
                       player.velocity[1] + (dy * player.walk_acc * delta))

    # ** delta ?
    player.velocity = (player.velocity[0] + player.velocity[0] * -player.slow_down * delta,
                       player.velocity[1] + player.velocity[1] * -player.slow_down * delta)

    if (speed := vec_len(player.velocity)) > player.max_speed:
        player.velocity = ((player.velocity[0] * (player.max_speed / speed)),
                           (player.velocity[1] * (player.max_speed / speed)))

    player.centerx += player.velocity[0] * delta
    player.centery += player.velocity[1] * delta

    if key_pressed(player.key_small):
        player.small = not player.small

    if player.shot_timeout > 0:
        player.shot_timeout -= delta
        if player.shot_timeout < 0:
            player.shot_timeout = 0

    if key_down(player.key_shoot) and player.shot_timeout == 0:
        # shoot
        player_speed = vec_len(player.velocity)
        if player_speed != 0:
            shot = Shot()
            shot.centerx = player.centerx
            shot.centery = player.centery
            shot.shooter_idx = player.idx
            shot.velocity = (player.velocity[0] * (player.shot_speed / player_speed),
                             player.velocity[1] * (player.shot_speed / player_speed))
            shots.append(shot)
            player.shot_timeout = player.shot_delay_start

    if player.small and player.size > player.min_size:
        player.size -= player.gesmol_speeed
    elif not player.small and player.size < player.max_size:
        player.size += player.gesmol_speeed
    player.width = player.height = player.size

def draw_player(player):
    window = pg.display.get_surface()
    pg.draw.rect(window, pg.Color(100, 30, 30), (player.centerx - player.size / 2,
                                                 player.centery - player.size / 2,
                                                 player.size,
                                                 player.size))

# square
LEVEL = \
"""
##########
#        #
#        #
#        #
# S    S #
#        #
#        #
#        #
#        #
##########
"""

def parse_level(level_string):
    GRID_SIZE = 40

    walls = []
    starts = []

    level_lines = level_string.strip().split("\n")
    for tile_y, line in enumerate(level_lines):
        y = tile_y * GRID_SIZE
        for tile_x, c in enumerate(line):
            x = tile_x * GRID_SIZE
            r = pg.Rect(x, y, GRID_SIZE, GRID_SIZE)
            if c == "#":
                # It's a wall
                walls.append(r)
            elif c == "S":
                # It's the start
                starts.append((x, y))

    return walls, starts


def init():
    """ A function for loading all your assets.
        (Audio assets can at their earliest be loaded here.)
    """
    # Load images here
    assets["teapot"] = pg.image.load("teapot.png")

    # Load sounds here
    assets["plong"] = pg.mixer.Sound("plong.wav")


def update():
    """The program starts here"""
    # Initialization (only runs on start/restart)
    player1 = Player()
    player2 = Player()

    walls, start = parse_level(LEVEL)

    player1.idx = 1
    player1.key_up = "w"
    player1.key_down = "s"
    player1.key_left = "a"
    player1.key_right = "d"
    player1.key_small = "f"
    player1.key_shoot = "c"

    player2.idx = 2
    player2.key_up = "i"
    player2.key_down = "k"
    player2.key_left = "j"
    player2.key_right = "l"
    player2.key_small = "h"
    player2.key_shoot = "n"

    reset_players = True
    # Main update loop
    while True:
        if reset_players:
            reset_players = False
            player1.centerx = start[0][0]
            player1.centery = start[0][1]
            player2.centerx = start[1][0]
            player2.centery = start[1][1]
            shots.clear()

        update_player(player1, delta())
        update_player(player2, delta())

        to_remove = []
        for shot in shots:
            if not update_shot(shot, delta()):
                to_remove.append(shot)
        for shot in to_remove:
            shots.remove(shot)

        draw_player(player1)
        draw_player(player2)
        for shot in shots:
            draw_shot(shot)

        for shot in shots:
            for other in shots:
                if shot.shooter_idx != other.shooter_idx:
                    _, depth = overlap_data(shot, other)
                    if depth > 0:
                        to_remove.append(shot)
            for player in (player1, player2):
                _, depth = overlap_data(player, shot)
                if depth > 0 and player.idx != shot.shooter_idx:
                    print(f"{player.idx} ded by {shot.shooter_idx}")
                    reset_players = True
        for shot in to_remove:
            shots.remove(shot)

        for wall in walls:
            window = pg.display.get_surface()
            pg.draw.rect(window, pg.Color(100, 100, 100), wall)
            for player in (player1, player2):
                player.velocity, wall_vel, overlap = solve_rect_overlap(player,
                                                                        wall,
                                                                        player.velocity,
                                                                        mass_b=0,
                                                                        bounce=0.1)

        # Main loop ends here, put your code above this line
        yield


# This has to be at the bottom, because of python reasons.
if __name__ == "__main__":
   start_game(init, update)
