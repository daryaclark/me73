
# Author: Darya Clark
# Purpose: This program handles the measuring belt system of the REEKON 2
# shaft cutting device driven by a stepper motor

import RPi.GPIO as GPIO 
import time 


# declare pin values 
pin1, pin2, pin3, pin4 = 16, 18, 22, 24

# calculated values associated with measuring
STEP_DELAY = 0.01
MM_PER_STEP = .0117
IN_PER_STEP = .065
CM_PER_STEP = .117

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
name: posY
parameters: integer representing steps to move
goal: move stepper in the positive y direction
"""
def posY(stepCount: int):
    for x in range(0, stepCount):
        step(1, 0, 0, 0)
        step(0, 0, 1, 0)
        step(0, 1, 0, 0)
        step(0, 0, 0, 1)
        step(0, 0, 0, 0)

"""
name: negY
parameters: integer representing steps to move
goal: move stepper in the negative y direction
"""
def negY(stepCount: int):
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
name: measureDistance
parameters: integers representing the original length of the rod, the cut size
            and the unit used to measure
goal: move the belt system according to distance provided 
returns: integer representing the number of steps moved to be stored later
"""
def measureDistance(original: int, cut: int, unit: str) -> int:

    piSetup()

    # if cut is going to be more than half of the original, set cut to opposite
    if (cut > (.5 * original)):
        cut = original - cut

    # adjust according to which unit is used, round accordingly 
    if unit == "mm":
        stepCount = round(cut * (1/MM_PER_STEP))
    if unit == "in":
        stepCount = round(cut * (1/IN_PER_STEP))
    if unit == "cm":
        stepCount = round(cut * (1/CM_PER_STEP))


    stepCount = int(stepCount)

    negY(stepCount)

    GPIO.cleanup()

    return stepCount






