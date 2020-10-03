# LiU mJam 2020

Game made during the LiU Micro Jam 2020, a five hour game jam. The theme was
"small stuff", so I made a two player arena shooter where you can press a key to
become very small (practically invisible, but still suspectible to hits). In
order to succeed, you need to keep track of both your own position as well as
the opponent's.

## Install/run

1. Clone/download and `cd`.
2. Install dependencies.
```
$ pip3 install -r requirements.txt
```
3. Run
```
$ python3 game.py
```

## "Issues" (features!)

- When a player is killed it is printed to the console instead of on the screen.
- Customize keybinds in `game.py` (inside `update`). It's fairly
  straightforward, unless you need `shift` or some other weird key.
- No scoring or anything.
- Still unnamed.

## ribs.py

<a href="https://github.com/lithekod/snake-ribs"><img src="docs/ribs-logo.svg" alt="Snake-ribs logo" width="250"></img></a>
