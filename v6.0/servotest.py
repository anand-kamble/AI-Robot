# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1.start(0)
print ("Waiting for 2 seconds")
time.sleep(2)

#Let's move the servo!
print ("Rotating 180 degrees in 10 steps")

# Define variable duty
duty = 2

# Loop for duty values from 2 to 12 (0 to 180 degrees)
while duty <= 12:
    servo1.ChangeDutyCycle(duty)
    time.sleep(1)
    duty = duty + 1

# Wait a couple of seconds
time.sleep(2)

# Turn back to 90 degrees
print ("Turning back to 90 degrees for 2 seconds")
servo1.ChangeDutyCycle(7)
time.sleep(2)
servo1.ChangeDutyCycle(0)

#turn back to 0 degrees
print ("Turning back to 0 degrees")
servo1.ChangeDutyCycle(2)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)

#Clean things up at the end
servo1.stop()
GPIO.cleanup()
print ("Goodbye")   


''' he servo angle is determined by the pulse width in a 50 Hz PWM signal.

Most servos move to 0 when they receive a pulse 1500 µs long. Generally it is safe to send a servo a pulse in the range 1000 µs to 2000 µs. Generally a 10 µs change in pulse width results in a 1 degree change in angle.

At some point you will reach the limit of rotation. That limit varies between different makes and models of servos. If you try to force a servo beyond its limits it will get very hot (possibly to destruction) and may strip its gears.

The small 9g servos generally have an extended angle range, 180 degrees or more. Typically they accept pulse widths in the range 500 µs to 2500 µs.



20 ms per cycle
1000 us 0deg
2000 us 180deg

5.55 us per deg


400 us == 0 deg duty = 2
2400 == 180 deg duty = 12





 '''