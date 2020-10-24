import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def trigger(pin):
  GPIO.setup(trigger, GPIO.OUT)
  GPIO.output(trigger, True)
 
def meteor():
  trigger(26)

def yellow():
  trigger(19)

def purple():
  trigger(13)