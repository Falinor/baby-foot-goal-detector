import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

METEOR = 13
YELLOW = 6
PURPLE = 19

GPIO.setup(METEOR, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(PURPLE, GPIO.OUT)

def trigger(pin):
    disable_all()
    GPIO.output(pin, True)
    # Wait a little before disabling the output
    time.sleep(0.5)
    disable_all()

def disable(pin):
    GPIO.output(pin, False)

def disable_all():
    disable(METEOR)
    disable(YELLOW)
    disable(PURPLE)
 
def meteor():
    trigger(METEOR)
    print('Now playing meteor')

def yellow():
    trigger(YELLOW)
    print('Now playing yellow')

def purple():
    trigger(PURPLE)
    print('Now playing purple')

if __name__ == '__main__':
    meteor()
    time.sleep(2)
    yellow()
    time.sleep(2)
    purple()
