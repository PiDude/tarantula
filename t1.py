#/bin/sh

import RPi.GPIO as GPIO
import sys
import time
import os
import cwiid

#use GPIO numbering
GPIO.setmode(GPIO.BCM)

# GPIO pins in use:
# GPIO 2  n/c               GPIO 15
# GPIO 3  n/c               GPIO 16
# GPIO 4  shutdown button   GPIO 17
# GPIO 5  LED seg           GPIO 18
# GPIO 6  LED seg           GPIO 19  LED seg
# GPIO 7                    GPIO 20  drive motor
# GPIO 8                    GPIO 21  drive motor
# GPIO 9                    GPIO 22  LED seg
# GPIO 10                   GPIO 23  steer motor
# GPIO 11                   GPIO 24  steer motor
# GPIO 12                   GPIO 25
# GPIO 13  LED seg          GPIO 26  LED seg
# GPIO 14                   GPIO 27  LED seg



# define a shutdown button
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)  

# use a 7-segment LED (5161AS) to show status of wimote.
# set up seven GPIO pins 
#
#  10  9   8    7   6
#   G  F  Gnd   A   B
#    
#          A
#        -----
#       |     |
#       |F    |B
#       |  G  |
#        -----
#       |     |
#       |E    |C
#       |     |
#        -----   dp
#          D
#
#  1   2   3   4   5
#  E   D  Gnd  C   dp


segments = (27,22,5,6,13,19,26)

for segment in segments:

    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, False)


# define the LED segments to make numbers

num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}


# display a 0 to show program is running.
print 'displaying 1'

for x in range(0,7):
    GPIO.output(segments[x], num['1'][x])
time.sleep(2)


# drive motor
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

# steer motor
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


#PWM_FREQ=50  #50Hz
#GPIO.PWM(23, PWM_FREQ)
#GPIO.PWM(17, PWM_FREQ)
#GPIO.PWM(20, PWM_FREQ)
#GPIO.PWM(21, PWM_FREQ)

# a litte time to de-bounce a wiimote button
button_delay = 0.1


def Shutdown(channel):

    # on shutdown, display a "3"

    for x in range(0,7):
        GPIO.output(segments[x], num['3'][x])  

    time.sleep(2)

    GPIO.cleanup()
    os.system("sudo shutdown -h now")


	
# configure the shutdown button
GPIO.add_event_detect(4, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)   



#print 2 to show pair wiimote
print 'display 6'

for x in range(0,7):
    GPIO.output(segments[x], num['6'][x])

time.sleep(2)


print 'press 1 + 2 on the Wii remote.....\n'

wii = None
i = 2

while not wii:
    try:
        wii = cwiid.Wiimote()
    except RuntimeError:
        if (i>10):

            GPIO.output(6, True) # turn on RED LED.  wiimote failed.
            time.sleep(2)
            GPIO.output(6, False)
            GPIO.cleanup()

            quit()
            break

#        print 'Error connecting to Wii remote. trying again...'
        i = i +1


#wiimote pairing SUCCESS
print 'Wii remote connected !\n'
print 'displaying 3'

for x in range(0,7):
    GPIO.output(segments[x], num['3'][x])

time.sleep(2)



wii.rpt_mode = cwiid.RPT_BTN


while True:

    buttons = wii.state['buttons']

    # quit if press + and - buttons together'

    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
#        print '\nClosing connection....'
        wii.rumble = 1
        time.sleep(0.5)
        wii.rumble = 0
        GPIO.cleanup()
        exit(wii)

    elif (buttons & cwiid.BTN_UP):  # go forward
        
        print 'forward'
        
        GPIO.output(20, True)
        GPIO.output(21, False)
        
        time.sleep(button_delay)
        
    elif (buttons & cwiid.BTN_DOWN):  # go backward

        print 'back'

        GPIO.output(20, False)
        GPIO.output(21, True)

        time.sleep(button_delay)


    elif (buttons & cwiid.BTN_LEFT):    # turn left
        
        print 'left'

        GPIO.output(23, False)
        GPIO.output(24, True)

        time.sleep(button_delay)


    elif (buttons & cwiid.BTN_RIGHT):    # turn right

        print 'right'

        GPIO.output(23, True)
        GPIO.output(24, False)

        time.sleep(button_delay)
        
    else:
        GPIO.output(20, False)
        GPIO.output(21, False)

        GPIO.output(23, False)
        GPIO.output(24, False)

        time.sleep(button_delay)


#print 'done'


GPIO.cleanup()



