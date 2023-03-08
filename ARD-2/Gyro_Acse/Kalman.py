

class KalmanAngle:
    def __init__(self):
        self.angle = 0.0
        self.uncertanty = 4
        self.angle_prediction = 0
        self.kalman_usertanty = 0
        self.kalman_gain = 0
        self.acc_std = 3


    def getAngle(self, acc_angle, gyro_angle, dt):
        self.angle = self.angle + gyro_angle * dt
        self.uncertanty += dt**2 * self.uncertanty ** 2
        self.kalman_gain = self.uncertanty * 1 / (self.uncertanty + self.acc_std**2)
        self.angle += self.kalman_gain * (acc_angle - self.angle)
        self.uncertanty *= (1 - self.kalman_gain)
        return self.angle

    def setAngle(self,angle):
        self.angle = angle


    def setUnsertanty(self, a):
        self.unsertanty = a
