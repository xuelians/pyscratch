#!/usr/bin/python3

import pygame
import sys
from pygame.locals import *
from pygame.math import Vector2 as Vec2d


class SpriteObj():
    """Sprite Object"""
    oid_cnt = 0
    obj_dict = {}
    image_cache = {} # save loaded image surface

    def __init__(self, name=''):
        # base
        SpriteObj.check_name(name)
        self._oid = SpriteObj.gen_oid()
        self._name = name if name else 'SpriteObj_%d' % self._oid
        # self._screen = sys.modules[__name__]
        # for display
        self._surf = None
        self._costume = []
        self._costume_used = 0
        # for motion
        self.vdir = Vec2d(0, -1)  # point up
        self.vpos = Vec2d(0, 0)  # position
        # init actions
        SpriteObj.append_obj(self)

    @classmethod
    def check_name(cls, name):
        if name in cls.obj_dict:
            raise RuntimeError(
                'name [%s] has been used for another SpriteObj' % name)

    @classmethod
    def gen_oid(cls):
        cls.oid_cnt += 1
        return cls.oid_cnt

    @classmethod
    def append_obj(cls, obj):
        if obj is None:
            raise RuntimeError('Expect SpriteObj but None')
        if obj.name in cls.obj_dict:
            raise RuntimeError(
                'name [%s] has been used for another SpriteObj' % obj.name)
        cls.obj_dict[obj.name] = obj

    @classmethod
    def delete_obj(cls, name_or_obj):
        if isinstance(name_or_obj, cls):
            del cls.obj_dict[name_or_obj.name]
        else:
            del cls.obj_dict[name_or_obj]

    @classmethod
    def update_all(cls):
        for obj in cls.obj_dict.values():
            obj._update()

    @classmethod
    def load_image(cls, image_file, alpha=False):
        if image_file not in cls.image_cache:
            if image_file.endswith('.png') or alpha:
                surf = pygame.image.load(image_file).convert_alpha()
            else:
                surf = pygame.image.load(image_file).convert()
            if surf:
                cls.image_cache[image_file] = surf
            else:
                raise IOError('fail to load image %s' % image_file)
        return cls.image_cache[image_file]

    @property
    def name(self):
        """return sprite object name (string)"""
        return self._name

    @property
    def oid(self):
        """return sprite object id (int)"""
        return self._oid

    @property
    def surf(self):
        """sprite display surface (refer to pygame.surface)"""
        return self._surf

    def _update(self):
        """update the sprite on screen with new custome and new position"""
        if self._surf is not None:
            rect = self._surf.get_rect()
            rect.center = (self.vpos[0], self.vpos[1])
            scr = pygame.display.get_surface()
            scr.blit(self._surf, rect)

    def show(self):
        """
        Makes sprite appear on the Stage
        """
        self._screen.show_sprite(self)

    def hide(self):
        """
        Make a hide-and-seek game with characters that appear and disappear.
        """
        self._screen.hide_sprite(self)

    # Motions Methods
    def turn_left(self, angle):
        """
        Turn a angle to the left on current moving direction
        """
        self.vdir = self.vdir.rotate(-angle)

    def turn_right(self, angle):
        """Turn a right to the right on current moving direction"""
        self.vdir = self.vdir.rotate(angle)

    def point_dir(self, angle):
        """
        Set the angle as current moving direction
        - angle: 0~360, 0 for up, 90 for right, 180 for down, 270 for left
        """
        self.vdir = Vec2d(0, -1).rotate(angle)

    def point_mouse(self):
        """Set current moving direction to mouse postion"""
        mdir = Vec2d(pygame.mouse.get_pos()) - self.vpos
        if mdir != (0, 0):
            self.vdir = mdir.normalize()

    def move(self, steps):
        """move steps on current moving direction"""
        self.vpos += self.vdir * steps

    def move_to(self, center_x, center_y):
        """
        set sprite center to given position (pixel x & y) with sprite left-top
        """
        self.vpos = Vec2d(center_x, center_y)

    def change_x(self, amount):
        """Change the x position by this amount"""
        self.vpos[0] += amount

    def change_y(self, amount):
        """Change the y position by this amount"""
        self.vpos[1] += amount

    def set_x(self, amount):
        """Set the x position of a sprite"""
        self.vpos[0] = amount

    def set_y(self, amount):
        """Change the y position by this amount"""
        self.vpos[1] = amount

    # Looks Methods
    def __add_costume(self, image_surf, index=None):
        num = len(self._costume)
        if index:
            self._costume.insert(index, image_surf)
            if 0 <= index <= num:
                return index
            elif num < index:
                return num
            elif -num <= index < 0:
                return num - index
            else:
                return 0
        else:
            self._costume.append(image_surf)
            return num

    def add_costume(self, image_file, index=None):
        flist = image_file if isinstance(image_file, list) else [image_file]
        pos_list = []
        for each in flist:
            surf = SpriteObj.load_image(each)
            pos = self.__add_costume(surf, index)
            pos_list.append(pos)
            if index is not None:
                index += 1
        return pos_list[0]

    def set_costume(self, image_file, index=None):
        index = self.add_costume(image_file, index)
        self.switch_costume(index)

    def del_costume(self, index=None):
        if index:
            return self._costume.pop(index)
        else:
            return self._costume.pop()

    def switch_costume(self, index):
        """
        Switch costumes to change the look of a sprite
        """
        try:
            self._surf = self._costume[index]
            self._costume_used = index
        except IndexError as err:
            pass

    def next_costume(self):
        """
        Switches to the next costume in the sprite's costume list
        """
        self._costume_used += 1
        if self._costume_used >= len(self._costume):
            self._costume_used = 0  # back to first costume
        try:
            self._surf = self._costume[self._costume_used]
        except IndexError as err:
            pass


def set_event(name_or_id, func=None):
    """
    register event callback funtion with args. clean callback by set func is None.<br>
    - 1: ActiveEvent, func(gain, state)
    - 2: KeyDown, func(key, mod, unicode)
    - 3: KeyUp, func(key, mod)
    - 4: MouseMotion, func(pos, rel, buttons)
    - 5: MouseButtonUp, func(pos, button)
    - 6: MouseButtonDown, func(pos, button)
    - 7: JoyAxisMotion, func(joy, axis, value)
    - 8: JoyBallMotion, func(joy, ball, rel)
    - 9: JoyHatMotion, func(joy, hat, value)
    - 10: JoyButtonUp, func(joy, button)
    - 11: JoyButtonDown, func(joy, button)
    - 12: Quit, func(args)
    - 16: VideoResize, func(size, w, h)
    - 17: VideoExpose, func(args)
    - 24~31: UserEvent, func(code)
    """
    helpmsg = ''
    for eid, name in this.__event_dict.items():
        helpmsg += '\n\t%2d: %s' % (eid, name)
    name = this.__event_dict.get(name_or_id, None) if isinstance(
        name_or_id, int) else name_or_id
    if name not in this.__event_cb:
        raise ValueError('invalid event [%s], please use below id or name:%s' %
                         (name_or_id, helpmsg))
    this.__event_cb[name] = func


def closed():
    """return True if screen closed (right-top close button clicked)"""
    return this.__screen_closed


def draw_image(image_file, pos_x, pos_y):
    """
    load a image file and set position (left-top)
    """
    obj = SpriteObj()
    obj.add_costume(image_file)
    obj.move_to(pos_x, pos_y)
    return obj


def sleep(milliseconds):
    """entry sleep mode for milliseconds, return integer as actual sleep ticks"""
    return this.__clock.tick(milliseconds)


def __convert_pressed_keys():
    """convert pressed key list to name list"""
    name = []
    press = pygame.key.get_pressed()
    for i in range(0, len(press)):
        if press[i] == 1:
            name.append(pygame.key.name(i))
    return name


def __update_key_mouse():
    """save key and mouse to global"""
    this.key_press = __convert_pressed_keys()
    this.mouse_pos = pygame.mouse.get_pos()
    this.mouse_rel = pygame.mouse.get_rel()
    this.mouse_btn = pygame.mouse.get_pressed()


def __call_user_cb(event):
    event_name = pygame.event.event_name(event.type)
    func = this.__event_cb.get(event_name, None)
    if func:
        if event_name == 'Quit':
            func()
        elif event_name == 'ActiveEvent':
            func(event.gain, event.state)
        elif event_name == 'KeyDown':
            func(event.key, event.mod, event.unicode)
        elif event_name == 'KeyUp':
            func(event.key, event.mod)
        elif event_name == 'MouseMotion':
            func(event.pos, event.rel, event.buttons)
        elif event_name == 'MouseButtonUp':
            func(event.pos, event.button)
        elif event_name == 'MouseButtonDown':
            func(event.pos, event.button)
        elif event_name == 'JoyAxisMotion':
            func(event.joy, event.axis, event.value)
        elif event_name == 'JoyBallMotion':
            func(event.joy, event.ball, event.rel)
        elif event_name == 'JoyHatMotion':
            func(event.joy, event.hat, event.value)
        elif event_name == 'JoyButtonUp':
            func(event.joy, event.button)
        elif event_name == 'JoyButtonDown':
            func(event.joy, event.button)
        elif event_name == 'VideoResize':
            func(event.size, event.w, event.h)
        elif event_name == 'VideoExpose':
            func()
        elif event_name.startswith('UserEvent'):
            func(event.code)
        else:
            raise ValueError('unknown event name [%s]' % event_name)


def run(wait_tick=50):
    """waiting event from screen"""
    __update_key_mouse()
    # event handle
    for event in pygame.event.get():
        if event.type == 12:  # 'Quit'
            this.__screen_closed = True
        # invoke callback
        __call_user_cb(event)
    return sleep(wait_tick)


def update():
    """refresh display"""
    # update background
    if this.__backdrop.surf:
        backdrop_heigth = this.__backdrop.surf.get_height()
        backdrop_width = this.__backdrop.surf.get_width()
        screen_width, screen_height = this.__screen_size
        for y in range(0, screen_height, backdrop_heigth):
            for x in range(0, screen_width, backdrop_width):
                this.__screen.blit(this.__backdrop.surf, (x, y))

    # update sprite
    SpriteObj.update_all()

    # update status bar
    status_text = "x=%d y=%d key=%s" % (
        *this.mouse_pos, '+'.join(this.key_press))
    screen_width, screen_height = this.__screen_size
    font_height = this.__font_obj.get_linesize()
    font_color = (255, 200, 0)  # orange
    font_bgcolor = (0, 0, 0)  # black
    # clean old text
    font_surf = pygame.Surface((screen_width, font_height))
    font_rect = font_surf.fill(font_bgcolor).move(
        0, screen_height - font_height)
    this.__screen.blit(font_surf, font_rect)
    # print(status_text)
    font_surf = this.__font_obj.render(
        status_text, True, font_color, font_bgcolor)
    font_rect = font_surf.get_rect().move(0, screen_height - font_height)
    this.__screen.blit(font_surf, font_rect)

    # final refresh
    pygame.display.update()


def show_sprite(obj):
    """
    Makes sprite appear on the Stage
    """
    if not isinstance(obj, SpriteObj):
        raise TypeError('only SpriteObj object can be shown')
    # # global this.__display_objs
    if obj.oid not in this.__display_objs:
        this.__display_objs[obj.oid] = obj


def hide_sprite(obj):
    """
    Make a hide-and-seek game with characters that appear and disappear.
    """
    if not isinstance(obj, SpriteObj):
        raise TypeError('only SpriteObj object can be hidden')
    # # global this.__display_objs
    if obj.oid in this.__display_objs:
        del this.__display_objs[obj.oid]


def set_backdrop(image_file, index=None):
    """
    add a image into backdrop list, and set it as current backdrop
    """
    index = this.__backdrop.add_costume(image_file, index)
    this.__backdrop.switch_costume(index)


def add_backdrop(image_file, index=None):
    """
    add a image into backdrop list
    """
    this.__backdrop.add_costume(image_file, index)


def del_backdrop(index=None):
    """
    remove a image into backdrop list
    """
    return this.__backdrop.del_costume(index)


def switch_backdrop(index):
    """
    Switch backdrops to change the look of a sprite
    """
    this.__backdrop.switch_costume(index)


def next_backdrop():
    """
    Switches to the next backdrop in the sprite's backdrop list
    """
    this.__backdrop.next_costume()


def load_image(image_file, alpha=False):
    """
    load image file, convert to surface and save in global list as cache
    - image_file: string, file path
    - return: image surface object
    """
    return SpriteObj.load_image(image_file, alpha)


def get_sprite(name):
    """return found SpriteObj, by name. return None for no found"""
    if name in SpriteObj.obj_dict:
        return SpriteObj.obj_dict[name]
    else:
        return None


def all_sprite():
    """return a list saved all SpriteObj"""
    return SpriteObj.obj_dict


def create_sprite(name):
    """create a SpriteObj"""
    return SpriteObj(name)


def delete_sprite(obj):
    """delete sprite object"""
    obj.hide()
    if obj.name in this.__sprite_objs:
        del this.__sprite_objs[obj.name]


def key_pressed(key_name):
    """return True if key pressed"""
    return key_name.lower() in this.key_press


def set_size(width, height):
    """set screen width and height"""
    this.__screen_size = (width, height)
    this.__screen = pygame.display.set_mode(this.__screen_size, 0, 32)


def set_caption(caption):
    """set window title"""
    if caption and isinstance(caption, str):
        pygame.display.set_caption(caption)


def __init_event():
    for i in range(0, pygame.NUMEVENTS):
        name = pygame.event.event_name(i)
        if name in ['NoEvent', 'Unknown']:
            continue
        if i > 24:
            name = '%s%d' % (name, i - 24)
        this.__event_dict[i] = name
        this.__event_cb[name] = None
        # print(i, this.__event_dict[i])


# init window when module imported
pygame.init()
# this is a pointer to the module object instance itself.
this = sys.modules[__name__]
# we can explicitly make assignments on it
this.__status_bar = True
this.__font_family = 'Console'
this.__font_size = 16
this.__font_obj = pygame.font.SysFont(this.__font_family, this.__font_size)
this.__font_height = this.__font_obj.get_linesize()
this.__screen_size = (800, 600)
this.__screen_resizable = True
this.__screen_closed = False
this.__screen = pygame.display.set_mode(this.__screen_size, 0, 32)
this.__clock = pygame.time.Clock()
this.__event_dict = {}  # event id (int) : event name (string)
this.__event_cb = {}  # event name (string) : event cb (function)
this.__display_objs = {}  # obj_id: obj
this.__sprite_objs = {}
this.__backdrop = SpriteObj('__backdrop__')
this.key_press = []  # for performance
this.mouse_btn = (0, 0, 0)
this.mouse_pos = (0, 0)
this.mouse_rel = (0, 0)
__init_event()
pygame.display.set_caption(__name__)
