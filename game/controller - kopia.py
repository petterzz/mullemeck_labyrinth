import math
from pyglet.window import key

class Controller:
    def __init__(self, limits=[-90, 90], servo_x=None, servo_y=None,
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


    #def controlSignalfromKeys(self, dt)

    def update(self, dt):
        # if keys are pressed
        if self.key_handler[key.LEFT]:
            if self.servo_x.position_state > self.limit_min:
                self.controlSignal_x = (self.servo_x.position_state -
                                        self.servo_x.MOTOR_SPEED*dt)
            else:
                self.controlSignal_x = self.limit_min
        elif self.key_handler[key.RIGHT]:
            if self.servo_x.position_state < self.limit_max:
                self.controlSignal_x = (self.servo_x.position_state +
                                        self.servo_x.MOTOR_SPEED*dt)
            else:
                self.controlSignal_x = self.limit_max
        # if no keys are pressed
        else:
            # if close to zero
            if (abs(self.servo_x.position_state) < self.servo_x.MOTOR_SPEED*dt):
                self.controlSignal_x = 0
            # return to zero at half speed
            else:
                if self.servo_x.position_state < 0:
                    self.controlSignal_x = (self.servo_x.position_state +
                                            self.servo_x.MOTOR_SPEED*dt*0.5)
                if self.servo_x.position_state > 0:
                    self.controlSignal_x = (self.servo_x.position_state -
                                            self.servo_x.MOTOR_SPEED*dt*0.5)
        # send control signal to servo object
        self.servo_x.controlSignal = self.controlSignal_x
        self.servo_y.controlSignal = self.controlSignal_y
