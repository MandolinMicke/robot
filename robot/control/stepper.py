import RPi.GPIO as gp
import time

import numpy as np

class Steps():
    """ class that gives the next step for a stepper motor


    """
    def __init__(self):
        h = gp.HIGH
        l = gp.LOW
        self.emptystep = [l,l,l,l]
        self.active_state = 0
        self.states = [
            [h,l,l,l],
            [h,h,l,l],
            [l,h,l,l],
            [l,h,h,l],
            [l,l,h,l],
            [l,l,h,h],
            [l,l,l,h],
            [h,l,l,h]
        ]
    def _counter_step(self,direction):
        """ updates the active_state the next step in order

        Parameter
        ---------
            direction: +1 or -1
        
        """
        if direction not in [1,-1]:
            ValueError(str(direction) + ' is not a correct counter step')
        self.active_state += direction
        if self.active_state > 7:
            self.active_state = 0
        elif self.active_state < 0:
            self.active_state = 7
        
    def next_step(self,direction):
        """ sends the next step in order

        Parameter
        ---------
            direction: +1 or -1
        
        Returns:
            list of states

        """
        self._counter_step(direction)
        return self.states[self.active_state]

    def get_empty_step(self):
        return self.emptystep

class StepMotor():
    def __init__(self,pins = [2,3,4,17]):
        gp.setmode(gp.BCM)
        self.pins = pins
        self.stepper = Steps()
        self.sleeptime = 0.0005
        
        for i in self.pins:
            gp.setup(i,gp.OUT)

    def do_step(self,direction):
        states = self.stepper.next_step(direction)
        # print(states)
        for i in range(4):
            gp.output(self.pins[i],states[i])
        time.sleep(self.sleeptime)
    
    def do_steps(self,direction,steps):
        for i in range(steps):
            self.do_step(direction)

    def turn_deg(self,angle):
        self.turn_rad(angle/180*np.pi)

    def turn_rad(self,angle):
        if angle <0:
            direction = -1
        else:
            direction = 1

        steps = round(angle*400/np.pi)
        self.do_steps(direction,steps)
    
    def set_speed(self,sleeptime):
        self.sleeptime = sleeptime

    
    def teardown(self):
        gp.cleanup()

if __name__ == '__main__':
    sm = StepMotor()

    # sm.do_steps(1,200)
    sm.turn_deg(1080)
    
    sm.teardown()