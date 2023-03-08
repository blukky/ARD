

class Target:

    def __init__(self, z=None, roll=None, pitch=None, yaw=None):
        self.z = z if z else 0
        self.roll = roll if roll else 0
        self.pitch = pitch if pitch else 0
        self.yaw = yaw if yaw else 0

    def __str__ (self):
        return f"z: {self.z} roll: {self.roll} pitch: {self.pitch} yaw: {self.yaw}"

    def get_z(self):
        return self.z

    def get_roll(self):
        return self.roll

    def get_pitch(self):
        return self.pitch

    def get_yaw(self):
        return self.yaw

    def set_z(self, z):
        self.z = z

    def set_roll(self, r):
        self.roll = r

    def set_pitch(self, p):
        self.pitch = p

    def set_yaw(self, y):
        self.yaw = y


    def set_target(self, z, r, p, y):
        self.z = z
        self.roll = r
        self.pitch = p
        self.yaw = y
