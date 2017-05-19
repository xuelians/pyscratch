#!/usr/bin/python3

import pygame
import sys
from pygame.locals import *
from pygame.math import Vector2 as Vec2d

FONT_HEIGHT = 0

__SCREEN_RESIZABLE = True
__SCREEN_WIDTH = 800
__SCREEN_HEIGHT = 600
__SCREEN_SIZE = (__SCREEN_WIDTH, __SCREEN_HEIGHT)
__SCREEN_OBJ = None
__CLOCK_OBJ = None
__EVENT_CB = {
    pygame.QUIT: None,  # none
    pygame.ACTIVEEVENT: None,  # gain, state
    pygame.KEYDOWN: None,  # unicode, key, mod
    pygame.KEYUP: None,  # key, mod
    pygame.MOUSEMOTION: None,  # pos, rel, buttons
    pygame.MOUSEBUTTONUP: None,  # pos, button
    pygame.MOUSEBUTTONDOWN: None,  # pos, button
    pygame.JOYAXISMOTION: None,  # joy, axis, value
    pygame.JOYBALLMOTION: None,  # joy, ball, rel
    pygame.JOYHATMOTION: None,  # joy, hat, value
    pygame.JOYBUTTONUP: None,  # joy, button
    pygame.JOYBUTTONDOWN: None,  # joy, button
    pygame.VIDEORESIZE: None,  # size, w, h
    pygame.VIDEOEXPOSE: None,  # none
    pygame.USEREVENT: None,  # code
}
__EVENT_NAME = {  # event type : event name
    pygame.QUIT: 'QUIT',
    pygame.ACTIVEEVENT: 'ACTIVEEVENT',
    pygame.KEYDOWN: 'KEYDOWN',
    pygame.KEYUP: 'KEYUP',
    pygame.MOUSEMOTION: 'MOUSEMOTION',
    pygame.MOUSEBUTTONUP: 'MOUSEBUTTONUP',
    pygame.MOUSEBUTTONDOWN: 'MOUSEBUTTONDOWN',
    pygame.JOYAXISMOTION: 'JOYAXISMOTION',
    pygame.JOYBALLMOTION: 'JOYBALLMOTION',
    pygame.JOYHATMOTION: 'JOYHATMOTION',
    pygame.JOYBUTTONUP: 'JOYBUTTONUP',
    pygame.JOYBUTTONDOWN: 'JOYBUTTONDOWN',
    pygame.VIDEORESIZE: 'VIDEORESIZE',
    pygame.VIDEOEXPOSE: 'VIDEOEXPOSE',
    pygame.USEREVENT: 'USEREVENT',
}
__DISPLAY_OBJS = {}  # obj_id: obj
__SPRITE_OBJS = {}
__QUIT = False
__BACKDROP = None
__SURF_DICT = {} # save load image surface

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
        self.vdir = Vec2d(0, -1) # point up
        # init actions

    @property
    def name(self):
        """return sprite object name (string)"""
        return self._name

    @property
    def oid(self):
        """return sprite object id (int)"""
        return self._oid

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
        mdir = Vec2d(pygame.mouse.get_pos()) - Vec2d(self._rect.centerx, self._rect.centery)
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
        return self

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

def init(caption="", width=800, height=600, resize=True):
    """
    create a screen
    """
    global __SCREEN_OBJ, __CLOCK_OBJ, __BACKDROP
    if __SCREEN_OBJ is not None:
        return
    # init window
    pygame.init()
    pygame.display.set_caption(caption)
    flags = 0
    flags += pygame.RESIZABLE if resize else 0
    __SCREEN_OBJ = pygame.display.set_mode(__SCREEN_SIZE, 0, 32)
    __CLOCK_OBJ = pygame.time.Clock()
    __BACKDROP = SpriteObj('__backdrop__')
    # _print_cb()


def set_event(event_name, func=None):
    """
    register event callback funtion with args. clean callback by set func is None.<br>
    - QUIT, func(args)
    - ACTIVEEVENT, func(gain, state)
    - KEYDOWN, func(key, mod, unicode)
    - KEYUP, func(key, mod)
    - MOUSEMOTION, func(pos, rel, buttons)
    - MOUSEBUTTONUP, func(pos, button)
    - MOUSEBUTTONDOWN, func(pos, button)
    - JOYAXISMOTION, func(joy, axis, value)
    - JOYBALLMOTION, func(joy, ball, rel)
    - JOYHATMOTION, func(joy, hat, value)
    - JOYBUTTONUP, func(joy, button)
    - JOYBUTTONDOWN, func(joy, button)
    - VIDEORESIZE, func(size, w, h)
    - VIDEOEXPOSE, func(args)
    - USEREVENT, func(code)
    """
    if not isinstance(event_name, str):
        raise ValueError('expect event name is a string')
    for val, name in __EVENT_NAME.items():
        if name == event_name:
            __EVENT_CB[val] = func
            return
    event_list = ' '.join(__EVENT_NAME.values())
    raise ValueError('expect event name is one of below:\n%s' % event_list)


def _event_name(event_type):
    return __EVENT_NAME.get(event_type, 'UNKNOWN')


def _event_type(event_name):
    return __EVENT_NAME.get(event_type, 0)


def _print_cb():
    for event, func in __EVENT_CB.items():
        print(event, _event_name(event), func)


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
    if __SCREEN_OBJ is None:
        init()
    """
    waiting event from screen
    """
    time_passed = __CLOCK_OBJ.tick(wait_tick)
    # event handle
    for event in pygame.event.get():
        # print(event)
        # pre-process
        if event.type == pygame.QUIT:
            global __QUIT
            __QUIT = True
        # invoke callback
        func = __EVENT_CB.get(event.type, None)
        if func:
            if event.type == pygame.QUIT:
                func(args)
            elif event.type == pygame.ACTIVEEVENT:
                func(event.gain, event.state)
            elif event.type == pygame.KEYDOWN:
                func(event.key, event.mod, event.unicode)
            elif event.type == pygame.KEYUP:
                func(event.key, event.mod)
            elif event.type == pygame.MOUSEMOTION:
                func(event.pos, event.rel, event.buttons)
            elif event.type == pygame.MOUSEBUTTONUP:
                func(event.pos, event.button)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                func(event.pos, event.button)
            elif event.type == pygame.JOYAXISMOTION:
                func(event.joy, event.axis, event.value)
            elif event.type == pygame.JOYBALLMOTION:
                func(event.joy, event.ball, event.rel)
            elif event.type == pygame.JOYHATMOTION:
                func(event.joy, event.hat, event.value)
            elif event.type == pygame.JOYBUTTONUP:
                func(event.joy, event.button)
            elif event.type == pygame.JOYBUTTONDOWN:
                func(event.joy, event.button)
            elif event.type == pygame.VIDEORESIZE:
                func(event.size, event.w, event.h)
            elif event.type == pygame.VIDEOEXPOSE:
                func(args)
            elif event.type == pygame.USEREVENT:
                func(event.code)
            else:
                pass
    return time_passed

def refresh():
    # refresh
    # if __BACKDROP._surf:
    #     __SCREEN_OBJ.blit(__BACKDROP._surf, __BACKDROP._rect)
    if __BACKDROP._surf:
        for y in range(0, __SCREEN_HEIGHT, __BACKDROP._surf.get_height()):
            for x in range(0, __SCREEN_WIDTH, __BACKDROP._surf.get_width()):
                __SCREEN_OBJ.blit(__BACKDROP._surf, (x, y))

    for _, obj in __DISPLAY_OBJS.items():
        if isinstance(obj, SpriteObj) and obj._surf:
            __SCREEN_OBJ.blit(obj._surf, obj._rect)
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

def is_key_pressed(key):
    pressed_keys = pygame.key.get_pressed()
    if key == 'UP':
        pressed = pressed_keys[K_UP]
    elif key == 'DOWN':
        pressed = pressed_keys[K_DOWN]
    elif key == 'LEFT':
        pressed = pressed_keys[K_LEFT]
    elif key == 'RIGHT':
        pressed = pressed_keys[K_RIGHT]
    elif key == 'SPACE':    
        pressed = pressed_keys[K_SPACE]
    else:
        pressed = 0
    return pressed
