
# Author: Darya Clark
# Purpose: This program controls the two lead screw stepper motors of the 
# REEKON 2 shaft cutting device. When called, it sets up the two motors and 
# lowers the dremel and activates its cutting feature

import RPi.GPIO as GPIO 
import time 
import relay

# declare pin values 
pin1 = 11
pin2 = 12
pin3 = 13 
pin4 = 15

# values associated with speed and step count to move lead screws 
NON_CUTTING = 0.001
STEP_DELAY = .05
FASTSTEPS3 = 250
FASTSTEPS6 = 400
SLOWSTEPS3 = 20
SLOWSTEPS6 = 15
REPEAT3 = 30
REPEAT6 = 75
CUTDELAY3 = 20
CUTDELAY6 = 30

"""
name: piSetup
parameters: none
goal: setup associated pins on Pi
"""
def piSetup():
    # makes pin an output 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)

"""
name: posZ
parameters: integer representing steps to move
goal: move lead screw stepper in the positive z direction
"""
def posZ(stepCount: int):
    for x in range(0, stepCount):
        step(1, 0, 0, 0)
        step(0, 0, 1, 0)
        step(0, 1, 0, 0)
        step(0, 0, 0, 1)
        step(0, 0, 0, 0)

"""
name: negZ
parameters: integer representing steps to move
goal: move lead screw stepper in the negative z direction
"""
def negZ(stepCount: int):
    for x in range(0, stepCount):
        step(0, 0, 0, 0)
        step(0, 0, 0, 1)
        step(0, 1, 0, 0)
        step(0, 0, 1, 0)
        step(1, 0, 0, 0)

"""
name: step
parameters: integers representing the pin numbers
goal: move lead screw stepper in the positive z direction
"""
def step(p1: int, p2: int, p3: int , p4: int):
    GPIO.output(pin1, p1)
    GPIO.output(pin2, p2)
    GPIO.output(pin3, p3)
    GPIO.output(pin4, p4)
    time.sleep(STEP_DELAY)

"""
name: negFastZ
parameters: integer representing steps to move
goal: move lead screw stepper in the negative z direction faster
"""
def negZFast(stepCount: int):
    for x in range(0, stepCount):
        stepFast(0, 0, 0, 0)
        stepFast(0, 0, 0, 1)
        stepFast(0, 1, 0, 0)
        stepFast(0, 0, 1, 0)
        stepFast(1, 0, 0, 0)

"""
name: posZFast
parameters: integer representing steps to move
goal: move lead screw stepper in the positive z direction faster
"""
def posZFast(stepCount: int):
    for x in range(0, stepCount):
        stepFast(1, 0, 0, 0)
        stepFast(0, 0, 1, 0)
        stepFast(0, 1, 0, 0)
        stepFast(0, 0, 0, 1)
        stepFast(0, 0, 0, 0)
"""
name: step
parameters: integers representing the pin numbers
goal: move lead screw stepper in the positive z direction
"""
def stepFast(p1: int, p2: int, p3: int , p4: int):
    GPIO.output(pin1, p1)
    GPIO.output(pin2, p2)
    GPIO.output(pin3, p3)
    GPIO.output(pin4, p4)
    time.sleep(NON_CUTTING)

"""
name: lowerAndCut
parameters: integer representing diameter of the rod
goal: lower the dremel using lead screws, activate cutting, and drive through
      rod
"""
def lowerAndCut(diameter: int):
    
    piSetup()
    
    if diameter == 3:
        # move halfway down then turn on dremel
        negZFast(int(FASTSTEPS3*.5))
        relay.turnOnDremel()
        time.sleep(1)
        negZFast(int(FASTSTEPS3*.5))
        
        # times to repeat step count lowering
        for i in range(REPEAT3):
            negZ(SLOWSTEPS3)
            time.sleep(CUTDELAY3)

    elif diameter == 6:
        # move halfway down then turn on dremel
        negZFast(int(FASTSTEPS6*.5))
        relay.turnOnDremel()
        time.sleep(1)
        negZFast(int(FASTSTEPS6*.5))
        
        # times to repeat step count lowering
        for i in range(REPEAT6):
            negZ(SLOWSTEPS6)
            time.sleep(CUTDELAY6)

    
    # turn off dremel 
    relay.turnOffDremel()
    # cleanup all pins 
    GPIO.cleanup()

"""
name: raise dremel
parameters: integer representing diameter of the rod
goal: raise dremel based on amount lowered
"""
def raiseDremel(diameter: int):
    piSetup()
    # added accounts for amount in slow steps
    if diameter == 3:
        posZFast(FASTSTEPS3+10)
    else:
        posZFast(FASTSTEPS6+20)
    GPIO.cleanup() 



