#!/usr/bin/python3

import pygame
import sys
import math
import random
from pygame.locals import *
from pygame.math import Vector2 as Vec2d

VER = (0, 1)


class SpriteObj():
    """Sprite Object"""
    oid_cnt = 0
    obj_dict = {}
    obj_dead = []  # put name here to delete a sprite obj
    image_cache = {}  # save loaded image surface

    def __init__(self, name='', owner=None):
        # base
        if name.endswith('XXXXXX'):
            self._oid = SpriteObj.gen_oid()
            self._name = name.replace('XXXXXX', str(self._oid))
        else:
            SpriteObj.check_name(name)
            self._oid = SpriteObj.gen_oid()
            self._name = name if name else 'SpriteObj_%d' % self._oid
        self._owner = self if owner is None else owner
        # for display
        self._hidden = False
        self._surf = None
        self._costume = []
        self._costume_used = 0
        self._rotate_angle = 0
        self._rotate_angle2 = 0  # rotated angle for performance
        self._rotate_surf = None
        # for motion
        self.vdir = Vec2d(0, -1)  # point up
        self.vpos = Vec2d(0, 0)  # position
        # for auto-move
        self._am_enabled = False
        self._am_speed = 1
        # init actions
        SpriteObj.append_obj(self)

    def __str__(self):
        return 'SpriteObj<%s>' % self._name

    def __repr__(self):
        return 'SpriteObj<%s>' % self._name

    @classmethod
    def check_name(cls, name):
        """raise RuntimeError if name has been used"""
        if name in cls.obj_dict:
            raise RuntimeError(
                'name [%s] has been used for another SpriteObj' % name)

    @classmethod
    def gen_oid(cls):
        """return a integer as unique object id"""
        cls.oid_cnt += 1
        return cls.oid_cnt

    @classmethod
    def append_obj(cls, obj):
        """append SpriteObj into managed list"""
        if obj is None:
            raise RuntimeError('Expect SpriteObj but None')
        if obj.name in cls.obj_dict:
            raise RuntimeError(
                'name [%s] has been used for another SpriteObj' % obj.name)
        cls.obj_dict[obj.name] = obj

    @classmethod
    def delete_obj(cls, name_or_obj):
        """delete SpriteObj from managed list"""
        if isinstance(name_or_obj, cls):
            cls.obj_dead.append(name_or_obj.name)
        else:
            cls.obj_dead.append(name_or_obj)

    @classmethod
    def update_all(cls):
        """re-draw all managed object on screen"""
        while cls.obj_dead:
            name = cls.obj_dead.pop()
            if name in cls.obj_dict:
                # print('del %s' % name)
                del cls.obj_dict[name]
        for obj in cls.obj_dict.values():
            obj._update()

    @classmethod
    def load_image(cls, image_file, alpha=False):
        """get image serface from cached list"""
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
    def owner(self):
        """return the owner of sprite"""
        return self._owner

    @property
    def surf(self):
        """sprite display surface (refer to pygame.surface)"""
        return self._surf

    @property
    def pos(self):
        """return (x,y) of current position"""
        return (self.vpos[0], self.vpos[1])

    @property
    def pos_x(self):
        """return x of current position"""
        return self.vpos[0]

    @property
    def pos_y(self):
        """return y of current position"""
        return self.vpos[1]

    def in_pos(self, xy_or_x, y=None):
        """return True if sprite object on given position (x,y)"""
        if self._hidden:
            return False
        x = xy_or_x if y is not None else xy_or_x[0]
        y = y if y is not None else xy_or_x[1]
        rect = self._surf.get_rect()
        rect.center = (self.vpos[0], self.vpos[1])
        return rect.collidepoint(x, y)

    def out_of_screen(self):
        """check if sprite is out of screen"""
        scr_rect = pygame.display.get_surface().get_rect()
        if self._rotate_angle and self._rotate_surf:
            obj_rect = self._rotate_surf.get_rect(
                center=(self.vpos[0], self.vpos[1]))
        else:
            obj_rect = self._surf.get_rect(center=(self.vpos[0], self.vpos[1]))
        return not scr_rect.colliderect(obj_rect)

    def collide_objs(self, objs):
        cobjs = []
        if objs:
            for obj in objs:
                self_rect = self._surf.get_rect(
                    center=(self.vpos[0], self.vpos[1]))
                obj_rect = obj._surf.get_rect(
                    center=(obj.vpos[0], obj.vpos[1]))
                if self_rect.colliderect(obj_rect):
                    cobjs.append(obj)
        return cobjs

    def _update(self):
        """update the sprite on screen with new custome and new position"""
        if self._hidden:
            return
        if self._surf is not None:
            scr = pygame.display.get_surface()
            if self._rotate_angle:
                self._rotate()
            else:
                self._rotate_surf = self._surf
            rect = self._rotate_surf.get_rect(
                center=(self.vpos[0], self.vpos[1]))
            scr.blit(self._rotate_surf, rect)
            # auto-move
            if self._am_enabled:
                self.move(self._am_speed)
                if self.out_of_screen():
                    self.delete_obj(self)

    def show(self):
        """
        Makes sprite appear on the Stage
        """
        self._hidden = False

    def hide(self):
        """
        Make a hide-and-seek game with characters that appear and disappear.
        """
        self._hidden = True

    # Motions Methods
    def get_dir(self):
        """return a float angle as current moving direction, 0 is up, 90 is right"""
        return Vec2d(0, -1).angle_to(self.vdir)

    def change_dir(self, angle, rotate=False):
        """turn a angle on current moving direction,
        positive angle means turn clockwise"""
        self.vdir = self.vdir.rotate(angle)
        if rotate:
            self._rotate_angle = int(self.get_dir())

    def set_dir(self, angle, rotate=False):
        """
        Set the angle as current moving direction
        - angle: 0~360, 0 for up, 90 for right, 180 for down, 270 for left
        """
        self.vdir = Vec2d(0, -1).rotate(angle)
        if rotate:
            self._rotate_angle = int(self.get_dir())

    def turn_left(self, angle, rotate=False):
        """
        Turn a angle to the left on current moving direction,
        as same as anti-clockwise
        """
        self.change_dir(-angle, rotate=rotate)

    def turn_right(self, angle, rotate=False):
        """Turn a right to the right on current moving direction,
        as same as clockwise"""
        self.change_dir(angle, rotate=rotate)

    def point_pos(self, xy_or_x, y=None, rotate=False):
        """Set current moving direction to a postion"""
        if y is not None:
            mdir = Vec2d(xy_or_x, y) - self.vpos
        else:
            mdir = Vec2d(xy_or_x) - self.vpos
        if mdir != (0, 0):
            self.vdir = mdir.normalize()
        if rotate:
            self._rotate_angle = int(self.get_dir())

    def point_mouse(self, rotate=False):
        """Set current moving direction to mouse postion"""
        self.point_pos(pygame.mouse.get_pos(), rotate=rotate)

    def point_obj(self, obj, rotate=False):
        """Set current moving direction to a SpriteObj"""
        self.point_pos(obj.pos, rotate=rotate)

    def move(self, steps):
        """move steps on current moving direction"""
        self.vpos += self.vdir * steps

    def move_to(self, xy_or_x, y=None):
        """
        set sprite center to given position (pixel x & y) with sprite left-top
        """
        if y is not None:
            self.vpos = Vec2d(xy_or_x, y)
        else:
            self.vpos = Vec2d(xy_or_x)

    def set_auto_move(self, speed, dir):
        self._am_enabled = True
        self._am_speed = speed
        self.set_dir(dir, True)

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

    def _rotate(self):
        if self._rotate_angle != self._rotate_angle2:
            angle = self._rotate_angle
            # print(angle)
            org_rect = self._surf.get_rect()
            rect_scale = 1
            arc = math.radians(angle)
            new_w = int((abs(org_rect.width * math.cos(arc)) +
                         abs(org_rect.height * math.sin(arc))) / rect_scale)
            new_h = int((abs(org_rect.width * math.sin(arc)) +
                         abs(org_rect.height * math.cos(arc))) / rect_scale)
            new_surf = pygame.transform.rotate(self._surf, -angle)
            new_surf = pygame.transform.scale(new_surf, (new_w, new_h))
            self._rotate_surf = new_surf
            self._rotate_angle2 = self._rotate_angle

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


def draw_image(image_file, pos_x, pos_y):
    """
    load a image file and set position (left-top)
    """
    obj = SpriteObj()
    obj.add_costume(image_file)
    obj.move_to(pos_x, pos_y)
    return obj


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
    this.keys = __convert_pressed_keys()
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


def __run_fps(framerate=100):
    msec = this.__clock.tick(framerate)
    __run_fps.frame_sum += 1
    if now_time() - __run_fps.last_time > 1000:
        this.fps = int(__run_fps.frame_sum /
                       (now_time() - __run_fps.last_time) * 1000)
        __run_fps.frame_sum = 0
        __run_fps.last_time = now_time()
    return msec


__run_fps.frame_sum = 0
__run_fps.last_time = 0


def run():
    """waiting event from screen"""
    # refresh screen
    __update_background()
    __update_sprites()
    __update_status_bar()
    pygame.display.update()
    # release cpu
    msec = __run_fps(100)
    # event handle
    __update_key_mouse()
    for event in pygame.event.get():
        if event.type == 12:  # 'Quit'
            this.closed = True
        # invoke callback
        __call_user_cb(event)
    return msec


def __update_status_bar():
    status_text = "fps=%d x=%d y=%d key=%s" % (this.fps,
                                               *this.mouse_pos,
                                               '+'.join(this.keys))
    screen_width, screen_height = this.size
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


def __update_sprites():
    SpriteObj.update_all()


def __update_background():
    obj = get_sprite('__backdrop__')
    if obj and obj.surf:
        backdrop_heigth = obj.surf.get_height()
        backdrop_width = obj.surf.get_width()
        screen_width, screen_height = this.size
        for y in range(0, screen_height, backdrop_heigth):
            for x in range(0, screen_width, backdrop_width):
                this.__screen.blit(obj.surf, (x, y))


def get_backdrop():
    """get backdrop sprite object"""
    return get_sprite('__backdrop__')


def set_backdrop(image_file, index=None):
    """
    add a image into backdrop list, and set it as current backdrop
    """
    obj = get_backdrop()
    index = obj.add_costume(image_file, index)
    obj.switch_costume(index)


def add_backdrop(image_file, index=None):
    """
    add a image into backdrop list
    """
    get_backdrop().add_costume(image_file, index)


def del_backdrop(index=None):
    """
    remove a image into backdrop list
    """
    return get_backdrop().del_costume(index)


def switch_backdrop(index):
    """
    Switch backdrops to change the look of a sprite
    """
    get_backdrop().switch_costume(index)


def next_backdrop():
    """
    Switches to the next backdrop in the sprite's backdrop list
    """
    get_backdrop().next_costume()


def load_image(image_file, alpha=False):
    """
    load image file, convert to surface and save in global list as cache
    - image_file: string, file path
    - return: image surface object
    """
    return SpriteObj.load_image(image_file, alpha)


def get_sprite(name, defval=None):
    """return found SpriteObj, by name. return None for no found"""
    if name in SpriteObj.obj_dict:
        return SpriteObj.obj_dict[name]
    else:
        return defval


def get_sprite_owner(name, defval=None):
    """return the owner of SpriteObj (found by name).
       return None for no found,
       return SpriteObj self if SpriteObj not has owner"""
    if name in SpriteObj.obj_dict:
        return SpriteObj.obj_dict[name].owner
    else:
        return defval


def all_sprite():
    """return a list saved all SpriteObj"""
    return SpriteObj.obj_dict


def create_sprite(name, owner=None, images=None, xy_or_x=None, y=None):
    """create a SpriteObj with a name
    - name: string: if name end with 'XXXXXX', use object id to replace the end 'XXXXXX'
    - owner: obj: set owner for sprite, used for get owner if has sprite
    - images: string/list: init the costume from image file path / file list"""
    obj = SpriteObj(name, owner)
    if images is not None:
        obj.set_costume(images)
    if xy_or_x is not None:
        pos = xy_or_x if y is None else (xy_or_x, y)
        obj.move_to(pos)
    return obj


def delete_sprite(obj):
    """delete sprite object"""
    SpriteObj.delete_obj(obj)


def keysed(key_name):
    """return True if key pressed"""
    return key_name.lower() in this.keys


def set_size(width, height):
    """set screen width and height"""
    this.size = (width, height)
    this.__screen = pygame.display.set_mode(this.size, 0, 32)


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


def now_time():
    """time in milliseconds"""
    return pygame.time.get_ticks()


def get_sprite_by_name(prefix):
    objs = []
    for name, obj in SpriteObj.obj_dict.items():
        if name.startswith(prefix):
            objs.append(obj)
    return objs


def get_sprite_in_pos(xy_or_x, y=None):
    """return a SpriteObj list which is in given position"""
    objs = []
    pos = (xy_or_x, y) if y is not None else xy_or_x
    for obj in SpriteObj.obj_dict.values():
        if obj.in_pos(pos):
            objs.append(obj)
    return objs


def get_sprite_under_mouse():
    """return a SpriteObj list which is under mouse position"""
    return get_sprite_in_pos(this.mouse_pos)


def random_num(min, max):
    return random.random() * (max - min) + min


def random_pos():
    x = random_num(0, this.size[0])
    y = random_num(0, this.size[1])
    return (x, y)


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
this.size = (800, 600)
this.__screen_resizable = True
this.closed = False
this.__screen = pygame.display.set_mode(this.size, 0, 32)
this.__clock = pygame.time.Clock()
this.__event_dict = {}  # event id (int) : event name (string)
this.__event_cb = {}  # event name (string) : event cb (function)
this.keys = []  # for performance
this.mouse_btn = (0, 0, 0)
this.mouse_pos = (0, 0)
this.mouse_rel = (0, 0)
this.fps = 0
__init_event()
pygame.display.set_caption(__name__)
create_sprite('__backdrop__').hide()
