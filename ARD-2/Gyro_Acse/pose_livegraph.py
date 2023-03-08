#!/home/drone/Desktop/ARD/venv/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gyro_thread import MPU6050
from time import time








fig = plt.figure()
ax = fig.add_subplot()
#pose = np.zeros((1,3))
mpu = MPU6050()
mpu.start()
xarr = []
gyro = []
acc = []
#pose = []

t = time()
def change_pose(i):
    global t
    dt = time() - t
    t = time()
    global pose
    ax.clear()
    xarr.append(i)
    acc.append(mpu.currentPitch)
    gyro.append(mpu.currentRoll)
    #acc.append(mpu.linAcc[0])
    #vel.append(mpu.velocity[0])
    #pose.append(mpu.pose[0])
    #ax.scatter(mpu.pose, s=10)
    ax.plot(xarr, acc, c="r", label="pitch")
    ax.plot(xarr, gyro, c="g", label="roll")
    #ax.plot(xarr, pose, c="b", label="pose")
    ax.legend()
    #pose = np.append(pose, np.expand_dims(mpu.pose, axis=0), axis=0)




ani = animation.FuncAnimation(fig, change_pose, interval=1)
plt.show()

mpu.isStart = False
