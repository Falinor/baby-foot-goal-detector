# Libraries
import RPi.GPIO as GPIO
import time
import statistics

import client
import detector
import lights

if __name__ == '__main__':
    try:
        lights.meteor()
        detectors = [
            detector.Detector('joker', 17, 27),
            detector.Detector('batman', 23, 24)
        ]
        while True:
            for detec in detectors:
                detec.measure()
            time.sleep(0.5)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
