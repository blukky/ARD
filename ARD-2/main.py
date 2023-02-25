import yaml
from yaml import Loader
from Gyro_Acse.Gyro import GyroAccel
import time



with open("config.yaml", 'r') as f:
    config = yaml.load(f.read(), Loader=Loader)


GYRO_CONFIG = config.get("gyro")

gyro_accel = GyroAccel(GYRO_CONFIG.get("pin"))

t = time.time()
while True:
    new_t = time.time()
    dt = t - new_t
    t = new_t
    gyro_accel.get_accelerometer_data()
    gyro_accel.get_gyroscope_data(dt)
    time.sleep(1)
