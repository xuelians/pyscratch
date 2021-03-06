# pyscratch
Scratch Interface

## Install

1. copy screen.py to your folder.
2. add `import screen` at beginning in your file


## Usage

create new python file with below frame.

```python
import screen

def main():
    # add code here to init

    while not screen.closed:
        screen.run()
        # add code here to process periodically
    
    # add code here to clean up
    return

if __name__ == '__main__':
    main()
```


## Module Variables

- `closed` (bool) default as True, return True once window's top-right close button clicked. 
- `keys` (list) value is empty list [] when no key pressed
- `edge_bounce` (bool) default as False, set True to allow bounce if on edge

## Module Methods




## Compatibility

Scratch Method


| *Scratch Motion*                  | *SpriteObj Methods*   | *Notes*           |
|-----                              |-----                  |-----              |
| move (10) step                    | obj.move(10)          |
|                                   | obj.move_to(x, y)     | new               |
| turn clockwise (15) degrees       | obj.turn_right(15)    | support rotate    |
| turn anti-clock (15) degrees      | obj.turn_left(15)     | support rotate    |
| point to direction (90)           | obj.point_dir(90)     | support rotate    |
| point to mouse                    | obj.point_mouse()     | support rotate    |
| point to sprite                   | obj.point_obj(obj)    | support rotate    |
| glide (1) secs to x (11) y (2)    | obj.glide_to(1, 11, 2) | **not yet**    |
| change x by (10)                  | obj.change_x(10)      |
| set x to (10)                     | obj.set_x(10)         |
| change y by (10)                  | obj.change_y(10)      |
| set y to (10)                     | obj.set_y(10)         |
|                                   | obj.set_pos(x, y)     | alias of obj.move_to()  |
| if on edge, bounce                | obj.edge_bounce = True | **not yet**      |
| set rotate style (left-right)     |                       | **not support** |
| x position                        | obj.pos_x             | attr    |
| y position                        | obj.pos_y             | attr    |
| direction                         | obj.dir               | attr    |

| *Looks*                           |         |
|-----                              |-----    |
| say hello for 2 sec               |         |
| say hello                         |         |
| think hmm.. for 2 sec             |         |
| think hmm..                       |         |
| show                              | obj.show() |
| hide                              | obj.hide() |
| switch costume to 2               | obj.switch_costume(2) |
| next costume                      | obj.next_costume() |
| switch backdrop to 2              |  screen.switch_backdrop(2) |
| change color effect by 5          | |
| set colro effect as 0             | |
| clear graphic effect              | |
| change size by 10                 | obj.change_size(10) |
| set size to 100%                  | obj.set_size(100) | 
| go to front                       | obj.go_front() |
| go back 1 layout                  | obj.back_layout(1) |
| custome #                         | obj.custome | 
| backdrop name                     | screen.backdrop.name |
| size                              | obj.size | 

| Sensing                           |         |
|-----                              |-----    |
| touch mouse                       | obj.is_touch_mouse()        |
| touch edge                        | obj.is_touch_edge()        |
| touch sprtie                      | obj.is_touch_obj(obj)        |
| touch color                       |       |
| color1 touch color2               |       |
| distance to mouse                 | obj.distance_to_mouse()       |
| distance to sprtie                | obj.distance_to_obj(obj)       |
| ask xxxx and wait                 | |
| answer                            | |
| key 'space' pressed?              | screen.key_pressed('space') |
| mouse down?                       | screen.mouse_down() |
| mouse x                           | screem.mouse_x |
| mouse y                           | screen.mouse_y |
| loudness                          | |
| video motion on sprite            | |
| turn video on/off                 | |
| set video transparency 10%        | |
| timer                             | |
| reset timer                       | |
| x position of sprite              | |
| y position of sprite              | |
| direction of sprite               | |
| custume # of sprite               | |
| custume name of sprite            | |
| size of sprite                    | |
| volumne of sprite                 | |
| current year/month/.../second     | |
| day since 2000                    | |
| username                          | |





