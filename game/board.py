import pyglet
from pyglet.window import key
import resources

class Board:
    def __init__(self, x=0, y=0, batch=None, *args, **kwargs):

        self.topview_sprite = pyglet.sprite.Sprite(
                              img=resources.board_topview_image,
                              x=x, y=y,
                              batch = batch,
                              *args, **kwargs)
        self.xview_sprite = pyglet.sprite.Sprite(
                              img=resources.board_sideview_image,
                              x = self.topview_sprite.x,
                              y = (self.topview_sprite.y -
                                   self.topview_sprite.height/2 - 140),
                              batch = batch,
                              *args, **kwargs)
        self.yview_sprite = pyglet.sprite.Sprite(
                              img=resources.board_sideview_image,
                              x = (self.topview_sprite.x -
                                   self.topview_sprite.width/2 - 140),
                              y = self.topview_sprite.y,
                              batch = batch,
                              *args, **kwargs)

        self.topview_sprite.scale=1.5

        self.yview_sprite.rotation = -90

        self.x = x
        self.y = y
        self.x_rotation = 0
        self.y_rotation = 0



    def update(self, dt):
        self.xview_sprite.rotation = self.x_rotation
        self.yview_sprite.rotation = self.y_rotation - 90
