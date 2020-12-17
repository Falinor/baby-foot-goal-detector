import RPi.GPIO as GPIO
from os.path import dirname, join
import statistics
import time

import client
import detector
import eventbus
import lights
import sound


DEFAULT_GOAL_TIMEOUT = 5

def countdown(seconds):
    while seconds > 0:
        print('Reset in', seconds)
        time.sleep(1)
        seconds -= 1

ambiances = sound.Playlist(directory)
def ambiances():
    for sound in ambiances.next():
        eventbus.on('goal:scored', sound.stop)
        sound.play().wait_done()

goals = sound.Playlist(join(dirname(__file__), 'sounds', 'goals'))
def goal():
    goals.next().play().wait_done()

def init():
    lights.meteor()
    anthem = sound.Sound(join(dirname(__file__), 'sounds', 'uefa-anthem.wav'))
    anthem.play().wait_done()
    lights.yellow()

def detect():
    detectors = [
        detector.Detector('Joker', 24, 27, lights.yellow),
        detector.Detector('Batman', 23, 17, lights.purple)
    ]
    while True:
        for detec in detectors:
            detection = detec.measure()
            if detection:
                # Goal
                lights.meteor()
                # Send to the server
                client.emit('goal:scored', detec.team)
                print("Goal scored against %s!" % detec.team)
                eventbus.emit('goal:scored')
                goal()
                # Wait for the given time
                countdown(DEFAULT_GOAL_TIMEOUT)
                # Highlight the last scoring team
                detec.light_up()
        time.sleep(0.1)

async def main():
    init()
    detect()

if __name__ == '__main__':
    try:
        init()
        playlist()
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        lights.disable_all()
        GPIO.cleanup()
