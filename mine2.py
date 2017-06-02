
import screen

ROW = 20
COL = 20
SIZE = 32


class BlockObj():
    def __init__(self, x, y):
        name = 'block_%d_%d' % (x, y)
        images = [
            './pics/0.png', './pics/1.png', './pics/2.png',
            './pics/3.png', './pics/4.png', './pics/5.png',
            './pics/6.png', './pics/7.png', './pics/8.png',
            './pics/mine2.png', './pics/flag.png',
            './pics/unknown.png',  # 11
            './pics/mine.png',  # 12
            './pics/mine3.png'  # 13
        ]
        self.body = screen.create_sprite(name, self, images)
        self.body.switch_costume(11)
        self.body.set_size(SIZE / 64 * 100)
        self.body.move_to(x * SIZE + SIZE / 2, y * SIZE + SIZE / 2)
        self.x = x
        self.y = y
        self.mine = False
        self.opened = False
        self.flaged = False

    # class method function
    def open(self):
        if not self.opened and not self.flaged:
            self.opened = True
            print('open', self.x, self.y)
            if self.mine == True:
                self.body.switch_costume(9)
            else:
                blocks = self._get_round()
                n = 0
                for b in blocks:
                    if b.mine:
                        n += 1
                self.body.switch_costume(n)
                if n == 0:
                    for b in blocks:
                        b.open()
        pass

    def flag(self):
        if self.flaged == False:
            self.body.switch_costume(10)
            self.flaged = True
        else:
            self.body.switch_costume(11)
            self.flaged = False

    def _get_round(self):
        blocks = []
        for x in [self.x - 1, self.x, self.x + 1]:
            for y in [self.y - 1, self.y, self.y + 1]:
                b = screen.get_sprite_owner('block_%d_%d' % (x, y))
                if b is not None:
                    blocks.append(b)
        return blocks


def put_mines(row, column, num):
    while num > 0:
        x = screen.random_num(0, column)
        y = screen.random_num(0, row)
        b = screen.get_sprite_owner('block_%d_%d' % (x, y))
        if b and b.mine != True:
            b.mine = True
            num -= 1


def create_blocks(row, column):
    x_range = range(0, column)
    y_range = range(0, row)
    # create blocks
    for y in y_range:
        for x in x_range:
            BlockObj(x, y)
    # put mine
    put_mines(row, column, ROW * COL / 10)


def game_is_win():
    not_opened = 0
    for y in range(0, ROW):
        for x in range(0, COL):
            b = screen.get_sprite_owner('block_%d_%d' % (x, y))
            if not b.mine and not b.opened:
                not_opened += 1
    return not_opened == 0


def game_is_lost():
    mine_opened = 0
    for y in range(0, ROW):
        for x in range(0, COL):
            b = screen.get_sprite_owner('block_%d_%d' % (x, y))
            if b.mine and b.opened:
                mine_opened += 1
    return mine_opened > 0


def game_over(msg):
    for y in range(0, ROW):
        for x in range(0, COL):
            b = screen.get_sprite_owner('block_%d_%d' % (x, y))
            if not b.mine:
                b.open()
            elif not b.opened:
                if b.flaged:
                    b.body.switch_costume(13)
                else:
                    b.body.switch_costume(12)
            else:
                pass  # ignore opened block
    print(msg)
    screen.set_event(6, None)


def on_mouse_down(pos, button):
    if screen.mouse_down():
        x = screen.mouse_x // SIZE
        y = screen.mouse_y // SIZE
        b = screen.get_sprite_owner('block_%d_%d' % (x, y))
        if b is not None:
            if screen.mouse_down('left'):
                b.open()
            if screen.mouse_down('right'):
                b.flag()
        if game_is_win():
            game_over('WIN')
        if game_is_lost():
            game_over('LOST')


def main():
    screen.set_size(640, 640)
    screen.set_event(6, on_mouse_down)
    screen.status_bar = False

    create_blocks(ROW, COL)

    while not screen.closed:
        screen.run()


if __name__ == '__main__':
    main()
