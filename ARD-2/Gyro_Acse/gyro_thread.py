#Connections
#MPU6050 - Raspberry pi
#VCC - 5V  (2 or 4 Board)
#GND - GND (6 - Board)
#SCL - SCL (5 - Board)
#SDA - SDA (3 - Board)


#from .Kalman import KalmanAngle
import smbus			#import SMBus module of I2C
import time
import math
from threading import Thread
import numpy as np
from math import sin, cos, radians, degrees
from .Kalman import KalmanAngle

class MPU6050(Thread):
    PWR_MGMT_1   = 0x6B
    SMPLRT_DIV   = 0x19
    CONFIG       = 0x1A
    GYRO_CONFIG  = 0x1B # FS_SEL
    ACCEL_CONFIG = 0x1C # AFS_SEL
    INT_ENABLE   = 0x38
    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D
    ACCEL_ZOUT_H = 0x3F
    GYRO_XOUT_H  = 0x43
    GYRO_YOUT_H  = 0x45
    GYRO_ZOUT_H  = 0x47

    #radToDeg = 180 / math.pi


    def __init__(self, pin: int = None):
        super(MPU6050, self).__init__()
        self.pin = pin if not pin is None else 0x68
        self.bus = smbus.SMBus(1)
        #self.kalmanX = KalmanAngle()
        #self.kalmanY = KalmanAngle()

        self.RestrictPitch = False	#Comment out to restrict roll to ±90deg instead - please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf
        self.currentPitch = 0
        self.currentRoll = 0
        self.currentYaw = 0
        self.kalmanPitch = KalmanAngle()
        self.kalmanRoll = KalmanAngle()
        while True:
            try:
                self.init_settings()
                break
            except:
                print("ERROR READING DATA")



        self.errorAccelPitch = 0.8
        self.errorAccelRoll = -0.8
        self.errorAccelYaw = 0
        self.errorGyroPitch = 0
        self.errorGyroRoll = 0
        self.errorGyroYaw = 0
        self.errorAccel = np.zeros(3)#np.array([-0.72, 0.11, 1.14])
        self.linAcc = np.zeros(3)
        self.velocity = np.zeros(3)
        self.pose = np.zeros(3)
        #self.errorYaw = 0
        self.isStart = True

    def init_settings(self):
        #write to sample rate register
        self.bus.write_byte_data(self.pin, MPU6050.SMPLRT_DIV, 7)

        #Write to power management register
        self.bus.write_byte_data(self.pin, MPU6050.PWR_MGMT_1, 1)

	#Write to Configuration register
	#Setting DLPF (last three bit of 0X1A to 6 i.e '110' It removes the noise due to vibration.) https://ulrichbuschbaum.wordpress.com/2015/01/18/using-the-mpu6050s-dlpf/
        self.bus.write_byte_data(self.pin, MPU6050.CONFIG, int('0000110',2))

	#Write to Gyro configuration register
        self.bus.write_byte_data(self.pin, MPU6050.GYRO_CONFIG, 1 << 3)
        self.bus.write_byte_data(self.pin, MPU6050.ACCEL_CONFIG, 2 << 3)
        #print(self.bus.read_byte_data(self.pin, MPU6050.GYRO_CONFIG))
	#Write to interrupt enable register
        self.bus.write_byte_data(self.pin, MPU6050.INT_ENABLE, 1)

    def read_raw_data(self, addr):
	#Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(self.pin, addr)
        low = self.bus.read_byte_data(self.pin, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

    def dist(self,a, b, c):
        return math.sqrt(a**2 + b**2 + c**2)


    def currect_angle(self, angle,  x, z):
        if x < 0 and z < 0:
            angle = -180 - angle
        if x > 0 and z < 0:
            angle = 180 - angle
        return angle

    def calcAngle(self, accX, accY, accZ):
        u_line = self.dist(accX, accY, accZ)
        if u_line == 0:
            pitch = 0
            roll = 0
        else:
            pitch = math.degrees(math.asin(accY / u_line))
            roll = math.degrees(math.asin(-accX / u_line))
        return pitch, roll


    def get_accelerometer_data(self):
        accX = self.read_raw_data(MPU6050.ACCEL_XOUT_H)
        accY = self.read_raw_data(MPU6050.ACCEL_YOUT_H)
        accZ = self.read_raw_data(MPU6050.ACCEL_ZOUT_H)
        self.acc = np.array([accX, accY, accZ]) / 4096
        return {"accX": accX / 4096, "accY": accY / 4096, "accZ": accZ / 4096}


    def get_gyroscope_data(self):
        gyroX = self.read_raw_data(MPU6050.GYRO_XOUT_H)
        gyroY = self.read_raw_data(MPU6050.GYRO_YOUT_H)
        gyroZ = self.read_raw_data(MPU6050.GYRO_ZOUT_H)
        return {"gyroX": gyroX, "gyroY": gyroY, "gyroZ": gyroZ}

    def calibrateAccel(self, iter):
        for i in range(iter):
            self.get_accelerometer_data()
            self.get_R()
            tcAcc = self.R.T @ self.acc.T
            self.errorAccel += (tcAcc - [0, 0, 1]) * 9.81
        self.errorAccel /= iter



    def calibrateGyro(self, iter):
        for i in range(iter):
            gyro = self.get_gyroscope_data()
            self.errorGyroPitch += gyro.get("gyroX") / 65.5
            self.errorGyroRoll += gyro.get("gyroY") / 65.5
            self.errorGyroYaw += gyro.get("gyroZ") / 65.5
        self.errorGyroPitch /= iter
        self.errorGyroRoll /= iter
        self.errorGyroYaw /= iter


    def calcAngleAccel(self):
        accel = self.get_accelerometer_data()
        pitch, roll = self.calcAngle(**accel)
        accel_pitch = pitch - self.errorAccelPitch
        accel_roll = roll - self.errorAccelRoll
        #print("Accel Angle:", accel_pitch, accel_roll)
        return accel_pitch, accel_roll


    def get_gyro_rate(self, gyro=None):
        if gyro is None:
            gyro = self.get_gyroscope_data()
        gyro_pitch = gyro.get("gyroX") / 65.5 - self.errorGyroPitch
        gyro_roll = gyro.get("gyroY") / 65.5 - self.errorGyroRoll
        gyro_yaw = gyro.get("gyroZ") / 65.5 - self.errorGyroYaw
        #self.gyro_rate = {"x": gyro_pitch, "y": gyro_roll, "z": gyro_yaw}
        return {"x": gyro_pitch , "y": gyro_roll , "z": gyro_yaw }



    def calc_current_angle_by_gyro(self, gyro, dt):
        self.newCurrentPitch += gyro.get("x") * dt
        self.newCurrentRoll +=  gyro.get("y") * dt
        self.newCurrentYaw += gyro.get("z") * dt
        self.newCurrentPitch += self.newCurrentRoll * math.sin(math.radians(gyro.get("z") * dt))
        self.newCurrentRoll -= self.newCurrentPitch * math.sin(math.radians(gyro.get("z") * dt))

    def calcAngleGyro(self, dt):
        gyro = self.get_gyroscope_data()
        gyro_rate = self.get_gyro_rate(gyro)
        self.calc_current_angle_by_gyro(gyro_rate, dt)
        return self.newCurrentPitch


    def calc_current_angle(self):
        self.currentPitch = 0.9 * self.currentPitch +  0.1 * self.newCurrentPitch
        self.currentRoll =  0.9 * self.currentRoll + 0.1 * self.newCurrentRoll
        self.currentYaw = 0.9 * self.currentYaw + 0.1 * self.newCurrentYaw


    def initRun(self):
        self.calibrateGyro(1000)
        #self.calibrateAccel(1000)
        self.newCurrentPitch, self.newCurrentRoll = self.calcAngleAccel()
        self.kalmanPitch.setAngle(self.newCurrentPitch)
        self.kalmanRoll.setAngle(self.newCurrentRoll)
        self.newCurrentYaw = 0
        self.calc_current_angle()

    def calc_new_currect_angle(self, pitch_acc, roll_acc):
        self.newCurrentPitch = 0.99 * self.newCurrentPitch + 0.01 * pitch_acc
        self.newCurrentRoll = 0.99 * self.newCurrentRoll + 0.01 * roll_acc
        #self.newCurrentYaw = 0.99 * self.newCurrentYaw


    def my_cos(self, a):
        return cos(radians(a))

    def my_sin(self, a):
        return sin(radians(a))


    def get_R(self):
        self.R = np.array([[self.my_cos(self.currentYaw) * self.my_cos(self.currentRoll), -1 * self.my_sin(self.currentPitch) * self.my_cos(self.currentYaw) + self.my_cos(self.currentYaw) * self.my_sin(self.currentRoll) * self.my_sin(self.currentPitch), self.my_sin(self.currentYaw) * self.my_sin(self.currentPitch) + self.my_cos(self.currentYaw) * self.my_sin(self.currentRoll) * self.my_cos(self.currentPitch)],
                           [self.my_sin(self.currentYaw) * self.my_cos(self.currentRoll), self.my_cos(self.currentYaw) * self.my_cos(self.currentPitch) + self.my_sin(self.currentYaw) * self.my_sin(self.currentRoll) * self.my_sin(self.currentPitch), -1 * self.my_cos(self.currentYaw) * self.my_sin(self.currentPitch) + self.my_sin(self.currentYaw) * self.my_sin(self.currentRoll) * self.my_cos(self.currentPitch)],
                           [-1 * self.my_sin(self.currentRoll), self.my_cos(self.currentRoll) * self.my_sin(self.currentPitch), self.my_cos(self.currentRoll) * self.my_cos(self.currentPitch)]
                          ])


    #def calc_velocity(self, dt):
    #    self.get_R()
    #    #print(self.R)
    #    tcAcc = self.R @ self.acc.T
    #    self.linAcc = np.around((tcAcc - [0, 0, 1]) * 9.81 - self.errorAccel, 2)
    #    #print("acc:", self.linAcc[0])
    #    self.velocity = 0.9 * self.velocity + 0.1 *  np.around((self.velocity + self.linAcc * dt), 2)
    #    #print("vel:", self.velocity[0])
    #    self.pose = 0.9 * self.pose + 0.1 * np.around((self.pose + self.velocity * dt), 2)
    #   #print("pose:", self.pose[0])

    def run(self):
        self.initRun()
        timer = time.time()
        print("-"*100)
        while self.isStart:
            #try:
            dt = time.time() - timer
            #print(dt)
            timer = time.time()
            gyro = self.get_gyroscope_data()
            gyro_rate = self.get_gyro_rate(gyro)
            #self.calcAngleGyro(dt)
            accel_pitch, accel_roll = self.calcAngleAccel()
            self.currentPitch = self.kalmanPitch.getAngle(accel_pitch, gyro_rate.get("x"), dt)
            self.currentRoll = self.kalmanRoll.getAngle(accel_roll, gyro_rate.get("y"), dt)
            #self.calc_new_currect_angle(accel_pitch, accel_roll)
            #self.calc_current_angle()
            #self.calc_velocity(dt)
            time.sleep(0.005)






                #self.currentPitch = pitch
                #self.currentRoll = roll
                #if (self.RestrictPitch):
                #if((pitch < -90 and self.currentPitch > 90) or (pitch > 90 and self.currentPitch < -90)):
                #    self.kalmanX.setAngle(pitch)
                #    complAngleX = pitch
                #    self.currentPitch = pitch
                #    #gyroXAngle = pitch
                #else:
                #self.currentPitch = self.kalmanX.getAngle(self.currentPitch,gyroXRate,dt)
                #if(abs(self.currentRoll)>90):
                #    gyroYRate  = -gyroYRate
                #    self.currentRoll  = self.kalmanY.getAngle(roll,gyroYRate,dt)
                #else:
                #if((roll < -90 and self.currentRoll > 90) or (roll > 90 and self.currentRoll < -90)):
                #    self.kalmanY.setAngle(roll)
                #    complAngleY = roll
                #    self.currentRoll   = roll
                #    #gyroYAngle  = roll
                #else:
                #self.currentRoll = self.kalmanY.getAngle(roll,gyroYRate,dt)
                #if(abs(self.currentPitch)>90):
                #    gyroXRate  = -gyroXRate
                #    self.currentPitch = self.kalmanX.getAngle(pitch,gyroXRate,dt)

		#angle = (rate of change of angle) * change in time
                #gyroXAngle = gyroXRate * dt
                #gyroYAngle = gyroYRate * dt

		#compAngle = constant * (old_compAngle + angle_obtained_from_gyro) + constant * angle_obtained from accelerometer
                #compAngleX = 0.99 * (compAngleX + gyroXRate * dt) + 0.01 * pitch
                #compAngleY = 0.99 * (compAngleY + gyroYRate * dt) + 0.01 * roll
                #if ((gyroXAngle < -180) or (gyroXAngle > 180)):
                #    gyroXAngle = self.currentPitch
                #if ((gyroYAngle < -180) or (gyroYAngle > 180)):
                #    gyroYAngle = self.currentRoll
                #print(compAngleX, compAngleY)
                #print("Angle X: " + str(self.currentPitch)+"   " +"Angle Y: " + str(self.currentRoll))
	        #print(str(roll)+"  "+str(gyroXAngle)+"  "+str(compAngleX)+"  "+str(kalAngleX)+"  "+str(pitch)+"  "+str(gyroYAngle)+"  "+str(compAngleY)+"  "+str(kalAngleY))
            #except:
            #    print("ERROR")
