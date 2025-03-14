#!/usr/bin/env python3

import fcntl
import io
import os
import random
import re
import select
import signal
import struct
import sys
import termios
import time
import tty

WIDTH = 629
HEIGHT = 135
KEY_MAP = {
    b"\x1b[A": "up",
    b"\x1b[B": "down",
    b"\x1b[C": "right",
    b"\x1b[D": "left",
    b"\x03": "ctrl+c",
    b"\x1b": "escape",
}

old_settings = termios.tcgetattr(sys.stdin.fileno())
player: tuple[int, int]
tiles: list[list[str]]


def get_terminal_size():
    winsize = fcntl.ioctl(sys.stdin.fileno(), termios.TIOCGWINSZ, struct.pack("<HHHH", 0, 0, 0, 0))
    rows, cols, _, _ = struct.unpack("<HHHH", winsize)
    return rows, cols


def set_terminal_size(rows, cols):
    winsize = struct.pack("<HHHH", rows, cols, 0, 0)
    fcntl.ioctl(sys.stdin.fileno(), termios.TIOCSWINSZ, winsize)


def init_tiles():
    tiles = [["Nothing" for _ in range(WIDTH)] for _ in range(HEIGHT)]

    n = random.randint(3000, 5000)
    i = 0
    while i < n:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if tiles[y][x] == "Nothing":
            tiles[y][x] = "Bronze Coin"
            i += 1

    n = random.randint(1000, 3000)
    i = 0
    while i < n:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if tiles[y][x] == "Nothing":
            tiles[y][x] = "Silver Coin"
            i += 1

    n = random.randint(500, 1000)
    i = 0
    while i < n:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if tiles[y][x] == "Nothing":
            tiles[y][x] = "Gold Coin"
            i += 1

    tiles[0][0] = "${flag}"
    return tiles


def init_player():
    return (WIDTH // 2, HEIGHT // 2)


def set_non_blocking(fd):
    fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)


def set_blocking(fd):
    fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) & ~os.O_NONBLOCK)


def enter_raw_mode():
    fd = sys.stdin.fileno()
    tty.setraw(fd)


def exit_raw_mode():
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def read_key():
    rlist, _, _ = select.select([sys.stdin], [], [])
    if sys.stdin in rlist:
        return sys.stdin.buffer.read(16)
    return b""


def init():
    enter_raw_mode()
    set_non_blocking(sys.stdin.fileno())


def fini():
    set_blocking(sys.stdin.fileno())
    exit_raw_mode()


def handle_input():
    global player

    seq = read_key()
    key = KEY_MAP.get(seq, seq.decode("utf-8", "ignore"))
    if key == "q" or key == "ctrl+c" or key == "escape":
        fini()
        exit()
    elif key == "up":
        player = player[0], player[1] - 1
    elif key == "down":
        player = player[0], player[1] + 1
    elif key == "left":
        player = player[0] - 1, player[1]
    elif key == "right":
        player = player[0] + 1, player[1]
    elif match_result := re.match(r"\x1b\[8;(\d+);(\d+)t", key):
        rows, cols = match_result.groups()
        set_terminal_size(int(rows), int(cols))
    else:
        return False
    return True


def print_map():
    global player

    rows, cols = get_terminal_size()
    start_x = max(0, (WIDTH - cols) // 2)
    end_x = min(WIDTH, start_x + cols)
    start_y = max(0, (HEIGHT - rows) // 2)
    end_y = min(HEIGHT, start_y + rows - 1)

    player_x, player_y = player
    if player_x < start_x:
        player_x = end_x - 1
    if player_x >= end_x:
        player_x = start_x
    if player_y < start_y:
        player_y = end_y - 1
    if player_y >= end_y:
        player_y = start_y
    player = player_x, player_y

    buffer = io.StringIO()

    buffer.write("\x1b[2J\x1b[H")
    buffer.write(f"You found {tiles[player_y][player_x]}\r\n")
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if x == player_x and y == player_y:
                buffer.write("ඞ")
            else:
                buffer.write("_")
        if WIDTH < cols and y < end_y - 1:
            buffer.write("\r\n")

    sys.stdout.write(buffer.getvalue())


def start():
    global tiles, player

    if not sys.stdin.isatty():
        raise RuntimeError("Please run in a TTY")

    init()

    tiles = init_tiles()
    player = init_player()

    signal.signal(signal.SIGWINCH, lambda signum, frame: print_map())

    print_map()
    while True:
        if handle_input():
            print_map()


if sys.stdout.isatty():
    # open stdout in write-only mode so it will never block
    sys.stdout = open(os.ttyname(sys.stdout.fileno()), "w")
start()
