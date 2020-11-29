import os
import sys
sys.path.insert(0, os.path.join('..', 'rl'))

import sensor
import numpy as np
import sensor
from shapely.geometry import LineString, Point
import matplotlib.pyplot as plt
import time
from Communication import Network
from Commands import sensor_distance, shutdown

maze = LineString([[0,4], [0,0], [.9,0], [.9,4], [0,6]])

sensors = []
min_dist, max_dist = 0.1, 3
res = 20
sensors.append(sensor.Surrounding(np.pi/2, min_dist, max_dist,np.pi,res,0.05))
sensors.append(sensor.Surrounding(-np.pi/2, min_dist, max_dist,np.pi,res,0.05))
# sensors.append(sensor.Surrounding(-np.pi/2, min_dist, max_dist,np.pi/2,5))
net = Network('master_sim')
net.setup_publisher()
x_0 = 0.4
y_0 = 2
h_0 = np.pi/2
dy = [0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2]
for t in dy:
    out = []
    y_0 +=t
    for s in sensors:
        s.set_vehicle_pos(Point(x_0,y_0),h_0)
        out.extend(s.distance(maze))

    for i in out:
        # print(i)
        if i.distance != 0:
            net.send(sensor_distance(i.distance,i.angle,i.std))
            time.sleep(0.0001)
net.send(shutdown())