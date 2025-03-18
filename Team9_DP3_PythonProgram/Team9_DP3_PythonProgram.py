## All libraries imported
import time
import sys
from sensor_library import *
from gpiozero import Buzzer
from gpiozero import Motor

## Defined input/output devices
gas = Gas_Sensor()
buzzer = Buzzer(27)
motor = Motor(forward = 16, backward = 12)

## Defined global variables
rolling_avg=0
list_ethanol = []
condition=False
ethanol_thres = 0.4 #Ethanol threshold level 

## Print column titles
print("Ethanol values", "\t", "Ethanol values (avg)","\t","  Motor Status","\t", "  Buzzer Status")

## Defined function to calculate rolling average.
def rolling_avg():
    n = 5
    list_ethanol.append(gas.ethanol())

    five = list_ethanol[-5:]
    sum_five = sum(five)
    rolling_avg = sum_five / n

    if len(list_ethanol) > n:
        list_ethanol.pop(0)
        
    return rolling_avg
    
## Defined function that rotates the motor for specific time.
def rot_motor(seconds):
    for i in range(seconds):
        motor_status=True
        motor.backward(speed = 0.25)
        print("   ",format(gas.ethanol(), ".3f"),"\t","\t", format(rolling_avg_list, ".3f"), "\t","\t","\t", motor_on, "\t","\t","\t",buzzer.is_active)
        time.sleep(1)
        motor.stop()

## Continuously print ethanol values, rolling average, and status of output devices. 
while True:
    motor_status = motor.is_active
    buzzer_status = buzzer.is_active
    rolling_avg_list = rolling_avg()

    print("   ",format(gas.ethanol(), ".3f"),"\t","\t", format(rolling_avg_list, ".3f"), "\t","\t","\t", motor_on, "\t","\t","\t",buzzer.is_active)
    time.sleep(1)
    
    ## Condition to rotate motor and turn on buzzer
    if rolling_avg > ethanol_thres and condition==False:
        condition=True
        rot_motor(1)
        buzzer.beep(1, 1, 3)
