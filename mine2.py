
import screen


class BlockObj():
    def __init__(self, x, y):
        name = 'block_%d_%d' % (x, y)
        posx = x * 64 + 32
        posy = y * 64 + 32
        images = [
            './pics/0.png', './pics/1.png', './pics/2.png',
            './pics/3.png', './pics/4.png', './pics/5.png',
            './pics/6.png', './pics/7.png', './pics/8.png',
            './pics/mine2.png', './pics/flag.png',
            './pics/unknown.png',  # 11
            './pics/mine.png',  # 12
            './pics/mine3.png'  # 13
        ]
        self.body = screen.create_sprite(name, self, images, posx, posy)
        self.body.switch_costume(11)
        self.mine = False
        self.x = x
        self.y = y
        self.opened = False
        self.flaged = False

    # class method function
    def flag(self):
        if self.opened:
            return
        if not self.flaged:
            self.body.switch_costume(10)
            self.flaged = True
        else:
            self.body.switch_costume(11)
            self.flaged = False

    def open(self):
        if self.opened == True or self.flaged:
            return
        self.opened = True
        print('open', self.body.name)
        if self.mine == True:
            self.body.switch_costume(9)
        else:
            blocks = self.find_neighbor()
            n = 0
            for b in blocks:
                if b.mine == True:
                    n += 1
            self.body.switch_costume(n)
            if n == 0:
                for b in blocks:
                    b.open()
        pass

    def find_neighbor(self):
        blocks = []
        b = screen.get_sprite_owner('block_%d_%d' % (self.x - 1, self.y - 1))
        if b is not None:
            blocks.append(b)
        b = screen.get_sprite_owner('block_%d_%d' % (self.x, self.y - 1))
        if b is not None:
            blocks.append(b)
        b = screen.get_sprite_owner('block_%d_%d' % (self.x + 1, self.y - 1))
        if b is not None:
            blocks.append(b)
        b = screen.get_sprite_owner('block_%d_%d' % (self.x - 1, self.y))
        if b is not None:
            blocks.append(b)
        b = screen.get_sprite_owner('block_%d_%d' % (self.x + 1, self.y))
        if b is not None:
            blocks.append(b)
        b = screen.get_sprite_owner('block_%d_%d' % (self.x - 1, self.y + 1))
        if b is not None:
            blocks.append(b)
        b = screen.get_sprite_owner('block_%d_%d' % (self.x, self.y + 1))
        if b is not None:
            blocks.append(b)
        b = screen.get_sprite_owner('block_%d_%d' % (self.x + 1, self.y + 1))
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
    put_mines(row, column, 10)


def game_is_win(row, column):
    x_range = range(0, column)
    y_range = range(0, row)
    for y in y_range:
        for x in x_range:
            b = screen.get_sprite_owner('block_%d_%d' % (x, y))
            if not b.mine and not b.opened:
                return False
    return True

def game_is_lost(row, column):
    x_range = range(0, column)
    y_range = range(0, row)
    for y in y_range:
        for x in x_range:
            b = screen.get_sprite_owner('block_%d_%d' % (x, y))
            if b.mine and b.opened:
                return True
    return False


def game_over(row, column):
    x_range = range(0, column)
    y_range = range(0, row)
    for y in y_range:
        for x in x_range:
            b = screen.get_sprite_owner('block_%d_%d' % (x, y))
            if not b.opened:
                if b.mine:
                    if b.flaged:
                        b.body.switch_costume(13)
                    else:
                        b.body.switch_costume(12)
                else:
                    b.open()

def on_mouse_down(pos, button):
    print(pos, button)
    x = screen.mouse_x // 64
    y = screen.mouse_y // 64
    b = screen.get_sprite_owner('block_%d_%d' % (x, y))
    if b is not None:
        if screen.mouse_down('left'):
            b.open()
        if screen.mouse_down('right'):
            b.flag()
    # check if win
    if game_is_win(10, 10):
        print('WIN')
        game_over(10, 10)
        screen.set_event(6, None)
    if game_is_lost(10, 10):
        print('LOST')
        game_over(10, 10)
        screen.set_event(6, None)


def main():
    screen.set_size(640, 640)
    screen.set_event(6, on_mouse_down)
    create_blocks(10, 10)

    while not screen.closed:
        screen.run()
        # on_mouse_down()


if __name__ == '__main__':
    main()
