
class Servo:
    def __init__(self, *args, **kwargs):


        # Motor max speed [deg/s]
        self.MOTOR_SPEED = 250.0
        # Control signal [deg]
        self.controlSignal = 0

        # --State variables
        # Motor position [deg]
        self.position_state = 0.0
        # Motor speed [deg/s]
        self.motorSpeed_state = 0.0


    def update(self, dt):
        # update position according to control signal and motor speed
        if self.controlSignal < self.position_state:
            if abs(self.position_state - self.controlSignal) < self.MOTOR_SPEED*dt:
                self.position_state = self.controlSignal
            else:
                self.position_state -= self.MOTOR_SPEED*dt
        if self.controlSignal > self.position_state:
            if abs(self.position_state - self.controlSignal) < self.MOTOR_SPEED*dt:
                self.position_state = self.controlSignal
            else:
                self.position_state += self.MOTOR_SPEED*dt
