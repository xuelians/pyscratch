
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
            './pics/mine.png'  # 12
        ]
        self.body = screen.create_sprite(name, self, images, posx, posy)
        self.body.switch_costume(11)
        self.mine = False

    # class method function
    def open(self):
        if self.mine == True:
            self.body.switch_costume(9)
        else:
            self.body.switch_costume(0)
        pass


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


def on_mouse_down():
    if screen.mouse_btn[0]:
        x = screen.mouse_pos[0] // 64
        y = screen.mouse_pos[1] // 64
        b = screen.get_sprite_owner('block_%d_%d' % (x, y))
        if b is not None:
            b.open()


def main():
    screen.set_size(640, 640)
    create_blocks(10, 10)

    while not screen.closed:
        screen.run()
        on_mouse_down()

if __name__ == '__main__':
    main()
