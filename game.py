from ribs import *
from dataclasses import dataclass

# Asset dictionary for holding all your assets.
assets = {}

@dataclass
class Player:
    position = [0, 0]
    size = 10

    velocity = [0, 0]

    walk_acc = 1000.0
    max_walk_speed = 100
    slow_down = 0.01


def update_player(player, delta):
    if key_down("d") or key_down(pg.K_RIGHT):
        player.velocity[0] += player.walk_acc * delta
    elif key_down("a") or key_down(pg.K_LEFT):
        player.velocity[0] -= player.walk_acc * delta
    else:
        # Yes, this is supposed to be an exponent.
        player.velocity[0] *= player.slow_down ** delta

    player.velocity[0] = max(min(player.velocity[0], player.max_walk_speed), -player.max_walk_speed)

    player.position[0] += player.velocity[0] * delta
    player.position[1] += player.velocity[1] * delta
    print(player.position)


def draw_player(player):
    window = pg.display.get_surface()
    half_width = player.size / 2
    top_left = (int(player.position[0] - half_width), int(player.position[1] - half_width))
    pg.draw.rect(window, pg.Color(100, 30, 30), (top_left, (player.size, player.size)))


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
    player.position[1] = 100

    # Main update loop
    while True:
        update_player(player, delta())

        draw_player(player)

        # Main loop ends here, put your code above this line
        yield


# This has to be at the bottom, because of python reasons.
if __name__ == "__main__":
   start_game(init, update)
