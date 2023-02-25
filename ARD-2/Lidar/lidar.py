#!/usr/bin/python

import time
import VL53L0X
import RPi.GPIO as GPIO
import subprocess as sp

# GPIO for Sensor 1 shutdown pin
# sensor1_shutdown = 20
# GPIO for Sensor 2 shutdown pin
# sensor2_shutdown = 16
GPIO_SENSORS = [25, 14, 18, 22, 23, 27, 17, 4, 24, 5]
ORIENTATION = ["FRONT", "FRONT RIGHT", "RIGHT", "BACK RIGHT", "BACK", "BACK LEFT", "LEFT", "FRONT LEFT", "UP", "DOWN"]
GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
for i in GPIO_SENSORS:
    if not i is None:
        GPIO.setup(i, GPIO.OUT)
# GPIO.setup(sensor2_shutdown, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
for i in GPIO_SENSORS:
    if not i is None:
        GPIO.output(i, GPIO.LOW)
# GPIO.output(sensor2_shutdown, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)
COUNT_SENSOR = 10
# Create one object per VL53L0X passing the address to give to
# each.
SENSORS = list()
start_address = 0x40
for i in range(COUNT_SENSOR):
    SENSORS.append(VL53L0X.VL53L0X(address=(start_address + i)))
    #print(hex(start_address + i))
    #SENSORS[-1].open()
    #tof.open()
    #SENSORS.append(tof)
    #print(sp.run("i2cdetect -y 1", shell=True))


#SENSORS[0].start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE) Set 
# shutdown pin high for the first VL53L0X then call to start ranging
for ind, i in enumerate(GPIO_SENSORS, start=0):
    print(ind)
    if not i is None:
        GPIO.output(i, GPIO.HIGH)
        time.sleep(1)
        SENSORS[ind].start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        #print(sp.run("i2cdetect -y 1", shell=True))
# Set shutdown pin high for the second VL53L0X then 
# call to start ranging 
# GPIO.output(sensor2_shutdown, GPIO.HIGH)
# time.sleep(0.50)
# tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = SENSORS[0].get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing / 1000))

for count in range(1, 101):
    for ind, i in enumerate(SENSORS):
        distance = i.get_distance()
        if distance > 0:
            print(f"sensor {ORIENTATION[ind]} - {distance} mm, {(distance / 10)} cm, iteration {count}")
        else:
            print("%s - Error" % ORIENTATION[ind])
    print("-"*10)
    time.sleep(5)
    # distance = tof1.get_distance()
    # if distance > 0:
    #     print("sensor %d - %d mm, %d cm, iteration %d" % (2, distance, (distance / 10), count))
    # else:
    #     print("%d - Error" % 2)
    #
    # time.sleep(timing / 1000000.00)

for i in SENSORS:
    i.stop_ranging()
for i in GPIO_SENSORS:
    GPIO.output(i, GPIO.LOW)
#for i in SENSORS:
#    i.close()
