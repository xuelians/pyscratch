# pyscratch
Scratch Interface


## Module Variables

- `closed` (bool) default as True, return True once window's top-right close button clicked. 
- `keys` (list) value is empty list [] when no key pressed
- `edge_bounce` (bool) defalut as False, set True to allow bounce if on edge

## Module Methods




## Compatibile

Scratch Method

*Motion*:

- move (10) step    ->  obj.move(10)
- turn clockwise (15) degrees ->  obj.turn_right(15)
- turn anti-clock (15) degrees -> obj.turn_left(15)
- point to direction (90) -> obj.point_dir(90)
- point to mouse  -> obj.point_mose()
- point to sprite -> obj.point_obj(obj)
- glide (1) secs to x (11) y (2)  -> obj.glide(1, 11, 2)
- change x by (10) -> obj.change_x(10)
- set x to (10) -> obj.set_x(10)
- change y by (10) -> obj.change_y(10)
- set y to (10) -> obj.set_y(10)
- if on edge, bounce -> obj.edge_bounce = True
- set rotate style (left-right) -> NONE
- x position -> obj.pos_x
- y position -> obj.pos_y
- direction -> obj.dir

| Looks                 |         |
|-----                  |-----    |
| say hello for 2 sec   |         |
| say hello             |         |
| think hmm.. for 2 sec   |         |
| think hmm..             |         |
| show | obj.show() |
| hide | obj.hide() |
| switch costume to 2 |  obj.switch_costume(2) |
| next costume        | obj.next_costume() |
| switch backdrop to 2 |  screen.switch_backdrop(2) |
| change color effect by 5 | |
| set colro effect as 0 | |
| clear graphic effect | |
| change size by 10 | obj.change_size(10) |
| set size to 100% | obj.size_size(100) | 
| go to front | obj.go_front() |
| go back 1 layout | obj.back_layout(1) |
| custome # | obj.custome | 
| backdrop name | screen.backdrop.name |
| size | obj.size | 




