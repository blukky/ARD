import yaml
from yaml import Loader
from Gyro_Acse.Gyro import GyroAccel
import time
from LIDAR.lidar_helper import Lidar
from pynput import keyboard
from esc.esc import ESC
import os
#os.system("sudo pigpiod")
#time.sleep(1)
#def close_lidar(key):
#    if key == keyboard.Key.esc:
#        for lidar in lidars:
#            lidar.close()


with open("config.yaml", 'r') as f:
    config = yaml.load(f.read(), Loader=Loader)


GYRO_CONFIG = config.get("gyro")
LIDAR_CONFIG = config.get("lidar")
MOTOR_CONFIG = config.get("motor")
gyro_accel = GyroAccel(GYRO_CONFIG.get("pin"))

#lidars = []
#for key, value in LIDAR_CONFIG.items():
#    print(key, value)
#    lidar = Lidar(value, key)
#    lidar.set_sensor()
#    lidars.append(lidar)


#t = time.time()
#while True:
    #with keyboard.Listener(on_release=close_lidar) as listener:
    #    for lidar in lidars:
    #        dist = lidar.get_data()
    #        print(f"{lidar.label}: {dist} mm")

motor_pins = list(MOTOR_CONFIG.values())
motor_lable = list(MOTOR_CONFIG.keys())
motor = ESC(motor_pins, motor_lable)
motor.arm()
while True:
    inp = input()
    if inp == "q":
        break
    lable, speed = inp.split(" ")
    motor.control(lable, int(speed))
motor.stop()
