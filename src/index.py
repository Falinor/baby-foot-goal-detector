# Libraries
import RPi.GPIO as GPIO
import statistics
import time

# import client
import detector
import lights


state = {
  'light_status': 'meteor',
  'goal_timer': 0
}

DEFAULT_GOAL_TIMER = 40

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
                detection = detec.measure()
                if detection:
                    if state['light_status'] == 'meteor':
                        # Goal
                        print("Goal scored against %s!" % self.team)
                        # client.sio.emit('goal:scored', self.team)
                        detec.light_up()
                        state['light_status'] = detec.team

                    state['goal_timer'] = DEFAULT_GOAL_TIMER
                elif state['goal_timer'] > 0:
                    state['goal_timer'] -= 1
                    if state['goal_timer'] == 0:
                      state['light_status'] = 'meteor'
                      lights.disable_all()
                      lights.meteor()
            time.sleep(0.1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        lights.disable_all()
        GPIO.cleanup()
