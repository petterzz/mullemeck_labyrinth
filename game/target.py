import pyglet
import board, resources
from pyglet.window import key

class Target(pyglet.sprite.Sprite):
    def __init__(self, board=None, *args, **kwargs):
        super(Target, self).__init__(
            img=resources.target_image, x=board.x, y=board.y,
            *args, **kwargs)
        self.scale=1.0
        self.board = board

        self.tracklistPos = 0
        self.tracklist = [[80,60],[90,-80],[-130,-110],[-70,50]]


    def on_key_press(self, symbol, modifiers):
        if symbol == key.T:
            if self.tracklistPos == len(self.tracklist)-1:
                self.tracklistPos = 0
            else:
                self.tracklistPos += 1

    def update(self, dt):
        self.x = self.board.x + self.tracklist[self.tracklistPos][0]
        self.y = self.board.y + self.tracklist[self.tracklistPos][1]
