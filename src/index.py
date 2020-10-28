# Libraries
import RPi.GPIO as GPIO
import statistics
import time

import client
import detector
import lights


if __name__ == '__main__':
    try:
        lights.disable_all()
        lights.meteor()
        detectors = [
            detector.Detector('Joker', 24, 27, lights.yellow),
            detector.Detector('Batman', 23, 17, lights.purple)
        ]
        while True:
            for detec in detectors:
                detec.measure()
            time.sleep(0.5)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        lights.disable_all()
        GPIO.cleanup()
