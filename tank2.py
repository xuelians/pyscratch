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
            tank.move(speed)
        if screen.key_pressed('down'):
            tank.move(-speed)
        if screen.key_pressed('left'):
            tank.turn_left(2, rotate=True)
        if screen.key_pressed('right'):
            tank.turn_right(2, rotate=True)
        if screen.key_pressed('space'):
            tank.point_mouse(rotate=True)
            tank.move(speed)
        elif screen.key_pressed('w'):
            tank.move(speed)
        # else:
        #     tank.move_to(screen.mouse_pos)
        mobjs = screen.get_sprite_under_mouse()
        if len(mobjs):
            print(mobjs)
        
        if tank.out_of_screen():
            print('out of screen, %s' % str(tank.pos))
    # exit
    print("end")