import math
from pyglet.window import key

class Controller:
    def __init__(self, limits=[-90, 90], servo_x=None, servo_y=None,
                 ball=None, target=None,
                 *args, **kwargs):
        # Servo-objects connected to this controller
        self.servo_x = servo_x
        self.servo_y = servo_y
        # output signals from this controller [deg]
        self.controlSignal_x = 0
        self.controlSignal_y = 0
        # limits to output signals [deg]
        self.limit_min = limits[0]
        self.limit_max = limits[1]

        self.key_handler = key.KeyStateHandler()

        self.ball = ball
        self.target = target

        self.distToTarget_x = 0
        self.distToTarget_y = 0

    # determine control signal based on arrow keys held down
    def controlSignalFromKeys(self, dt, servo, key_decrease, key_increase):
        # if keys are pressed
        if self.key_handler[key_decrease]:
            if servo.position_state > self.limit_min:
                controlSignal = (servo.position_state - servo.MOTOR_SPEED*dt)
            else:
                controlSignal = self.limit_min
        elif self.key_handler[key_increase]:
            if servo.position_state < self.limit_max:
                controlSignal = (servo.position_state + servo.MOTOR_SPEED*dt)
            else:
                controlSignal = self.limit_max
        # if no keys are pressed
        else:
            # if close to zero
            if (abs(servo.position_state) < servo.MOTOR_SPEED*dt):
                controlSignal = 0
            # return to zero at half speed
            else:
                if servo.position_state < 0:
                    controlSignal = (servo.position_state +
                                     servo.MOTOR_SPEED*dt*0.5)
                if servo.position_state > 0:
                    controlSignal = (servo.position_state -
                                     servo.MOTOR_SPEED*dt*0.5)
        return controlSignal

    def controlSignalFromController(self):
        k1 = 1
        k2 = 1
        k3 = 2
        k4 = 0.3


        vx = self.ball.velocity_x
        dx = self.distToTarget_x
        cx = (k1*dx + (dx*k2-vx*k3))*k4

        vy = self.ball.velocity_y
        dy = self.distToTarget_y
        cy = (k1*dy + (dy*k2-vy*k3))*k4

        if cx < -40:
            cx = -40
        if cx > 40:
            cx = 40

        if cy < -40:
            cy = -40
        if cy > 40:
            cy = 40


        return [cx, -cy]

    def update(self, dt):
        # calculate control signals and send to servo objects
        if self.key_handler[key.SPACE]:
            [self.servo_x.controlSignal, self.servo_y.controlSignal] = self.controlSignalFromController()

            print [self.servo_x.controlSignal, self.servo_y.controlSignal]

        else:
            self.servo_x.controlSignal = self.controlSignalFromKeys(dt, self.servo_x, key.LEFT, key.RIGHT)
            self.servo_y.controlSignal = self.controlSignalFromKeys(dt, self.servo_y, key.UP, key.DOWN)



        self.distToTarget_x = self.target.x - self.ball.x
        self.distToTarget_y = self.target.y - self.ball.y
