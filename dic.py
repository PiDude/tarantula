#/bin/sh

import RPi.GPIO as GPIO
import sys
import time
import os

#use GPIO numbering

GPIO.setmode(GPIO.BCM)

# define a shutdown button
#GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)  

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

print segments[0]
print segments[1]


for segment in segments:

    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

# define the LED segments to make numbers

#array[0]=[1,1,1,1,1,1,0]
#array[1]=[0,1,1,0,0,0,0]
#array[2]=[1,1,0,1,1,0,1]
#array[3]=[1,1,1,1,0,0,1]
#array[4]=[0,1,1,0,0,1,1]
#array[5]=[1,0,1,1,0,1,1]
#array[6]=[1,0,1,1,1,1,1]
#array[7]=[1,1,1,0,0,0,0]
#array[8]=[1,1,1,1,1,1,1]
#array[9]=[1,1,1,1,0,1,1]

print 'declaring num'

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


print 'printing num[9]'
print num['9']
print num['9'][1]


# on shutdown, display a "9"

print 'pair wiimote'

for x in range(0,7):

    print segments[x]
    GPIO.output(segments[x], num['9'][x])  

time.sleep(2)



#blink green LED twice as signal to pair wiimote.


print 'press 1 + 2 on the Wii remote.....\n'

wii = None
i = 2



#wiimote pairing SUCCESS.  light green LED for 2 seconds.
print 'Wii remote connected !\n'



time.sleep(2)


GPIO.cleanup()



