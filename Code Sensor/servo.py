from gpiozero import Servo
from time import sleep


def pakan(lama):
    servo = Servo(26)
    servo.mid()
    sleep(1)
    
    servo.min()
    sleep(lama)

    servo.mid()
    sleep(1)

    servo.value = None;

#pakan(0.3)