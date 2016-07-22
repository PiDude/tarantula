#/bin/sh

import RPi.GPIO as GPIO
import sys
import time
import os
import cwiid


GPIO.setmode(GPIO.BCM)

# shutdown button
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)  

# LEDs to show status of wimote.
#  GPIO 5 - green LED means SUCCESS pairing
#  GPIO 6 - red LED means FAILURE pairing

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

GPIO.output(5, False)
GPIO.output(6, False)


# right gearbox
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

#left gearbox
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)


#PWM_FREQ=50  #50Hz
#GPIO.PWM(23, PWM_FREQ)
#GPIO.PWM(17, PWM_FREQ)
#GPIO.PWM(20, PWM_FREQ)
#GPIO.PWM(21, PWM_FREQ)

button_delay = 0.1


def Shutdown(channel):

    GPIO.output(5, True)
    GPIO.output(6, True)
    time.sleep(2)
    GPIO.output(5, False)
    GPIO.output(6, False)
    GPIO.cleanup()
    os.system("sudo shutdown -h now")
	

GPIO.add_event_detect(4, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)   

#blink green LED as signal to pair wiimote.

GPIO.output(5, True)
time.sleep(0.5)
GPIO.output(5, False)
time.sleep(0.5)
GPIO.output(5, True)
time.sleep(0.5)
GPIO.output(5, False)


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

        print 'Error connecting to Wii remote. trying again...'
        i = i +1


GPIO.output(5, True)  #wiimote pairing SUCCESS.  light green LED for 2 seconds.
print 'Wii remote connected !\n'
time.sleep(2)
GPIO.output(5, False)


wii.rpt_mode = cwiid.RPT_BTN


while True:

    buttons = wii.state['buttons']

    # quit if press + and - buttons together'

    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        print '\nClosing connection....'
        wii.rumble = 1
        time.sleep(0.5)
        wii.rumble = 0
        GPIO.output(5, True)
        GPIO.output(6, True)
        GPIO.cleanup()
        exit(wii)

    elif (buttons & cwiid.BTN_UP):  # go forward
        
        print 'forward'
        
        GPIO.output(23, True)
        GPIO.output(24, False)
        
        GPIO.output(20, True)
        GPIO.output(21, False)

        time.sleep(button_delay)
        
    elif (buttons & cwiid.BTN_DOWN):  # go backward

        print 'back'

        GPIO.output(23, False)
        GPIO.output(24, True)

        GPIO.output(20, False)
        GPIO.output(21, True)

        time.sleep(button_delay)


    elif (buttons & cwiid.BTN_LEFT):    # turn left
        
        print 'left'

        GPIO.output(23, True)
        GPIO.output(24, False)

        GPIO.output(20, False)
        GPIO.output(21, True)

        time.sleep(button_delay)


    elif (buttons & cwiid.BTN_RIGHT):    # turn right

        print 'right'

        GPIO.output(23, False)
        GPIO.output(24, True)

        GPIO.output(20, True)
        GPIO.output(21, False)

        time.sleep(button_delay)
        
    else:
        GPIO.output(23, False)
        GPIO.output(24, False)

        GPIO.output(20, False)
        GPIO.output(21, False)

        time.sleep(button_delay)


print 'done'
GPIO.output(5, True)
GPIO.output(6, True)
time.sleep(2)
GPIO.output(5, False)
GPIO.output(6, False)


GPIO.cleanup()



