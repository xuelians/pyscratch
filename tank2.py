#!/usr/bin/python3

import screen


class TankObj():

    def __init__(self):
        self.foot = screen.create_sprite(
            'tank_foot', './pics/tank_foot.png', (300, 300))
        self.body = screen.create_sprite(
            'tank_body', './pics/tank_body.png', self.foot.pos)
        self.head = screen.create_sprite(
            'tank_head', './pics/tank_head.png', self.foot.pos)
        self.speed = 1
        self._fire_colddown = False
        pass

    def _aim(self):
        self.head.point_mouse(True)

    def go_ahead(self):
        self.foot.move(self.speed)
        self.head.move_to(self.foot.pos)
        self.body.move_to(self.foot.pos)

    def go_back(self):
        self.foot.move(-self.speed)
        self.head.move_to(self.foot.pos)
        self.body.move_to(self.foot.pos)

    def turn_left(self):
        self.foot.turn_left(2, True)
        self.body.turn_left(2, True)

    def turn_right(self):
        self.foot.turn_right(2, True)
        self.body.turn_right(2, True)

    def fire(self, btn):
        if btn:
            if not self._fire_colddown:
                obj = screen.create_sprite('bullet_XXXXXX', './pics/bullet.png', self.foot.pos)
                obj.set_auto_move(5, screen.mouse_pos)
                self._fire_colddown = True
        else:
            self._fire_colddown = False

    def update(self):
        if screen.key_pressed('up'):
            self.go_ahead()
        if screen.key_pressed('down'):
            self.go_back()
        if screen.key_pressed('left'):
            self.turn_left()
        if screen.key_pressed('right'):
            self.turn_right()
        self._aim()
        self.fire(screen.mouse_btn[0])

if __name__ == '__main__':

    # init
    screen.set_backdrop('./pics/grass.jpg')
    tank = TankObj()

    while screen.closed() == False:
        tick = screen.run()
        tank.update()
    # exit
    print("end")
