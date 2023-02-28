

class Motor:


    def __init__(self, label, pin, pi):
        self.pin = pin
        self.label = label
        self.pi = pi


    def set_speed(self, speed):
        self.pi.set_servo_pulsewidth(self.pin, speed)
        print(f"{self.label} gpio: {self.pin} speed: {speed}")

    def __eq__(self, other):
        if type(other) == int:
            return self.pin == other
        if type(other) == str:
            return self.label == other
