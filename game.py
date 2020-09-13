from ribs import *

# Asset dictionary for holding all your assets.
assets = {}
def init():
    """ A function for loading all your assets,
        this is since audio assets in particlular
        can at their earliest be loaded here.
    """
    assets["teapot"] = pg.image.load("teapot.png")
    assets["plong"] = pg.mixer.Sound("plong.wav")


def update():
    """The program starts here"""
    num_teapots = 1

    # Initialization (only runs on start/restart)
    rect_a = pg.Rect(200, 200, 100, 100)
    vel_a = (0, 1000)
    rect_b = pg.Rect(250, 250, 50, 100)
    vel_b = (0, 0)

    # Main update loop
    while True:
        if key_pressed("A") or key_pressed(pg.K_LEFT):
            assets["plong"].play()
            num_teapots += 1
            restart()

        for i in range(num_teapots):
            r = 100
            a = i * 1 / 5 + time()
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

        # Main loop ends here, put your code above this line
        yield


# This has to be at the bottom, because of python reasons.
if __name__ == "__main__":
   start_game(init, update)
