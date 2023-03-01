from mpu6050 import mpu6050





class GyroAccel:
    def __init__(self, pin: int):
        self.sensor = mpu6050(pin)
        self.accelerometer_data = None
        self.gyroscope_data = None
        self.dgrees = {"x": 0, "y": 0, "z": 0}

    def get_accelerometer_data(self):
        self.accelerometer_data = self.sensor.get_accel_data(g=True)
        print("ACCEL:", self.accelerometer_data)

    def get_gyroscope_data(self, dt):
        self.gyroscope_data = self.sensor.get_gyro_data()
        print("GYRO:", self.gyroscope_data)
        diff_dgrees = {key: value * dt for key, value in self.gyroscope_data.items()}
        self.dgrees = {key: value + diff_dgrees[key] for key, value in self.dgrees.items()}
        print("DGREES:", self.dgrees)
