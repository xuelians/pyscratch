#!/usr/bin/python3

import screen

def on_mouse_down(pos, button):
    pass


if __name__ == '__main__':

    # init
    screen.init()
    screen.add_backdrop('./pics/grass.jpg')
    screen.set_event('MouseButtonDown', on_mouse_down)
    # screen.set_event('KEYDOWN', on_key_down)

    tank = screen.create_sprite('tank')
    tank.set_costume('./pics/1.png')
    tank.move_to(300, 300)

    # main-loop
    running = True
    while not screen.is_quit():
        screen.update()
        tick = screen.run(30)

        tank = screen.get_sprite('tank')
        if tank:
            if screen.is_key_pressed('up'):
                tank.point_dir(0)
                tank.move(10)
            elif screen.is_key_pressed('down'):
                tank.point_dir(180)
                tank.move(10)
            elif screen.is_key_pressed('left'):
                tank.change_x(-10)
            elif screen.is_key_pressed('right'):
                tank.change_x(10)
            elif screen.is_key_pressed('space'):
                tank.point_mouse()
                tank.move(10)
    # exit
    print("end")