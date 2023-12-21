
# Author: Darya Clark
# Purpose: This program serves as the main driver for the REEKON 2 shaft cutting
# device and runs the program as a whole. Use ^C to cancel as needed

import updateTable

import RPi.GPIO as GPIO 
import time
from typing import Tuple, Dict
import measuringMotor
import feedIn
import relay
import resetter
import leadScrewStepper


CLOCK_SPEED = 2

def main():

    try: 

        time.sleep(CLOCK_SPEED)

        stopProgram = False
        
        cutLength, original = welcome() 

        # if error, stop program
        if cutLength == -1:
            "Try again in web browser; negative length of cut "
            return
        
        # start process with 
        updateTable.postStatus("Processes", "Place Block at Measurement", "Begin Process?", 1)
        # loop until stop
        while not stopProgram:

            # collect processes    
            stop = updateTable.getStatus("Processes", "Stop Program", "Begin Process?")
            blockPlaced = updateTable.getStatus("Processes", "Place Block at Measurement", "Begin Process?")
            feedRod = updateTable.getStatus("Processes", "Feed in Rod", "Begin Process?")
            lowerDremel = updateTable.getStatus("Processes", "Lower Dremel and Cut", "Begin Process?") 
            reset = updateTable.getStatus("Processes", "Reset", "Begin Process?") 

            if stop:
                # handle anything that has been run in the program 
                stopProgram = True
                # just in case! 
                relay.clean()
                if updateTable.getStatus("Processes", "Lower Dremel and Cut", "Complete"):
                    leadScrewStepper.raiseDremel(3)
                if updateTable.getStatus("Processes", "Place Block at Measurement", "Complete"):
                    resetter.resetMeasure(170)
                updateTable.resetTable("Processes")
                
            elif blockPlaced:
                print("placing block")

                updateTable.postStatus("Processes", "Place Block at Measurement", "Begin Process?", 0)
                updateTable.postStatus("Processes", "Place Block at Measurement", "In Process", 1)

                unit = str((updateTable.getMostRecent("Orders"))["Units"])
                # measure out distance for belt system based on cut
                stepCountMeasure = measuringMotor.measureDistance(original, cutLength, unit)

                updateTable.postStatus("Processes", "Place Block at Measurement", "In Process", 0)
                updateTable.postStatus("Processes", "Place Block at Measurement", "Complete", 1)
                updateTable.postStatus("Processes", "Feed in Rod", "Begin Process?", 1)

            elif feedRod:
                print("feeding in rod")

                updateTable.postStatus("Processes", "Feed in Rod", "Begin Process?", 0)
                updateTable.postStatus("Processes", "Feed in Rod", "In Process", 1)

                # feed in rod based on step count 
                order = updateTable.getMostRecent("Orders")
                diameter = int((order["Diameter"])[0])
                feedIn.runMotor(stepCountMeasure, diameter)
                time.sleep(1)
                resetter.resetMeasure(-(170-stepCountMeasure))
                
                updateTable.postStatus("Processes", "Feed in Rod", "In Process", 0)
                updateTable.postStatus("Processes", "Feed in Rod", "Complete", 1)
                updateTable.postStatus("Processes", "Lower Dremel and Cut", "Begin Process?", 1)

            elif lowerDremel:
                print("lower dremel")

                updateTable.postStatus("Processes", "Lower Dremel and Cut", "Begin Process?", 0)
                updateTable.postStatus("Processes", "Lower Dremel and Cut", "In Process", 1)

                order = updateTable.getMostRecent("Orders")
                diameter = int((order["Diameter"])[0])
                leadScrewStepper.lowerAndCut(3)
                leadScrewStepper.raiseDremel(3)

                updateTable.postStatus("Processes", "Lower Dremel and Cut", "In Process", 0)
                updateTable.postStatus("Processes", "Lower Dremel and Cut", "Complete", 1)
                updateTable.postStatus("Processes", "Reset", "Begin Process?", 1)

            elif reset:
                resetter.resetMeasure(170)
                resetter.resetTable()
                print("ending")
                return

            time.sleep(CLOCK_SPEED)

    # Cleans up pins
    except KeyboardInterrupt:
        # just in case! 
        relay.clean()
        if updateTable.getStatus("Processes", "Lower Dremel and Cut", "Complete"):
            leadScrewStepper.raiseDremel(3)
        if updateTable.getStatus("Processes", "Place Block at Measurement", "Complete"):
            resetter.resetMeasure(170)
        updateTable.resetTable("Processes")
        GPIO.cleanup()  # type:ignore
        return

"""
name: welcome
parameters: none
goal: pull first entry of table to get information about the cut 
return: tuple of cutLength and original 
"""
def welcome() -> Tuple[int, int]:
    print("Welcome!")

    # index information about shaft cut
    order = updateTable.getMostRecent("Orders")
    original = order["Starting Length"]
    desired = order["Desired Length"]
    unit = order["Units"]

    # prevent error
    if desired > original:
        print("Yikes! You can't cut a shaft more than its original length")
        return -1, -1
    else: 
        cutLength = original - desired 
    print(f"You requested a {cutLength} {unit} cut to your {original} {unit} length shaft. Here we go!")

    return cutLength, original

# Runs main code if file is run from console but NOT if included as library.
if __name__ == "__main__":
    main()