import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
import pigpio #importing GPIO library
from esc.motor import Motor


class ESC:
    max_value = 2000 # надо изменить на значения наших двигателей
    min_value = 1200  # надо изменить на значения наших двигателей



    def __init__(self, pins, lables):
        self.pi = pigpio.pi()
        self.motors = [Motor(l, p, self.pi) for l, p in zip(lables, pins)]

    def calibrate(self):   #Это процедура автоматической калибровки обычного ESC
        for motor in self.motors:
            motor.set_speed(0)
        print("Отсоедините аккумулятор и нажмите Enter")
        inp = input()
        for motor in self.motors:
            motor.set_speed(ESC.max_value)
        print("Подключите аккумулятор СЕЙЧАС .. вы услышите два звуковых сигнала, затем дождитесь постепенного понижения тона, затем нажмите Enter")
        inp = input()
        for motor in self.motors:
            motor.set_speed(ESC.min_value)
        print("Странно, да! Особый тон")
        time.sleep(7)
        print("Дождитесь этого ....")
        time.sleep (5)
        print("Я работаю над этим, НЕ ВОЛНУЙСЯ, ПРОСТО ПОДОЖДИ .....")
        for motor in self.motors:
            motor.set_speed(0)
        time.sleep(2)
        print("Включение ESC сейчас...")
        for motor in self.motors:
            motor.set_speed(ESC.min_value)
        time.sleep(1)
        print("Видишь.... уххххх")


    def control(self, lable, speed):
        speed = max(ESC.min_value + 0.18 * ESC.min_value , min(speed, ESC.max_value - 1))
        for motor in self.motors:
            if motor == lable:
                motor.set_speed(speed)
    def arm(self): #Это процедура постановки на охрану ESC
        arr = [0, ESC.max_value, ESC.min_value]
        for i in arr:
            for motor in self.motors:
                motor.set_speed(i)
            time.sleep(1)

    def stop(self): #Это, конечно, остановит каждое действие, которое ваш Pi выполняет для ESC.
        for motor in self.motors:
            motor.set_speed(0)
        self.pi.stop()

    def set_speed_motor(self, motors):
        for motor in motors:
            self.control(motor, motors[motor])
