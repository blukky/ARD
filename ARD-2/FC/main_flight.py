from FC.PID import PID_controller
from threading import Thread
from time import time

class MainFlightController(Thread):

    def __init__(self, esc,  gyro, lidars, params, target):
        self.esc = esc
        self.gyro = gyro
        self.lidars = lidars # {"front": Lidar, ...}
        self.params = params # {z: [[{k_p, k_i, k_d}, {min, max}], ...], Roll: [...], Pitch: [...], Yaw: []}
        self.target = target # {z: , Roll: , Pitch: , Yaw: }
        self.results = None
        self.power = {"z":0, "Roll": 0, "Pitch": 0, "Yaw": 0}

    def initializationPID(self):
        self.PID = {}
        self.results = {}
        for key in self.params:
            if not key in self.PID:
                self.PID[key] = []
                self.results[key] = []
            for param in self.params[key]:
                self .results[key].append(0)
                self.PID[key].append(PID_controller(*param))

    def set_target(self, target):
        selt.target = target

    def get_target(self):
        return self.target

    def run(self):
        t =time()
        while True:
            if not self.target is None:
                continue
            pose = self.lidars.get("front").get_data()
            target = self.target.get("z")
            for PID in self.PID.get("z"):
                dt = time() - t
                target = PID.PID(target, pose, dt)
                pose = self.gyro.accel_data[i]
            self.power["z"] = target
            pose = self.gyro.get_pitch()
            target = self.target.get("Pitch")
            for PID in self.PID.get("Pitch"):
                dt = time() - t
                target = PID.PID(target, pose, dt)
                pose = self.gyro.get_gyro_data().get("x") # I don't know
            self.power["Pitch"] = target
            pose = self.gyro.get_roll()
            target = self.target.get("Roll")
            for PID in self.PID.get("Roll"):
                dt = time() - t
                target = PID.PID(target, pose, dt)
                pose = self.gyro.get_gyro_data().get("y") # I don't know
            self.power["Roll"] = target
            pose = self.gyro.get_gyro_data().get("z")
            target = self.target.get("Yaw")
            dt = time() - t
            self.power["Yaw"] = self.PID.get("Yaw")[0].PID(target, pose, dt)
            self.esc.set_speed({"fr": self.power.get("z") + self.power("...") + self.power.get("...") + self.power.get("..."),
                                "fl": self.power.get("z") + 
                                "br": ...
                                "bl": ...})
            t = time()
