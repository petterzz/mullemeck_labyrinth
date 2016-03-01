import pyglet, math
import board, resources

class Ball(pyglet.sprite.Sprite):
    def __init__(self, board=None, mass=0.005,  *args, **kwargs):
        super(Ball, self).__init__(
            img=resources.asteroid_image, x=board.x, y=board.y,
            *args, **kwargs)
        self.scale=0.3

        self.g = 9.82
        self.board = board
        # velocity [m/s] (??   pixlar <-> m )
        self.velocity_x = 0.0
        self.velocity_y = 0.0


    def update(self, dt):
        # acceleration from slope
        accel_x = self.g * math.sin(math.radians(self.board.x_rotation))
        accel_y = self.g * -math.sin(math.radians(self.board.y_rotation))
        self.velocity_x += accel_x
        self.velocity_y += accel_y
        # decceleration from friction
        self.velocity_x *= 0.995
        self.velocity_y *= 0.995

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
