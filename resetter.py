
# Author: Darya Clark
# Purpose: This code resets the measuring motor as well as the Airtable; this
# file is used after program has run all the way through, or failed midway

import RPi.GPIO as GPIO 
import measuringMotor
import updateTable

"""
name: resetMeaure
parameters: integer representing step count
goal: move measuring motor specific number of steps
"""
def resetMeasure(stepCount: int):

    measuringMotor.piSetup()
    if stepCount > 0:
        measuringMotor.posY(stepCount)
    else: 
        measuringMotor.negY(abs(stepCount))
    GPIO.cleanup()

"""
name: resetTable
parameters: none
goal: publish 0 to all values in processes Airtable
"""
def resetTable():
    updateTable.resetTable("Processes")


    