#!/usr/bin/python3

import screen


class TankObj():

    def __init__(self):
        self.foot = screen.create_sprite(
            'tank_foot', self, './pics/tank_foot.png', (300, 300))
        self.body = screen.create_sprite(
            'tank_body', self, './pics/tank_body.png', self.foot.pos)
        self.head = screen.create_sprite(
            'tank_head', self, './pics/tank_head.png', self.foot.pos)
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

    def fire(self, btn_press):
        if btn_press:
            if not self._fire_colddown or screen.now_time() - self._fire_colddown > 200:
                mdir = self.head.dir
                obj = screen.create_sprite(
                    'bullet_XXXXXX', self, './pics/bullet1.png', self.foot.pos)
                obj.set_auto_move(5, mdir)
                obj = screen.create_sprite(
                    'bullet_XXXXXX', self, './pics/bullet1.png', self.foot.pos)
                obj.set_auto_move(5, mdir - 5)
                obj = screen.create_sprite(
                    'bullet_XXXXXX', self, './pics/bullet1.png', self.foot.pos)
                obj.set_auto_move(5, mdir + 5)
                self._fire_colddown = screen.now_time()
        else:
            self._fire_colddown = 0

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


class TargetObj():
    def __init__(self):
        self._create()

    def _create(self):
        self.body = screen.create_sprite('target_XXXXXX', self, './pics/1.png', screen.random_pos())
        # self.bar = screen.draw_box(64, 12, 'red', (0, 0, 0), 0)
        # self.bar.move_to(self.body.pos_x, self.body.pos_y+38)
        self.hp = 20
        self.bar2 = screen.SpriteBar(value=20, max=20, width=64)
        self.bar2.move_to(self.body.pos_x, self.body.pos_y+38)
        self.bar2.value = self.hp

    def update(self):
        if self.hp > 0:
            bullets = screen.get_sprite_by_name('bullet_')
            collide_bullets = self.body.collide_objs(bullets)
            if collide_bullets:
                print(collide_bullets, end=',')
                for obj in collide_bullets:
                    screen.delete_sprite(obj)
                    self.hp -= 1
                print(self.hp)
                self.bar2.value = self.hp
                if self.hp <= 0:
                    screen.delete_sprite(self.body)
                    screen.delete_sprite(self.bar2)
                    self._create()


if __name__ == '__main__':

    # init
    screen.set_backdrop('./pics/grass.jpg')
    tank = TankObj()
    target = TargetObj()

    while not screen.closed:
        tick = screen.run()
        tank.update()
        target.update()

    # exit
    print("end")
