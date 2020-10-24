import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

METEOR = 13
YELLOW = 26
PURPLE = 19

GPIO.setup(METEOR, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(PURPLE, GPIO.OUT)

def trigger(pin):
    GPIO.output(pin, True)

def disable(pin):
    GPIO.output(pin, False)

def disable_all():
    disable(METEOR)
    disable(YELLOW)
    disable(PURPLE)
 
def meteor():
    disable_all()
    print('Now playing meteor')
    trigger(METEOR)

def yellow():
    disable_all()
    print('Now playing yellow')
    trigger(YELLOW)

def purple():
    disable_all()
    print('Now playing purple')
    trigger(PURPLE)
