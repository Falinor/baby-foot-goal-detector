# Libraries
import RPi.GPIO as GPIO
import time
import statistics

import client


DISTANCE_THRESHOLD = 3

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

class Detector:
    def __init__(self, team, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        self.team = team

        # Set GPIO direction (IN / OUT)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        # Measure the reference distance
        self.ref_dist = self.ref_distance()
        print("Reference distance = %.1f cm" % self.ref_dist)


    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.trigger, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance

    # Compute the average distance of 10 measures
    def ref_distance(self):
        distances = map(lambda x: self.distance(), range(10))
        average = statistics.mean(distances)
        return average

    def is_goal(self, ref_dist, dist):
        return abs(ref_dist - dist) > DISTANCE_THRESHOLD

    def measure(self):
        dist = self.distance()
        print ("Measured Distance = %.1f cm" % dist)
        goal = self.is_goal(self.ref_dist, dist)
        if goal:
            print("Goal scored against %s!" % self.team)
            client.sio.emit('goal:scored', self.team)
            time.sleep(10)

