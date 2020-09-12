from ribs import *

# Asset dictionary for holding all your assets.
assets = {}

def init():
    """ A function for loading all your assets.
        (Audio assets can at their earliest be loaded here.)
    """
    # Load images here
    assets["teapot"] = pg.image.load("teapot.png")
    assets["plong"] = pg.mixer.Sound("plong.wav")


def update():
    """The program starts here"""
    # Initialization (only runs on start/restart)
    ...

    # Main update loop
    while True:
        ...

        # Main loop ends here, put your code above this line
        yield


# This has to be at the bottom, because of python reasons.
if __name__ == "__main__":
   start_game(init, update)
