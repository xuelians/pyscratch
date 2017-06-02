#!/usr/bin/python3
"""Summary

Attributes:
    this (TYPE): Description
    VER (tuple): Description
"""

import math
import random
import sys

import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vec2d

VER = (0, 1)


class SpriteObj(object):
    """Sprite Object

    Attributes:
        - name (str): unique name
        - oid (inr): unique id
        - owner (obj): the user of SpriteObj
        - surf (pygame.Surface): surface object
        - pos (tuple): center position (x, y)
        - pos_x (int): center x
        - pos_y (int): center y


    Methods:
        - set_owner(obj): set user of surface object
        - get_sprite_owner(name): get user of surface object
        - get
        - in_pos(x, y): check if SpriteObj cover given position
        - out_of_screen(): return True if SpriteObj out of screen
        - collide_objs(objs): return True if this SpriteObjs covered others
        - get_sprite_in_pos(pos): Get the SpriteObj which is at position
        - get_sprite_under_mouse(): Get the SpriteObj which is under mouse position
        - get_sprite_by_name(prefix):
    """
    _oid_cnt = 0
    _obj_dict = {}
    _obj_dead = []  # put name here to delete a sprite obj
    _image_cache = {}  # save loaded image surface

    def __init__(self, name=''):
        """Summary

        Args:
            name (str, optional): Description
        """
        super().__init__()
        # base
        if name.endswith('XXXXXX'):
            self._oid = SpriteObj.__gen_oid()
            self._name = name.replace('XXXXXX', str(self._oid))
        else:
            SpriteObj.__check_name(name)
            self._oid = SpriteObj.__gen_oid()
            self._name = name if name else 'SpriteObj_%d' % self._oid
        self._owner = self
        # for display
        self._hidden = False
        self._surf = None
        self._costume = []
        self._costume_used = 0
        self._rotate_angle = 0
        self._rotate_angle2 = 0  # rotated angle for performance
        self._rotate_surf = None
        # for motion
        self._vdir = Vec2d(0, -1)  # point up
        self._vpos = Vec2d(0, 0)  # position
        # for auto-move
        self._am_enabled = False
        self._am_speed = 1
        # init actions
        SpriteObj._append_obj(self)

    def __str__(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return 'SpriteObj<%s>' % self._name

    def __repr__(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return 'SpriteObj<%s>' % self._name

    @classmethod
    def __check_name(cls, name):
        """raise RuntimeError if name has been used

        Args:
            name (TYPE): Description

        Raises:
            RuntimeError: Description
        """
        if name in cls._obj_dict:
            raise RuntimeError(
                'name [%s] has been used for another SpriteObj' % name)

    @classmethod
    def __gen_oid(cls):
        """return a integer as unique object id

        Returns:
            TYPE: Description
        """
        cls._oid_cnt += 1
        return cls._oid_cnt

    @classmethod
    def _append_obj(cls, obj):
        """append SpriteObj into managed list

        Args:
            obj (TYPE): Description

        Raises:
            RuntimeError: Description
        """
        if obj is None:
            raise RuntimeError('Expect SpriteObj but None')
        if obj.name in cls._obj_dict:
            raise RuntimeError(
                'name [%s] has been used for another SpriteObj' % obj.name)
        cls._obj_dict[obj.name] = obj

    @classmethod
    def _delete_obj(cls, name_or_obj):
        """delete SpriteObj from managed list

        Args:
            name_or_obj (TYPE): Description
        """
        if isinstance(name_or_obj, cls):
            cls._obj_dead.append(name_or_obj.name)
        else:
            cls._obj_dead.append(name_or_obj)

    @classmethod
    def _update_all(cls):
        """re-draw all managed object on screen
        """
        while cls._obj_dead:
            name = cls._obj_dead.pop()
            if name in cls._obj_dict:
                # print('del %s' % name)
                del cls._obj_dict[name]
        for obj in cls._obj_dict.values():
            obj._update()

    @classmethod
    def load_image(cls, image_file, alpha=False):
        """get image serface from cached list

        Args:
            image_file (TYPE): Description
            alpha (bool, optional): Description

        Returns:
            TYPE: Description

        Raises:
            IOError: Description
        """
        if image_file not in cls._image_cache:
            if image_file.endswith('.png') or alpha:
                surf = pygame.image.load(image_file).convert_alpha()
            else:
                surf = pygame.image.load(image_file).convert()
            if surf:
                cls._image_cache[image_file] = surf
            else:
                raise IOError('fail to load image %s' % image_file)
        return cls._image_cache[image_file]

    @property
    def name(self):
        """sprite object name (str)

        Returns:
            TYPE: Description
        """
        return self._name

    @property
    def owner(self):
        """return the owner of sprite (obj)

        Returns:
            TYPE: Description
        """
        return self._owner

    # @property
    # def surf(self):
    #     """sprite display surface (refer to pygame.surface)

    #     Returns:
    #         TYPE: Description
    #     """
    #     return self._surf

    @property
    def topleft(self):
        return self._rect.topleft

    @property
    def bottomleft(self):
        return self._rect.bottomleft

    @property
    def bottomleft(self):
        return self._rect.bottomleft

    @property
    def pos(self):
        """return (x,y) of current position

        Returns:
            TYPE: Description
        """
        return (self._vpos[0], self._vpos[1])

    @property
    def pos_x(self):
        """return x of current position

        Returns:
            TYPE: Description
        """
        return self._vpos[0]

    @property
    def pos_y(self):
        """return y of current position

        Returns:
            TYPE: Description
        """
        return self._vpos[1]

    def set_pos(self, xy_or_x, y=None):
        pos = xy_or_x if y is None else (xy_or_x, y)
        self._vpos = Vec2d(pos)

    def set_owner(self, value):
        """
        set the owner of sprite object,
        used by get_sprite_owner() later

        Args:
            value (TYPE): Description
            - value (obj): a object as user of sprite object
        """
        self._owner = value

    def in_pos(self, xy_or_x, y=None):
        """check if SpriteObj cover given position

        Args:
            - xy_or_x (tuple/int): Description
            - y (int, optional): Description

        Returns:
            - bool: return True if sprite object at position
        """
        if self._hidden:
            return False
        x = xy_or_x if y is not None else xy_or_x[0]
        y = y if y is not None else xy_or_x[1]
        rect = self._surf.get_rect()
        rect.center = (self._vpos[0], self._vpos[1])
        return rect.collidepoint(x, y)

    def out_of_screen(self):
        """check if sprite is out of screen

        Returns:
            bool: return True if SpriteObj out of screen
        """
        scr_rect = pygame.display.get_surface().get_rect()
        if self._rotate_angle and self._rotate_surf:
            obj_rect = self._rotate_surf.get_rect(
                center=(self._vpos[0], self._vpos[1]))
        else:
            obj_rect = self._surf.get_rect(
                center=(self._vpos[0], self._vpos[1]))
        return not scr_rect.colliderect(obj_rect)

    def collide_objs(self, objs):
        """Summary

        Args:
            objs (list): other SpriteObjs

        Returns:
            bool: return True if this SpriteObjs covered others
        """
        cobjs = []
        if objs:
            for obj in objs:
                self_rect = self._surf.get_rect(center=self.pos)
                obj_rect = obj._surf.get_rect(center=obj.pos)
                if self_rect.colliderect(obj_rect):
                    cobjs.append(obj)
        return cobjs

    def _update(self):
        """update the sprite on screen with new custome and new position

        Returns:
            TYPE: Description
        """
        if self._hidden:
            return
        if self._surf is not None:
            scr = pygame.display.get_surface()
            if self._rotate_angle:
                self.__rotate()
            else:
                self._rotate_surf = self._surf
            rect = self._rotate_surf.get_rect(
                center=(self._vpos[0], self._vpos[1]))
            scr.blit(self._rotate_surf, rect)
            # auto-move
            if self._am_enabled:
                self.move(self._am_speed)
                if self.out_of_screen():
                    self._delete_obj(self)

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
    @property
    def dir(self):
        """return a float angle as current moving direction, 0 is up, 90 is right

        Returns:
            TYPE: Description
        """
        return Vec2d(0, -1).angle_to(self._vdir)

    def change_dir(self, angle, rotate=False):
        """turn a angle on current moving direction,
        positive angle means turn clockwise

        Args:
            angle (TYPE): Description
            rotate (bool, optional): Description
        """
        self._vdir = self._vdir.rotate(angle)
        if rotate:
            self._rotate_angle = int(self.dir)

    def point_dir(self, angle, rotate=False):
        """
        Set the angle as current moving direction
        - angle: 0~360, 0 for up, 90 for right, 180 for down, 270 for left

        Args:
            angle (int): Description
            rotate (bool, optional): Description
        """
        self._vdir = Vec2d(0, -1).rotate(angle)
        if rotate:
            self._rotate_angle = int(self.dir)

    def turn_left(self, angle, rotate=False):
        """
        Turn a angle to the left on current moving direction,
        as same as anti-clockwise

        Args:
            angle (TYPE): Description
            rotate (bool, optional): Description
        """
        self.change_dir(-angle, rotate=rotate)

    def turn_right(self, angle, rotate=False):
        """Turn a right to the right on current moving direction,
        as same as clockwise

        Args:
            angle (TYPE): Description
            rotate (bool, optional): Description
        """
        self.change_dir(angle, rotate=rotate)

    def point_pos(self, xy_or_x, y=None, rotate=False):
        """Set current moving direction to a postion

        Args:
            xy_or_x (TYPE): Description
            y (None, optional): Description
            rotate (bool, optional): Description
        """
        pos = xy_or_x if y is None else (xy_or_x, y)
        mdir = Vec2d(pos) - self._vpos
        if mdir != (0, 0):
            angle = Vec2d(0, -1).angle_to(mdir)
            self.point_dir(angle, rotate=rotate)

    def point_mouse(self, rotate=False):
        """Set current moving direction to mouse postion

        Args:
            rotate (bool, optional): Description
        """
        self.point_pos(pygame.mouse.get_pos(), rotate=rotate)

    def point_obj(self, obj, rotate=False):
        """Set current moving direction to a SpriteObj

        Args:
            obj (TYPE): Description
            rotate (bool, optional): Description
        """
        self.point_pos(obj.pos, rotate=rotate)

    def move(self, steps):
        """move steps on current moving direction

        Args:
          - steps (int): Description
        """
        self._vpos += self._vdir * steps

    def move_to(self, xy_or_x, y=None):
        """
        set sprite center to given position (pixel x & y)

        Args:
          - xy (tuple): position (x,y)
          - x, y (int): position x and y
        """
        pos = xy_or_x if y is None else (xy_or_x, y)
        self.set_pos(pos)

    def set_auto_move(self, speed, dir):
        """Summary

        Args:
            speed (TYPE): Description
            dir (TYPE): Description
        """
        self._am_enabled = True
        self._am_speed = speed
        self.point_dir(dir, True)

    def change_x(self, amount):
        """Change the x position by this amount

        Args:
          - amount (int): step in x-arix (postive to right)
        """
        self._vpos[0] += amount

    def change_y(self, amount):
        """Change the y position by this amount

        Args:
          - amount (int): step in y-arix (postive to up)
        """
        self._vpos[1] += amount

    def set_x(self, amount):
        """Set the x position of a sprite

        Args:
          - amount (int): position x
        """
        self._vpos[0] = amount

    def set_y(self, amount):
        """Change the y position by this amount

        Args:
          - amount (int): position y
        """
        self._vpos[1] = amount

    def __rotate(self):
        """Create a rotated surface"""
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
        """
        Insert 1 image surface object into costume list.

        Args:
          - image_surf (:obj:pygame.Surface): inserted image surface object
          - index (int, optional): insert position, default as None.
                None: means append the image surface and end of costume list

        Returns:
          - int: the image surface's position in list
        """
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
        """
        Insert one / a list images into costumes list

        Args:
          - image_file (str / list): one or a list of image file path
          - index (int, optional): insert position of images, default as None.
                None means append the image at end of costumes list

        Returns:
          - int: position of first added image in costumes list
        """
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
        """
        Insert one / a list images into costumes,
        then switch the first image as current costum.

        Args:
          - image_file (str / list): one or a list of image file path
          - index (int, optional): insert position of images, default as None.
                None means append the image at end of costumes list
        """
        index = self.add_costume(image_file, index)
        self.switch_costume(index)

    def del_costume(self, index=None):
        """
        delete a costume, default delete last one

        Args:
          - index (int, optional): the sequence of deleted costume

        Returns:
          - (Surface, optional): deleted Surface object
        """
        if index:
            return self._costume.pop(index)
        else:
            return self._costume.pop()

    def switch_costume(self, index):
        """
        Switch costumes to change the look of a sprite

        Args:
          - index (int): index in list
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


class SpriteBar(SpriteObj):

    def __init__(self, name='', value=100, max=100, min=0, width=64, height=10,
                 front_color='red', back_color='black', border_color='white',
                 front_color2=None):
        super().__init__(name)
        self.value = value
        self.val_max = max
        self.val_min = min
        self.bar_width = width
        self.bar_height = height
        self.front_color = front_color
        self.back_color = back_color
        self.border_color = border_color
        self.border = 1

    def _update(self):
        fc = Color(self.front_color) if isinstance(
            self.front_color, str) else Color(*self.front_color)
        bc = Color(self.back_color) if isinstance(
            self.back_color, str) else Color(*self.back_color)
        dc = Color(self.border_color) if isinstance(
            self.border_color, str) else Color(*self.border_color)
        self._surf = pygame.Surface((self.bar_width, self.bar_height))
        bg_rect = self._surf.fill(bc)
        bar_rect = bg_rect.copy()
        bar_rect.width = bg_rect.width * \
            ((self.value - self.val_min) / (self.val_max - self.val_min))
        pygame.draw.rect(self._surf, fc, bar_rect, 0)
        pygame.draw.rect(self._surf, dc, bg_rect, self.border)
        super()._update()


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

    Args:
        name_or_id (TYPE): Description
        func (None, optional): Description

    Raises:
        ValueError: Description
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

    Args:
        image_file (TYPE): Description
        pos_x (TYPE): Description
        pos_y (TYPE): Description

    Returns:
        TYPE: Description
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


def __convert_mouse_button():
    """convert pressed mouse button to a string"""
    btn = pygame.mouse.get_pressed()
    name = 'l' if btn[0] else ''
    name += 'm' if btn[1] else ''
    name += 'r' if btn[2] else ''
    return name

def __update_key_mouse():
    """save key and mouse to global"""
    this.keys = __convert_pressed_keys()
    this.mouse_pos = pygame.mouse.get_pos()
    this.mouse_x = this.mouse_pos[0]
    this.mouse_y = this.mouse_pos[1]
    this.mouse_rel = pygame.mouse.get_rel()
    this.mouse_btn = __convert_mouse_button()


def __call_user_cb(event):
    """Summary

    Args:
        event (TYPE): Description

    Raises:
        ValueError: Description
    """
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
    """Summary

    Args:
        framerate (int, optional): Description

    Returns:
        TYPE: Description
    """
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
    """waiting event from screen

    Returns:
        TYPE: Description
    """
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
    """Summary
    """
    status_text = "fps=%d x=%d y=%d btn=%s key=%s" % (this.fps,
                                                      *this.mouse_pos,
                                                      this.mouse_btn,
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
    """Summary
    """
    SpriteObj._update_all()


def __update_background():
    """Summary
    """
    obj = get_sprite('__backdrop__')
    if obj and obj._surf:
        backdrop_heigth = obj._surf.get_height()
        backdrop_width = obj._surf.get_width()
        screen_width, screen_height = this.size
        for y in range(0, screen_height, backdrop_heigth):
            for x in range(0, screen_width, backdrop_width):
                this.__screen.blit(obj._surf, (x, y))


def get_backdrop():
    """get backdrop sprite object

    Returns:
        TYPE: Description
    """
    return get_sprite('__backdrop__')


def set_backdrop(image_file, index=None):
    """
    add a image into backdrop list, and set it as current backdrop

    Args:
        image_file (TYPE): Description
        index (None, optional): Description
    """
    obj = get_backdrop()
    index = obj.add_costume(image_file, index)
    obj.switch_costume(index)


def add_backdrop(image_file, index=None):
    """
    add a image into backdrop list

    Args:
        image_file (TYPE): Description
        index (None, optional): Description
    """
    get_backdrop().add_costume(image_file, index)


def del_backdrop(index=None):
    """
    remove a image into backdrop list

    Args:
        index (None, optional): Description

    Returns:
        TYPE: Description
    """
    return get_backdrop().del_costume(index)


def switch_backdrop(index):
    """
    Switch backdrops to change the look of a sprite

    Args:
        index (TYPE): Description
    """
    get_backdrop().switch_costume(index)


def next_backdrop():
    """
    Switches to the next backdrop in the sprite's backdrop list
    """
    get_backdrop().next_costume()


def _load_image(image_file, alpha=False):
    """
    load image file, convert to surface and save in global list as cache
    - image_file: string, file path
    - return: image surface object

    Args:
        image_file (TYPE): Description
        alpha (bool, optional): Description

    Returns:
        TYPE: Description
    """
    return SpriteObj.load_image(image_file, alpha)


def get_sprite(name, defval=None):
    """return found SpriteObj, by name. return None for no found

    Args:
        name (TYPE): Description
        defval (None, optional): Description

    Returns:
        TYPE: Description
    """
    if name in SpriteObj._obj_dict:
        return SpriteObj._obj_dict[name]
    else:
        return defval


def get_sprite_owner(name, defval=None):
    """return the owner of SpriteObj (found by name).
    return None for no found,
    return SpriteObj self if SpriteObj not has owner

    Args:
        name (TYPE): Description
        defval (None, optional): Description

    Returns:
        TYPE: Description
    """
    if name in SpriteObj._obj_dict:
        return SpriteObj._obj_dict[name].owner
    else:
        return defval


def all_sprite():
    """return a list saved all SpriteObj

    Returns:
        TYPE: Description
    """
    return SpriteObj._obj_dict


def draw_box(width, height, color, bgcolor, border=0):
    fc = Color(color) if isinstance(color, str) else Color(*color)
    bc = Color(bgcolor) if isinstance(bgcolor, str) else Color(*bgcolor)
    obj = SpriteObj()
    obj._surf = pygame.Surface((width, height))
    obj._rect = pygame.draw.rect(obj._surf, fc, obj._surf.fill(bc), border)
    return obj


def create_sprite(name, owner=None, images=None, xy_or_x=None, y=None):
    """create a SpriteObj with a name

    Args:
    - name (str): unique name, support auto-name which end with 'XXXXXX'
    - owner (obj, optional): set owner for sprite, used for get owner if has sprite
    - images (str/list, optional): init the costume from image file path / file list
    - xy (tuple): position (x,y)
    - x, y (int, optional): position x & y

    Returns:
    - obj: create SpriteObj
    """
    obj = SpriteObj(name)
    if owner is not None:
        obj.set_owner(owner)
    if images is not None:
        obj.set_costume(images)
    if xy_or_x is not None:
        pos = xy_or_x if y is None else (xy_or_x, y)
        obj.move_to(pos)
    return obj


def delete_sprite(obj):
    """delete sprite object

    Args:
        obj (TYPE): Description
    """
    SpriteObj._delete_obj(obj)


def key_pressed(key_name):
    """return True if key pressed

    Args:
        key_name (TYPE): Description

    Returns:
        TYPE: Description
    """
    return key_name.lower() in this.keys


def set_size(width, height):
    """set screen width and height

    Args:
        width (TYPE): Description
        height (TYPE): Description
    """
    this.size = (width, height)
    this.__screen = pygame.display.set_mode(this.size, 0, 32)


def set_caption(caption):
    """set window title

    Args:
        caption (TYPE): Description
    """
    if caption and isinstance(caption, str):
        pygame.display.set_caption(caption)


def __init_event():
    """Summary
    """
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
    """time in milliseconds

    Returns:
        TYPE: Description
    """
    return pygame.time.get_ticks()


def get_sprite_by_name(prefix):
    """Summary

    Args:
        prefix (TYPE): Description

    Returns:
        TYPE: Description
    """
    objs = []
    for name, obj in SpriteObj._obj_dict.items():
        if name.startswith(prefix):
            objs.append(obj)
    return objs


def get_sprite_in_pos(xy_or_x, y=None):
    """return a SpriteObj list which is in given position

    Args:
        xy_or_x (TYPE): Description
        y (None, optional): Description

    Returns:
        TYPE: Description
    """
    objs = []
    pos = (xy_or_x, y) if y is not None else xy_or_x
    for obj in SpriteObj._obj_dict.values():
        if obj.in_pos(pos):
            objs.append(obj)
    return objs


def get_sprite_under_mouse():
    """
    Get the SpriteObj which is under mouse position

    Returns:
        obj: return a SpriteObj list
    """
    return get_sprite_in_pos(this.mouse_pos)


def random_num(min, max):
    """Summary

    Args:
        min (TYPE): Description
        max (TYPE): Description

    Returns:
        TYPE: Description
    """
    return random.random() * (max - min) + min


def random_pos():
    """Summary

    Returns:
        TYPE: Description
    """
    x = random_num(0, this.size[0])
    y = random_num(0, this.size[1])
    return (x, y)


def mouse_down(button='any'):
    """return True if mouse button is pressed"""
    if button.lower() in ['left', 'lbutton', 'l']:
        return 'l' in this.mouse_btn
    elif button.lower() in ['middle', 'mbutton', 'm']:
        return 'm' in this.mouse_btn
    elif button.lower() in ['right', 'rbutton', 'r']:
        return 'r' in this.mouse_btn
    else:
        return this.mouse_btn != ''


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
this.mouse_btn = ''
this.mouse_pos = (0, 0)
this.mouse_x = 0
this.mouse_y = 0
this.mouse_rel = (0, 0)
this.fps = 0
__init_event()
pygame.display.set_caption(__name__)
create_sprite('__backdrop__').hide()
