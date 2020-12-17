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

DEFAULT_GOAL_TIMEOUT = 5

def countdown(seconds):
    while seconds > 0:
        print('Reset in', seconds)
        time.sleep(1)
        seconds -= 1

if __name__ == '__main__':
    try:
        lights.meteor()
        anthem = sound.Sound(os.path.join(os.getcwd(), 'src', 'sounds', 'uefa-anthem.wav'))
        anthem.play().wait_done()

        lights.yellow()
        detectors = [
            detector.Detector('Joker', 24, 27, lights.yellow),
            detector.Detector('Batman', 23, 17, lights.purple)
        ]

        ambiances = sound.Playlist(os.path.join(os.getcwd(), 'src', 'sounds'))
        # [sound.play().wait_done() for sound in ambiances.next()]
        # for sound in ambiances.next():
            # Thread(target=playlist)

        # TODO: exec in a thread
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
                        state['light_status'] = 'Joker' if detec.team == 'Batman' else 'Batman'
                        detec.light_up()
            time.sleep(0.1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        lights.disable_all()
        GPIO.cleanup()
