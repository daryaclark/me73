
# Author: Darya Clark
# Purpose: This code serves as a debugging tool for electronic systems of the
# REEKON2 Shaft Cutting device. User runs code and adjusts values in 
# Airtable to test various systems

import updateTable
import leadScrewStepper
import measuringMotor
import RPi.GPIO as GPIO 
import time



CLOCK_SPEED = 3

def main():

    try: 

        time.sleep(3)

        stopProgram = False
        checker = 0
        
        # loop until stop
        while not stopProgram:
            # know how many checks occurred
            print(checker)
            print("checking again!")
            
            # pull values from Airtable
            runLeadScrew = updateTable.getStatus("Debugging", "Lead Screw Stepper Motor", "Run?")
            stop = updateTable.getStatus("Debugging", "Stop Program", "Run?")
            measuring = updateTable.getStatus("Debugging", "Measuring Motor", "Run?")
            
            
            if stop:

                print("stopping")
                stopProgram = True

            elif runLeadScrew:

                print("lead screw time")

                leadScrewStepper.piSetup()

                stepCount = updateTable.getStatus("Debugging", "Lead Screw Stepper Motor", "Step count")

                # account for negative values 
                if stepCount > 0:
                    leadScrewStepper.posZFast(stepCount)   
                else: 
                    stepCount = abs(stepCount)
                    leadScrewStepper.negZFast(stepCount)

                # change value back to 0 
                updateTable.postStatus("Debugging", "Lead Screw Stepper Motor", "Run?", 0) 

                GPIO.cleanup()
            elif measuring:
                print("measuring")

                measuringMotor.piSetup()

                stepCount1 = updateTable.getStatus("Debugging", "Measuring Motor", "Step count")

                if stepCount1 > 0:
                    measuringMotor.posY(stepCount1)   
                else: 
                    stepCount1 = abs(stepCount1)
                    measuringMotor.negY(stepCount1)

                updateTable.postStatus("Debugging", "Measuring Motor", "Run?", 0) 

                GPIO.cleanup()
            
            time.sleep(CLOCK_SPEED)
            checker += 1

        updateTable.postStatus("Debugging", "Stop Program", "Run?", 0)
        
    except KeyboardInterrupt:
        GPIO.cleanup()  # type:ignore

# Runs main code if file is run from console but NOT if included as library.
if __name__ == "__main__":
    main()