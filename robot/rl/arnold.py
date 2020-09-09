import numpy as np
from dataclasses import dataclass
# import matplotlib.pyplot as plt
import pylab as p
@dataclass
class ControlInput():
    """ struct def for the steps in Arnold
        
        Attributes
        ----------
            heading (float): rad, heading at start point
            time_step (float): s, time step of step
            left_speed (float): 0:1 rad/s speed of left motor
            right_speed (float): 0:1 rad/s speed of right motor
    """


    heading: float
    time_step: float
    left_speed: float
    right_speed: float



class Arnold():
    """ Base class for a robot which can move around in a world

        Parameters
        ----------

        Attributes
        ----------
            wheel_radius (float): radius of the wheels
            
            width (float): width of the robot
        Methods
        -------

    """

    def __init__(self):
        """ initalize Arnold

        """
        self.wheel_radius = 0.05
        self.width = 0.1

    def step(self,controlinput):
        left_len = controlinput.left_speed*self.wheel_radius*controlinput.time_step
        right_len = controlinput.right_speed*self.wheel_radius*controlinput.time_step
        
        frac = np.sqrt(4*self.width**2 - (left_len - right_len)**2)/2/self.width
        
        right_ang = np.arcsin(frac)
        if left_len >= right_len:
            deltah = right_ang - np.pi/2
        else:
            deltah = -right_ang + np.pi/2
        # print(deltah)
        trav_dist = (left_len + right_len)/2
        dx = trav_dist*np.cos(deltah + controlinput.heading)
        dy = trav_dist*np.sin(deltah + controlinput.heading)
        return dx, dy, deltah

if __name__ == '__main__':
    arnold = Arnold()
    inp = ControlInput
    inp.heading = 0
    inp.time_step = 1
    inp.left_speed = -0.1
    inp.right_speed = 0.1

    x = 0
    y = 0
    xl = []
    yl = []
    for i in range(10):
        dx, dy, deltah = arnold.step(inp)
        inp.heading += deltah
        x += dx
        y += dy
        print('New position: (' + str(x) + ',' + str(y) + ',' + str(inp.heading) + ')')
        # p.arrow( x, y, np.cos(inp.heading), np.sin(inp.heading), fc="k", ec="k",head_width=0.05, head_length=0.1 )
        # p.show()





