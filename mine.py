#!/usr/bin/python3

import screen
import math
import random


def get_block_mine(x, y):
    b = screen.get_sprite('block_%d_%d' % (x, y))
    if b is not None and b.mine == True:
        return 1
    return 0


def flag_block(x, y):
    b = screen.get_sprite('block_%d_%d' % (x, y))
    if b is not None and b.open == False:
        if b.flag == True:
            b.flag = False
            b.switch_costume(11)
        else:
            b.flag = True
            b.switch_costume(10)


def open_block(x, y):
    b = screen.get_sprite('block_%d_%d' % (x, y))
    if b is not None and b.open == False:
        b.open = True
        print('open %d,%d' % (x, y))
        if b.mine == True:
            b.switch_costume(9)
        else:
            n = get_block_mine(x - 1, y - 1)
            n += get_block_mine(x, y - 1)
            n += get_block_mine(x + 1, y - 1)
            n += get_block_mine(x - 1, y)
            n += get_block_mine(x + 1, y)
            n += get_block_mine(x - 1, y + 1)
            n += get_block_mine(x, y + 1)
            n += get_block_mine(x + 1, y + 1)
            b.switch_costume(n)
            if n == 0:
                open_block(x - 1, y - 1)
                open_block(x, y - 1)
                open_block(x + 1, y - 1)
                open_block(x - 1, y)
                open_block(x + 1, y)
                open_block(x - 1, y + 1)
                open_block(x, y + 1)
                open_block(x + 1, y + 1)
    pass


def is_game_over():
    for key, b in screen.all_sprite().items():
        if not key.startswith('block_'):
            continue
        if b.mine == True and b.open == True:
            return True
    return False


def is_game_win():
    n = 0
    for key, b in screen.all_sprite().items():
        if not key.startswith('block_'):
            continue
        if b.mine == False and b.open == False:
            n += 1
    if n == 0:
        return True
    else:
        return False


def show_mine():
    n = 0
    for key, b in screen.all_sprite().items():
        if not key.startswith('block_'):
            continue
        if b.mine == True:
            b.switch_costume(12)


def on_mouse_down(pos, button):
    print('pos=%s, button=%d' % (pos, button))
    if is_game_over():
        print('YOU LOST')
        return
    if is_game_win():
        print('YOU WIN')
        return
    x = pos[0] // 64
    y = pos[1] // 64
    if button == 1:
        open_block(x, y)
    if button == 3:
        flag_block(x, y)
    if is_game_win():
        show_mine()
        print('YOU WIN')


def on_key_down(key, mod, unicode):
    print('key=%s, mod=%d' % (key, mod))
    # for key, b in blocks.items():
    #     b.surf.hide()
    # blocks = create_blocks(6, 10)
    pass


def create_random(range_max):
    a = random.random()
    b = int(a * range_max)
    return b


def put_mines(row, column, num):
    while num > 0:
        x = create_random(column)
        y = create_random(row)
        b = screen.get_sprite('block_%d_%d' % (x, y))
        if b and b.mine == False:
            b.mine = True
            num -= 1


def create_blocks(row, column):
    """create blocks"""
    image_files = [
        './pics/0.png', './pics/1.png', './pics/2.png',
        './pics/3.png', './pics/4.png', './pics/5.png',
        './pics/6.png', './pics/7.png', './pics/8.png',
        './pics/mine2.png', './pics/flag.png',
        './pics/unknown.png',  # 11
        './pics/mine.png'  # 12
    ]
    # create blocks
    for y in range(0, row):
        for x in range(0, column):
            b = screen.create_sprite('block_%d_%d' % (x, y))
            b.add_costume(image_files)
            b.switch_costume(11)
            b.move_to(x * 64+32, y * 64+32)
            # add user-define variables
            b.mine = False
            b.open = False
            b.flag = False
    # put mine
    put_mines(row, column, 6)


def main():

    screen.init()
    screen.set_event('MouseButtonDown', on_mouse_down)
    screen.set_event('KeyDown', on_key_down)

    create_blocks(6, 10)

    while screen.is_quit() == False:
        screen.run()
        screen.update()

    # exit
    print("end")


if __name__ == '__main__':
    main()
