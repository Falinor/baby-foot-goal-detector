# Libraries
import RPi.GPIO as GPIO
import os
import statistics
import time

import client
import detector
import lights
import sound


state = {
  'light_status': 'yellow'
}

DEFAULT_GOAL_TIMEOUT = 20

def countdown(seconds):
    while seconds > 0:
        print('Reset in', seconds)
        time.sleep(1)
        seconds -= 1

if __name__ == '__main__':
    try:
        anthem = sound.Sound(os.path.join('src', 'sounds', 'uefa-anthem.mp3'))
        anthem.play()
        # Test lights
        lights.meteor()
        time.sleep(1)
        lights.purple()
        time.sleep(1)
        lights.yellow()
        time.sleep(1)

        detectors = [
            detector.Detector('Joker', 24, 27, lights.yellow),
            detector.Detector('Batman', 23, 17, lights.purple)
        ]
        while True:
            for detec in detectors:
                detection = detec.measure()
                if detection:
                    if state['light_status'] != 'meteor':
                        # Goal
                        lights.meteor()
                        print("Goal scored against %s!" % detec.team)
                        client.emit('goal:scored', detec.team)
                        state['light_status'] = 'meteor'
                        countdown(DEFAULT_GOAL_TIMEOUT)
                        # Highlight the last scoring team
                        detec.light_up()
                        state['light_status'] = 'Joker' if detec.team == 'Batman' else 'Batman'
            time.sleep(0.1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        lights.disable_all()
        GPIO.cleanup()
