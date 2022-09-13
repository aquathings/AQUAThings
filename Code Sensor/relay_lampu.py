import RPi.GPIO as GPIO
import time
channel = 26
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
def lampu_on(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn led on
def lampu_off(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn led off
