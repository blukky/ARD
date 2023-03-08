import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from figure import *
from tkinter import *
from tkinter import ttk
import time
import numpy as np
import board
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gyro_thread import MPU6050
ApplicationGL = False

class PortSettings:
    Name = "COM1"
    Speed = 9600
    Timeout = 2
    pin=0x68
class IMU:
    Roll = 0
    Pitch = 0
    Yaw = 0



myport = PortSettings()
myimu  = IMU()
pose = np.zeros((1,3))
ax = None
def RunAppliction():
    global ApplicationGL
    myport.Name = Port_entry.get()
    myport.Speed = Baud_entry.get()
    ApplicationGL = True
    ConfWindw.destroy()

ConfWindw = Tk()
ConfWindw.title("Configure Serial Port")
ConfWindw.configure(bg = "#2E2D40") 
ConfWindw.geometry('300x150')
ConfWindw.resizable(width=False, height=False)
positionRight = int(ConfWindw.winfo_screenwidth()/2 - 300/2)
positionDown = int(ConfWindw.winfo_screenheight()/2 - 150/2)
ConfWindw.geometry("+{}+{}".format(positionRight, positionDown))

Port_label = Label(text = "Port:",font =("",12),justify= "right",bg = "#2E2D40",fg = "#FFFFFF")
Port_label.place(x = 50, y =30,anchor = "center")
Port_entry = Entry(width = 20,bg = "#37364D", fg = "#FFFFFF", justify = "center")
Port_entry.insert(INSERT,myport.Name)
Port_entry.place(x = 180, y = 30,anchor = "center")

Baud_label = Label(text = "Speed:",font =("",12),justify= "right",bg = "#2E2D40",fg = "#FFFFFF")
Baud_label.place(x = 50, y =80,anchor = "center")
Baud_entry = Entry(width = 20,bg = "#37364D", fg = "#FFFFFF", justify = "center")
Baud_entry.insert(INSERT,str(myport.Speed))
Baud_entry.place(x = 180, y = 80,anchor = "center")

ok_button = Button(text = "Ok",width = 8,command = RunAppliction,bg="#135EF2",fg ="#FFFFFF")
ok_button.place(x = 150, y = 120,anchor="center")

def InitPygame():
    global display
    pygame.init()
    display = (1280,960)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('IMU visualizer   (Press Esc to exit)')


def InitGL():
    glClearColor((1.0/255*46),(1.0/255*45),(1.0/255*64),1)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    gluPerspective(100, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)


def DrawText(textString):     
    font = pygame.font.SysFont ("Courier New",25, True)
    textSurface = font.render(textString, True, (255,255,0), (46,45,64,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)         
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)    


def DrawBoard():
    
    glBegin(GL_QUADS)
    x = 0
    
    for surface in surfaces:
        
        for vertex in surface:  
            glColor3fv((colors[x]))          
            glVertex3fv(vertices[vertex])
        x += 1
    glEnd()

def DrawGL():
    global sensor
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity() 
    gluPerspective(90, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)   

    glRotatef(round(sensor.currentPitch,1), 0, 0, 1)
    glRotatef(round(sensor.currentRoll,1), 1, 0, 0)
    glRotatef(round(sensor.currentYaw, 1), 0, 1, 0)

    DrawText("Roll: {}°    Yaw: {}           Pitch: {}°".format(round(sensor.currentRoll,1), round(sensor.currentYaw, 1), round(sensor.currentPitch,1)))
    DrawBoard()
    pygame.display.flip()

def SerialConnection ():
    global sensor
    sensor = MPU6050()


def animate(i):
    global sensor
    global pose
    #global last_pose
    global ax
    ax.clear()
    ax.scatter(*sensor.pose, s=3)
    print(pose)
    ax.plot(pose[:, 0], pose[:, 1], pose[:, 2])
    pose = np.append(pose, np.expand_dims(sensor.pose, axis=0), axis=0)

def ReadData():
    global sensor
    sensor.run()
    while True:
        pass
def main():
    global sensor
    global ax
    ConfWindw.mainloop()
    if ApplicationGL == True:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        InitPygame()
        InitGL()
            #SerialConnection()
            #myThread1 = threading.Thread(target = ReadData)
            #myThread1.daemon = True
            #myThread1.start()
        sensor = MPU6050()
        sensor.start()
        ani = animation.FuncAnimation(fig, animate, interval=100)
        plt.show()
        while True:
            event = pygame.event.poll()
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                break 

            DrawGL()
            pygame.time.wait(1)
            #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            #DrawText("Sorry, something is wrong :c")
            #pygame.display.flip()
            #time.sleep(5)
        sensor.isStart = False


if __name__ == '__main__': main()
