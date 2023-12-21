
# Author: Darya Clark
# Purpose: This program activates the DC feed in motor of the REEKON 2 shaft
# cutting device. When called, the DC motor turns on and feeds in the rod 
# based on the number of steps the measuring motor has moved


import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)


# assocaited pins 
in1 = 21
in2 = 23
en = 32

"""
name: setUpDC
parameters: integer representing diameter of the shaft
goal: setup motor to be run, setting speed based on the diameter of the shaft
"""
def setupDC(dia: int):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)

    GPIO.setup(en, GPIO.OUT)

    p = GPIO.PWM(en, 1000)
    # set speed faster if shaft is thinner
    if dia == 3:
        p.start(80)
    else: 
        p.start(70)
    return p

"""
name: backwardSetup
parameters: none
goal: turn on the dc motor backwards
"""
def backwardSetup():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)

"""
name: forwardSetup()
parameters: none
goal: turn on the dc motor forwards 
"""
def forwardSetup():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)

"""
name: allOff
parameters: none
goal: turn dc motor completely off 
"""
def allOff():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)

"""
name: runMotor
parameters: integers representing step count and diameter
goal: 
"""
def runMotor(step: int, dia: int):

    p = setupDC(dia)
    timer = step * (1/47.3)
    forwardSetup()
    time.sleep(timer)
    p.stop()
    GPIO.cleanup()


    


