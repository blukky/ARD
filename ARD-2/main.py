import yaml
from yaml import Loader
from Gyro_Acse.gyro_thread import MPU6050
import time
from LIDAR.lidar_helper import Lidar
from esc.esc import ESC
import os
from FC.main_flight import MainFlightController
from FC.target import Target

with open("config.yaml", 'r') as f:
    config = yaml.load(f.read(), Loader=Loader)



target = Target()

GYRO_CONFIG = config.get("gyro")
LIDAR_CONFIG = config.get("lidar")
MOTOR_CONFIG = config.get("motor")
PID_CONFIG = config.get("pid")
#PID_CONFIG = {}
#for i in PID_CONFIG_FILE:
#    for key in i.keys():
#        if not key in PID_CONFIG:
#            PID_CONFIG[key] = []
#        PID_CONFIG[key].append(i[key])
print(PID_CONFIG)
mpu = MPU6050(GYRO_CONFIG.get("pin", None))
mpu.start()


lidars = {}
for key, value in LIDAR_CONFIG.items():
    print(key, value)
    lidar = Lidar(value, key)
    lidar.set_sensor()
    lidars[key] = lidar
print(lidars)
time.sleep(4)
motor_pins = list(MOTOR_CONFIG.values())
motor_lable = list(MOTOR_CONFIG.keys())
motor = ESC(motor_pins, motor_lable)
fc = MainFlightController(motor, mpu, lidars, PID_CONFIG, target)
fc.start()
#fc.join()
#motor.arm()
angle = ["pitch", "roll", "yaw"]

while True:
    for i in angle:
        inp = input(f"{i}: ")
    if inp == "q":
        break
    if i == "pitch":
        target.set_pitch(float(inp))
    if i == "roll":
        target.set_roll(float(inp))
    if i == "yaw":
        target.set_yaw(float(inp))
    #print(f"Angle: pitch: {gyro_accel.pitch} roll: {gyro_accel.roll} yaw: {gyro_accel.yaw}\n Speed: x: {gyro_accel.speed_x} y: {gyro_accel.speed_y} z: {gyro_accel.speed_z}")
    #subprocess.run("clear", shell=True)
    #if inp == "q":
    #    break
    #lable, speed = inp.split(" ")
    #motor.control(lable, int(speed))
#motor.stop()
mpu.isStart=False

