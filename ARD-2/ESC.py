# This program will let you test your ESC and brushless motor.
# Make sure your battery is not connected if you are going to calibrate it at first.
# Since you are testing your motor, I hope you don't have your propeller attached to it otherwise you are in trouble my friend...?
# This program is made by AGT @instructable.com. DO NOT REPUBLISH THIS PROGRAM... actually the program itself is harmful                                             pssst Its not, its safe.

import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
# os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library

motor_gpio_1 = 4  #Connect the ESC in this GPIO pin
motor_gpio_2 = 5  #Connect the ESC in this GPIO pin
motor_gpio_3 = 6  #Connect the ESC in this GPIO pin
motor_gpio_4 = 7  #Connect the ESC in this GPIO pin

pi = pigpio.pi()
pi.set_servo_pulsewidth(motor_gpio_1, 0)
pi.set_servo_pulsewidth(motor_gpio_2, 0)
pi.set_servo_pulsewidth(motor_gpio_3, 0)
pi.set_servo_pulsewidth(motor_gpio_4, 0)

max_value = 2000 # надо изменить на значения наших двигателей
min_value = 700  # надо изменить на значения наших двигателей
print("Для первого запуска выберите калибровать\n Введите точное слово для нужной функции\n")

def manual_drive(): #Вы будете использовать эту функцию для программирования вашего ESC, если потребуется
    print("Вы выбрали ручной вариант, поэтому укажите значение от 0 до вашего максимального значения")
    while True:
        inp = input()
        if inp == "stop":
            stop()
            break
        elif inp == "control":
            control()
            break
        elif inp == "arm":
            arm()
            break
        else:
            pi.set_servo_pulsewidth(motor_gpio_1, int(inp))
            pi.set_servo_pulsewidth(motor_gpio_2, int(inp))
            pi.set_servo_pulsewidth(motor_gpio_3, int(inp))
            pi.set_servo_pulsewidth(motor_gpio_4, int(inp))
                
def calibrate():   #Это процедура автоматической калибровки обычного ESC
    pi.set_servo_pulsewidth(motor_gpio_1, 0)
    pi.set_servo_pulsewidth(motor_gpio_2, 0)
    pi.set_servo_pulsewidth(motor_gpio_3, 0)
    pi.set_servo_pulsewidth(motor_gpio_4, 0)
    print("Отсоедините аккумулятор и нажмите Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(motor_gpio_1, max_value)
        pi.set_servo_pulsewidth(motor_gpio_2, max_value)
        pi.set_servo_pulsewidth(motor_gpio_3, max_value)
        pi.set_servo_pulsewidth(motor_gpio_4, max_value)
        print("Подключите аккумулятор СЕЙЧАС .. вы услышите два звуковых сигнала, затем дождитесь постепенного понижения тона, затем нажмите Enter")
        inp = input()
        if inp == '':            
            pi.set_servo_pulsewidth(motor_gpio_1, min_value)
            pi.set_servo_pulsewidth(motor_gpio_2, min_value)
            pi.set_servo_pulsewidth(motor_gpio_3, min_value)
            pi.set_servo_pulsewidth(motor_gpio_4, min_value)
            print("Странно, да! Особый тон")
            time.sleep(7)
            print("Дождитесь этого ....")
            time.sleep (5)
            print("Я работаю над этим, НЕ ВОЛНУЙСЯ, ПРОСТО ПОДОЖДИ .....")
            pi.set_servo_pulsewidth(motor_gpio_1, 0)
            pi.set_servo_pulsewidth(motor_gpio_2, 0)
            pi.set_servo_pulsewidth(motor_gpio_3, 0)
            pi.set_servo_pulsewidth(motor_gpio_4, 0)
            time.sleep(2)
            print("Включение ESC сейчас...")
            pi.set_servo_pulsewidth(motor_gpio_1, min_value)
            pi.set_servo_pulsewidth(motor_gpio_2, min_value)
            pi.set_servo_pulsewidth(motor_gpio_3, min_value)
            pi.set_servo_pulsewidth(motor_gpio_4, min_value)
            time.sleep(1)
            print("Видишь.... уххххх")
            control() # Вы можете изменить это на любую другую функцию, которую захотите
            
def control(): 
    print("Я запускаю двигатель, надеюсь, он откалиброван и включен, если не перезапустить, нажав 'x'")
    time.sleep(1)
    speed = 1500    # change your speed if you want to.... it should be between 700 - 2000
    print("Элементы управления - a для уменьшения скорости и d для увеличения скорости ИЛИ q для значительного уменьшения скорости и e для значительного увеличения скорости")
    while True:
        pi.set_servo_pulsewidth(motor_gpio_1, speed)
        pi.set_servo_pulsewidth(motor_gpio_2, speed)
        pi.set_servo_pulsewidth(motor_gpio_3, speed)
        pi.set_servo_pulsewidth(motor_gpio_4, speed)
        inp = input()
        if inp == "q":
            speed -= 100    # decrementing the speed like hell
            print ("speed = %d" % speed)
        elif inp == "e":    
            speed += 100    # incrementing the speed like hell
            print("speed = %d" % speed)
        elif inp == "d":
            speed += 10     # incrementing the speed 
            print("speed = %d" % speed)
        elif inp == "a":
            speed -= 10     # decrementing the speed
            print("speed = %d" % speed)
        elif inp == "stop":
            stop()          #going for the stop function
            break
        elif inp == "manual":
            manual_drive()
            break
        elif inp == "arm":
            arm()
            break
        else:
            print("ЧТО ТЫ ТАКОЕ СКАЗАЛ!! Нажмите a, q, d или e")
            
def arm(): #Это процедура постановки на охрану ESC
    print("Подключите аккумулятор и нажмите Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(motor_gpio_1, 0)
        pi.set_servo_pulsewidth(motor_gpio_2, 0)
        pi.set_servo_pulsewidth(motor_gpio_3, 0)
        pi.set_servo_pulsewidth(motor_gpio_4, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(motor_gpio_1, max_value)
        pi.set_servo_pulsewidth(motor_gpio_2, max_value)
        pi.set_servo_pulsewidth(motor_gpio_3, max_value)
        pi.set_servo_pulsewidth(motor_gpio_4, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(motor_gpio_1, min_value)
        pi.set_servo_pulsewidth(motor_gpio_2, min_value)
        pi.set_servo_pulsewidth(motor_gpio_3, min_value)
        pi.set_servo_pulsewidth(motor_gpio_4, min_value)
        time.sleep(1)
        control() 
        
def stop(): #Это, конечно, остановит каждое действие, которое ваш Pi выполняет для ESC.
    pi.set_servo_pulsewidth(motor_gpio_1, 0)
    pi.set_servo_pulsewidth(motor_gpio_2, 0)
    pi.set_servo_pulsewidth(motor_gpio_3, 0)
    pi.set_servo_pulsewidth(motor_gpio_4, 0)
    pi.stop()

#На самом деле это запуск программы, чтобы запустить функцию, ее нужно инициализировать перед вызовом ... глупый python.
inp = input()
if inp == "manual":
    manual_drive()
elif inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else :
    print("Спасибо Вам за то, что вы не следите за тем, что я говорю... теперь ты должен перезапустить программу, ДЭБИЛ!!")
