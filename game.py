from ribs import *
from dataclasses import dataclass

# Asset dictionary for holding all your assets.
assets = {}

@dataclass
class Player:
    rect = pg.Rect(0, 0, 10, 10)

    velocity = (0, 0)

    walk_acc = 1000.0
    max_walk_speed = 100
    slow_down = 0.01


def update_player(player, delta):
    if key_down("d") or key_down(pg.K_RIGHT):
        player.velocity = player.velocity[0] + player.walk_acc * delta, player.velocity[1]
    elif key_down("a") or key_down(pg.K_LEFT):
        player.velocity = player.velocity[0] - player.walk_acc * delta, player.velocity[1]
    else:
        # Yes, this is supposed to be an exponent.
        player.velocity = player.velocity[0] * (player.slow_down ** delta), player.velocity[1]

    player.velocity = (player.velocity[0], player.velocity[1] + 9.82 * delta)
    print(player.velocity)

    max_speed = player.max_walk_speed
    clamped_horizontal_speed = max(min(player.velocity[0], max_speed), -max_speed)
    player.velocity = (clamped_horizontal_speed, player.velocity[1])

    player.rect.x += player.velocity[0] * delta
    player.rect.y += player.velocity[1] * delta


def draw_player(player):
    window = pg.display.get_surface()
    pg.draw.rect(window, pg.Color(100, 30, 30), player.rect)

levels = [
"""
##########
#        #
#        #
#        #
# S    E #
##########
""",
"""
##########
#        #
# S      #
####     #
####   E #
##########
""",
]

def parse_level(level_string):
    grid_size = 20

    walls = []
    goals = []
    start = None

    level_lines = level_string.strip().split("\n")
    for tile_y, line in enumerate(level_lines):
        y = tile_y * grid_size
        for tile_x, c in enumerate(line):
            x = tile_x * grid_size
            r = pg.Rect(x, y, grid_size, grid_size)
            if c == "#":
                # It's a wall
                walls.append(r)
            elif c == "E":
                # It's a goal
                goals.append(r)
            elif c == "S":
                # It's the start
                start = (x, y)
                print(start)

    return walls, goals, start


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
    player = Player()

    walls, goals, start = parse_level(levels[1])
    player.rect.x = start[0]
    player.rect.y = start[1]

    # Main update loop
    while True:
        update_player(player, delta())
        draw_player(player)

        for wall in walls:
            window = pg.display.get_surface()
            pg.draw.rect(window, pg.Color(100, 100, 100), wall)

            solution = solve_rect_overlap(player.rect, wall, player.velocity, mass_b=0)
            player.velocity = solution[2]

        for goal in goals:
            window = pg.display.get_surface()
            pg.draw.rect(window, pg.Color(20, 100, 20), goal)

            _, depth = overlap_data(player.rect, goal)
            if depth > 0:
                print("GOAL!")


        # Main loop ends here, put your code above this line
        yield


# This has to be at the bottom, because of python reasons.
if __name__ == "__main__":
   start_game(init, update)
