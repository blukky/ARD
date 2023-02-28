
import time
import VL53L0X
import RPi.GPIO as GPIO
import subprocess as sp



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Lidar:


    def __init__(self, pin: int, label: str):
        self.pin = pin
        self.label = label
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)


    def set_sensor(self, num:int = None):
        if num is None:
            self.sensor = VL53L0X.VL53L0X(i2c_address=self.pin)
        else:
            self.num = num
            self.sensor = VL53L0X.VL53L0X(i2c_address=num)
        self.sensor.open()
        self.sensor.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)


    def get_data(self):
        distance = self.sensor.get_distance()
        if distance > 0:
            return distance
        return 0

    def close(self):
        self.sensor.stop_ranging()
        self.close()
