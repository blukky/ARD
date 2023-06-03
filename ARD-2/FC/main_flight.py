from FC.PID import PID_controller
from threading import Thread
from time import time
from .target import Target


class MainFlightController(Thread):

    def __init__(self, esc,  gyro, lidars, params, target):
        super(MainFlightController, self).__init__()
        self.esc = esc
        self.gyro = gyro
        self.vertical_speed = 0
        self.last_distance = lidars.get("down").get_data()
        self.lidars = lidars # {"front": Lidar, ...}
        self.params = params # {z: [[{k_p, k_i, k_d}, {min, max}], ...], Roll: [...], Pitch: [...], Yaw: [...]}
        self.target = target # {z: , Roll: , Pitch: , Yaw: }
        self.power = {"z":0, "roll": 0, "pitch": 0, "yaw": 0}
        self.isStart = True
    
    #def initializationPID(self):
    #    self.PID = {} # {z: [PID, ...], ...}
    #    for key in self.params:
    #        if not key in self.PID:
    #            self.PID[key] = []
    #        for param in self.params[key]:
    #            self.PID[key].append(PID_controller(param))
    #    print(self.PID)

    def set_target(self, target):
        selt.target = target

    def get_target(self):
        return self.target


    def stop(self):
        self.isStart = False

    def initPID(self):
        self.PID_z = PID_controller(self.params.get("z"))
        self.PID_pitch_rate = PID_controller(self.params.get("pitch"))
        self.PID_roll_rate = PID_controller(self.params.get("roll"))
        self.PID_yaw_rate = PID_controller(self.params.get("yaw"))
        print(self.PID_z, self.PID_pitch_rate, self.PID_roll_rate, self.PID_yaw_rate)


    def run(self):
        self.initPID()
        t = time()
        self.power["z"] = 1600
        while self.isStart:
            #print(self.target)
            dt = time() - t
            t = time()
            gyro_rate = self.gyro.get_gyro_rate()
            self.power["pitch"] = self.PID_pitch_rate.PID(gyro_rate.get("x"), self.target.pitch, dt)
            self.power["roll"] = self.PID_roll_rate.PID(gyro_rate.get("y"), self.target.roll, dt)
            self.power["yaw"] = self.PID_yaw_rate.PID(gyro_rate.get("z"), self.target.yaw, dt)
            #print({"fr": self.power["z"] - self.power["pitch"] - self.power["roll"] - self.power["yaw"],
            #      "br": self.power["z"] + self.power["pitch"] - self.power["roll"] + self.power["yaw"],
            #      "bl": self.power["z"] + self.power["pitch"] + self.power["roll"] - self.power["yaw"],
            #      "fl": self.power["z"] - self.power["pitch"] + self.power["roll"] + self.power["yaw"]
            #    })


        #self.initializationPID()
        #t = time()
        #while self.isStart:
        #    dt = time() - t
        #    t = time()
        #    if self.target is None:
        #        continue
        #    pose = self.lidars.get("down").get_data() / 100
        #    target = self.target.z
        #    for PID in self.PID.get("z"):
        #        target = PID.PID(target, pose, dt)
        #        print(target)
        #        pose = (self.lidars.get("down").get_data() / 100 - self.last_distance) / (dt)
        #    self.last_distance = self.lidars.get("front").get_data() / 100
        #    self.power["z"] = target
        #    pose = self.gyro.currentPitch
        #    target = self.target.pitch
        #    for PID in self.PID.get("pitch"):
        #        target = PID.PID(target, pose, dt)
        #        print(target)
        #        pose = self.gyro.angle_speed.get("x")
        #    self.power["Pitch"] = target
        #    pose = self.gyro.currentRoll
        #    target = self.target.roll
        #    for PID in self.PID.get("roll"):
        #        target = PID.PID(target, pose, dt)
        #        print(target)
        #        pose = self.gyro.angle_speed.get("y")
        #    self.power["Roll"] = target
        #    pose = self.gyro.currentYaw
        #    target = self.target.yaw
        #    self.power["Yaw"] = self.PID.get("yaw")[0].PID(target, pose, dt)
        #    print({"fr": self.power.get("z") + self.power.get("Pitch") - self.power.get("Roll") + self.power.get("Yaw"),
        #                        "fl": self.power.get("z") + self.power.get("Pitch") + self.power.get("Roll") - self.power.get("Yaw"),
        #                        "br": self.power.get("z") - self.power.get("Pitch") - self.power.get("Roll") - self.power.get("Yaw"),
        #                        "bl": self.power.get("z") - self.power.get("Pitch") + self.power.get("Roll") + self.power.get("Yaw")
        #                       })
