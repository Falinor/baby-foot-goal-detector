# Libraries
import RPi.GPIO as GPIO
import time
import statistics

import client

DISTANCE_THRESHOLD = 2
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

# Compute the average distance of 10 measures
def ref_distance():
    distances = map(lambda x: distance(), range(10))
    average = statistics.mean(distances)
    return average

def is_goal(ref_dist, dist):
    return abs(ref_dist - dist) > DISTANCE_THRESHOLD
 
if __name__ == '__main__':
    try:
        ref_dist = ref_distance()
        print("Reference distance = %.1f cm" % ref_dist)
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            goal = is_goal(ref_dist, dist)
            if goal:
                print("Goal!")
                client.sio.emit('goal:scored', 'batman')
                time.sleep(10)
            time.sleep(0.5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
