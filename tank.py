#!/usr/bin/python3

import screen

def on_mouse_down(pos, button):
    pass


if __name__ == '__main__':

    # init
    screen.set_backdrop('./pics/grass.jpg')
    screen.set_event('MouseButtonDown', on_mouse_down)
    # screen.set_event('KEYDOWN', on_key_down)

    tank = screen.create_sprite('tank')
    tank.set_costume('./pics/tank12.png')
    tank.move_to(300, 300)

    # main-loop
    speed = 2
    while screen.closed() == False:
        tick = screen.run()
        if screen.key_pressed('up'):
            tank.set_dir(0, rotate=True)
            tank.move(speed)
        elif screen.key_pressed('down'):
            tank.set_dir(180, rotate=True)
            tank.move(speed)
        elif screen.key_pressed('left'):
            tank.set_dir(270, rotate=True)
            tank.change_x(-speed)
        elif screen.key_pressed('right'):
            tank.set_dir(90, rotate=True)
            tank.change_x(speed)
        elif screen.key_pressed('space'):
            tank.point_mouse(rotate=True)
            tank.move(speed)
        elif screen.key_pressed('w'):
            tank.move(speed)
        # else:
        #     tank.move_to(screen.mouse_pos)
        mobjs = screen.get_sprite_under_mouse()
        if len(mobjs):
            print(mobjs)
    # exit
    print("end")