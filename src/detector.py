# Libraries
import RPi.GPIO as GPIO
import time
import statistics


DISTANCE_THRESHOLD = 2
TIME_BEFORE_LIGHT_RESET = 2
MAX_DETECTIONS = 10

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

class Detector:
    def __init__(self, team, trigger, echo, light_up):
        self.trigger = trigger
        self.echo = echo
        self.team = team
        self.light_up = light_up
        self.last = -1

        # Set GPIO direction (IN / OUT)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        # Measure the reference distance
        self.ref_dist = self.ref_distance()
        print("Reference distance = %.1f cm" % self.ref_dist)


    def distance(self):
        # Clean up
        GPIO.output(self.trigger, GPIO.LOW)
        GPIO.output(self.trigger, GPIO.HIGH)

	# set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, GPIO.LOW)

        # save StartTime
        i = 0
        while GPIO.input(self.echo) == 0:
            start_time = time.time()
            i += 1
            if i > 500:
                return 100000 # N'importe quoi qui marche en cm
                
        start_time = time.time()

        # save time of arrival
        i = 0
        while GPIO.input(self.echo) == 1:
            stop_time = time.time()
            i += 1
            if i > 500:
                return 100000 # N'importe quoi qui marche en cm

        stop_time = time.time()

        # time difference between start and arrival
        time_elapsed = stop_time - start_time
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (time_elapsed * 34300) / 2
        return distance

    # Compute the average distance of 10 measures
    def ref_distance(self):
        distances = map(lambda x: self.distance(), range(10))
        average = statistics.mean([d for d in distances if d < 60])
        return average

    def is_goal(self, ref_dist, dist):
        return ref_dist - dist > DISTANCE_THRESHOLD

    def measure(self, log = False):
        dist = self.distance()
        if log:
            print(self.team, dist)
        is_goal = self.is_goal(self.ref_dist, dist)
        self.last += 1
        if is_goal:
            if log:
                print('Ref dist:', self.ref_dist)
                print('Measured:', dist)
            # Remove false positives
            if self.last < MAX_DETECTIONS:
                self.last = 0
                return True
            else:
                self.last = 0
        return False
