import RPi.GPIO as GPIO
import time
channel = 13
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
def heater_on(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn switch on
def heater_off(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn switch off
