#!/usr/bin/python3

import pygame
import sys
from pygame.locals import *
from pygame.math import Vector2 as Vec2d

# config
__SCREEN_RESIZABLE = True
__SCREEN_SIZE = (800, 600)
__FONT_FAMILY = 'Console'
__FONT_SIZE = 16

# global variables
__SCREEN_OBJ = None
__SCREEN_FONT = None
__CLOCK_OBJ = None
__EVENT_DICT = {}  # event id (int) : event name (string)
__EVENT_CB = {}  # event name (string) : event cb (function)
__DISPLAY_OBJS = {}  # obj_id: obj
__SPRITE_OBJS = {}
__QUIT = False
__BACKDROP = None
__SURF_DICT = {}  # save load image surface
__KEY_PRESS = []  # for performance
__MOUSE_PRESS = (0, 0, 0)
__MOUSE_POS = (0, 0)
__MOUSE_REL = (0, 0)


class SpriteObj():
    __counter = 0

    def __init__(self, name=''):
        # base
        SpriteObj.__counter += 1
        self._oid = SpriteObj.__counter
        self._name = name if name else 'SpriteObj_%d' % self._oid
        self._screen = sys.modules[__name__]
        # for display
        self._surf = None
        self._rect = None
        self._costume = []
        self._cur_costume = 0
        # for motion
        self.vdir = Vec2d(0, -1)  # point up
        # init actions

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

    @property
    def rect(self):
        """sprite display position (refer to pygame.rect)"""
        return self._rect

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
        """Turn to the left"""
        self.vdir = self.vdir.rotate(-angle)

    def turn_right(self, angle):
        """Turn to the right"""
        self.vdir = self.vdir.rotate(angle)

    def point_dir(self, angle):
        """Set the direction of the current sprite"""
        self.vdir = Vec2d(0, -1).rotate(angle)

    def point_mouse(self):
        """Set the direction of the current sprite"""
        mdir = Vec2d(pygame.mouse.get_pos()) - \
            Vec2d(self._rect.centerx, self._rect.centery)
        if mdir != (0, 0):
            self.vdir = mdir.normalize()

    def move(self, steps):
        self.vpos = Vec2d(self._rect.centerx, self._rect.centery)
        self.vpos += self.vdir * steps
        self._rect.center = self.vpos

        # self.vpos += self.vdir * self.speed * self.time_passed / self.speed_scale
        # self.vpos.x = fixup_range(self.vpos.x, 0, 800)
        # self.vpos.y = fixup_range(self.vpos.y, 0, 600)

    def move_to(self, center_x, center_y):
        """
        set sprite center to given position (pixel x & y) with sprite left-top
        """
        self._rect = self._surf.get_rect()
        self._rect.center = (center_x, center_y)

    def change_x(self, amount):
        """Change the x position by this amount"""
        self._rect.centerx += amount

    def change_y(self, amount):
        """Change the y position by this amount"""
        self._rect.centery += amount

    def set_x(self, amount):
        """Set the x position of a sprite"""
        self._rect.centerx = amount

    def set_y(self, amount):
        """Change the y position by this amount"""
        self._rect.centery = amount

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
            surf = self._screen.load_image(each)
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
            self._cur_costume = index
        except IndexError as err:
            pass

    def next_costume(self):
        """
        Switches to the next costume in the sprite's costume list
        """
        self._cur_costume += 1
        if self._cur_costume >= len(self._costume):
            self._cur_costume = 0  # back to first costume
        try:
            self._surf = self._costume[self._cur_costume]
        except IndexError as err:
            pass


def __init_event():
    global __EVENT_DICT, __EVENT_CB
    for i in range(0, pygame.NUMEVENTS):
        name = pygame.event.event_name(i)
        if name in ['NoEvent', 'Unknown']:
            continue
        if i > 24:
            name = '%s%d' % (name, i - 24)
        __EVENT_DICT[i] = name
        __EVENT_CB[name] = None
        # print(i, __EVENT_DICT[i])


def init(caption="", width=800, height=600, resize=True):
    """
    create a screen
    """
    global __SCREEN_OBJ, __CLOCK_OBJ, __BACKDROP, __SCREEN_FONT
    if __SCREEN_OBJ is not None:
        return
    # init window
    pygame.init()
    pygame.display.set_caption(caption)
    flags = 0
    flags += pygame.RESIZABLE if resize else 0
    __SCREEN_OBJ = pygame.display.set_mode(__SCREEN_SIZE, 0, 32)
    __SCREEN_FONT = pygame.font.SysFont(__FONT_FAMILY, __FONT_SIZE)
    __CLOCK_OBJ = pygame.time.Clock()
    __BACKDROP = SpriteObj('__backdrop__')
    # _print_cb()
    __init_event()


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
    for eid, name in __EVENT_DICT.items():
        helpmsg += '\n\t%2d: %s' % (eid, name)
    name = __EVENT_DICT.get(name_or_id, None) if isinstance(
        name_or_id, int) else name_or_id
    if name not in __EVENT_CB:
        raise ValueError('invalid event [%s], please use below id or name:%s' %
                         (name_or_id, helpmsg))
    __EVENT_CB[name] = func

def is_quit():
    return __QUIT


def draw_image(image_file, pos_x, pos_y):
    """
    load a image file and set position (left-top)
    """
    obj = SpriteObj()
    obj.add_costume(image_file)
    obj.move_to(pos_x, pos_y)
    return obj


def run(wait_tick=50):
    """waiting event from screen"""
    if __SCREEN_OBJ is None:
        init()
    tick_passed = __CLOCK_OBJ.tick(wait_tick)
    # save key and mouse to global
    global __KEY_PRESS, __MOUSE_POS, __MOUSE_REL, __MOUSE_BTN
    __KEY_PRESS = __convert_pressed_keys()
    __MOUSE_POS = pygame.mouse.get_pos()
    __MOUSE_REL = pygame.mouse.get_rel()
    __MOUSE_BTN = pygame.mouse.get_pressed()
    # event handle
    for event in pygame.event.get():
        # print(pygame.event.event_name(event.type))
        # pre-process
        event_name = pygame.event.event_name(event.type)
        if event_name == 'Quit':
            global __QUIT
            __QUIT = True
        # invoke callback
        func = __EVENT_CB.get(event_name, None)
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
    return tick_passed


def __convert_pressed_keys():
    name = []
    press = pygame.key.get_pressed()
    for i in range(0, len(press)):
        if press[i] == 1:
            name.append(pygame.key.name(i))
    return name


def update():
    """refresh display"""
    # update background
    if __BACKDROP.surf:
        backdrop_heigth = __BACKDROP.surf.get_height()
        backdrop_width = __BACKDROP.surf.get_width()
        screen_width, screen_height = __SCREEN_SIZE
        for y in range(0, screen_height, backdrop_heigth):
            for x in range(0, screen_width, backdrop_width):
                __SCREEN_OBJ.blit(__BACKDROP.surf, (x, y))

    # update sprite
    for _, obj in __DISPLAY_OBJS.items():
        if obj and isinstance(obj, SpriteObj) and obj.surf:
            __SCREEN_OBJ.blit(obj.surf, obj.rect)

    # update status bar
    status_text = "x=%d y=%d key=%s" % (*__MOUSE_POS, '+'.join(__KEY_PRESS))
    screen_width, screen_height = __SCREEN_SIZE
    font_height = __SCREEN_FONT.get_linesize()
    font_color = (255, 200, 0)  # orange
    font_bgcolor = (0, 0, 0)  # black
    # clean old text
    font_surf = pygame.Surface((screen_width, font_height))
    font_rect = font_surf.fill(font_bgcolor).move(
        0, screen_height - font_height)
    __SCREEN_OBJ.blit(font_surf, font_rect)
    # print(status_text)
    font_surf = __SCREEN_FONT.render(
        status_text, True, font_color, font_bgcolor)
    font_rect = font_surf.get_rect().move(0, screen_height - font_height)
    __SCREEN_OBJ.blit(font_surf, font_rect)

    # final refresh
    pygame.display.update()


def show_sprite(obj):
    """
    Makes sprite appear on the Stage
    """
    if not isinstance(obj, SpriteObj):
        raise TypeError('only SpriteObj object can be shown')
    global __DISPLAY_OBJS
    if obj.oid not in __DISPLAY_OBJS:
        __DISPLAY_OBJS[obj.oid] = obj


def hide_sprite(obj):
    """
    Make a hide-and-seek game with characters that appear and disappear.
    """
    if not isinstance(obj, SpriteObj):
        raise TypeError('only SpriteObj object can be hidden')
    global __DISPLAY_OBJS
    if obj.oid in __DISPLAY_OBJS:
        del __DISPLAY_OBJS[obj.oid]


def add_backdrop(image_file, index=None):
    """
    add a image into backdrop list
    """
    __BACKDROP.add_costume(image_file, index)
    __BACKDROP.switch_costume(0)


def del_backdrop(index=None):
    """
    remove a image into backdrop list
    """
    return __BACKDROP.del_costume(index)


def switch_backdrop(index):
    """
    Switch backdrops to change the look of a sprite
    """
    __BACKDROP.switch_costume(index)


def next_backdrop():
    """
    Switches to the next backdrop in the sprite's backdrop list
    """
    __BACKDROP.next_costume()


def load_image(image_file, alpha=False):
    """
    load image, save in module dict
    """
    if image_file not in __SURF_DICT:
        if image_file.endswith('.png') or alpha:
            surf = pygame.image.load(image_file).convert_alpha()
        else:
            surf = pygame.image.load(image_file).convert()
        if surf:
            __SURF_DICT[image_file] = surf
        else:
            raise ValueError('fail to load image %s' % image_file)
    return __SURF_DICT[image_file]


def get_sprite(name):
    if name in __SPRITE_OBJS:
        return __SPRITE_OBJS[name]
    else:
        return None


def all_sprite():
    return __SPRITE_OBJS


def create_sprite(name):
    global __SPRITE_OBJS
    if name not in __SPRITE_OBJS:
        obj = SpriteObj(name)
        show_sprite(obj)
        __SPRITE_OBJS[name] = obj
    return get_sprite(name)


def delete_sprite(obj):
    global __SPRITE_OBJS
    obj.hide()
    if obj.name in __SPRITE_OBJS:
        del __SPRITE_OBJS[obj.name]


def is_key_pressed(key_name):
    """return True if key pressed"""
    return key_name.lower() in __KEY_PRESS
