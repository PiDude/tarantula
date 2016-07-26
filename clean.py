
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

for x in range(2,28):

    print x
    GPIO.setup(x, GPIO.OUT)
    GPIO.setup(x, False)

GPIO.cleanup()


