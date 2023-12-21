
# Author: Darya Clark
# Purpose: This program uses the relay in order to turn on the dremel cutting
#          device

import RPi.GPIO as GPIO 
import time

led = 40


def setup(): 
    GPIO.setup(led, GPIO.OUT)

def clean():
    GPIO.output(led, GPIO.LOW)
    GPIO.cleanup()

def turnOnDremel():
    setup()
    GPIO.output(led, GPIO.HIGH)

def turnOffDremel():
    setup()
    GPIO.output(led, GPIO.LOW)

