import numpy as np
from shapely.geometry import LineString, Point, MultiPoint


class Sensordata():
    def __init__(self,line,angle,distance=None):
        self.line = line
        self.angle = angle
        self.distance = distance
        self.std = 0
        

class Surrounding():
    def __init__(self, heading, min_dist, max_dist, fov, resolution, rand_std=0):
        """Initialize sensor.

        Simple sensor has no relative position in vehicle.

        Args:
            heading (float): Heading relative to vehicle, in radians.
            min_dist (float): Minimum distance for sensor signal in meters.
            max_dist (float): Maximum distance for sensor signal in meters.
            fov (float): the field of view for the sensor
            resolution (float): how many points the fov should be devided into
            rand_std (float): random_std for simulation, max std for each point

        """
        self.heading = heading
        self.fov = fov
        self.resolution = resolution
        self.min_dist = min_dist
        self.max_dist = max_dist
        self.set_vehicle_pos(Point(0, 0), 0)
        self.rand_std = rand_std

    # def __repr__(self):
    #     return f'Sensor {self.position} and {self.line}'
        
    def set_vehicle_pos(self, position, heading):
        """Update sensor with vehicle position.

        Args:
            position (Point): Vehicle x, y position in meters.
            heading (float): Vehicle heading in radians.
        """
        self.position = position
        heading = heading+self.heading
        self.lines = []
        angle_res = self.fov/self.resolution
        for i in range(self.resolution+1):
            heading_line = heading -self.fov/2 + angle_res*i
            self.lines.append(Sensordata(LineString([[self.position.x+self.min_dist*np.cos(heading_line),
                                self.position.y+self.min_dist*np.sin(heading_line)],
                                [self.position.x+self.max_dist*np.cos(heading_line), 
                                self.position.y+self.max_dist*np.sin(heading_line)]]),heading_line))

    def distance(self, maze):
        """Get distance from sensor to labyrinth.

        Args:
            maze (LineString): Labyrinth line object.

        Returns:
            list of Sensordata: Distance in meters. 0 if nothing intersects.
        """
        
        for sens_line in self.lines:
            points = sens_line.line.intersection(maze)
            
            if isinstance(points, Point):
                # Just the one point
                sens_line.distance = points.distance(self.position) + np.random.randn()*self.rand_std
                sens_line.std = np.random.randn()*self.rand_std*0.01
            elif isinstance(points, MultiPoint):
                # Find distance to closest point
                distance = self.max_dist
                for point in points:
                    d = point.distance(self.position)
                    if d < distance:
                        sens_line.distance = d + np.random.randn()*self.rand_std
                        sens_line.std = np.random.randn()*self.rand_std*0.01
            else:
                # No intersection                                                       
                sens_line.distance = 0
                sens_line.std = 0
        return self.lines

    # @property
    # def xy(self):
    #     """Returns sensor line position for plotting."""
    #     # return self.line.xy
    #     pass


class Simple():
    def __init__(self, heading_rel, min_dist, max_dist):
        """Initialize sensor.

        Simple sensor has no relative position in vehicle.

        Args:
            heading_rel (float): Heading relative to vehicle, in radians.
            min_dist (float): Minimum distance for sensor signal in meters.
            max_dist (float): Maximum distance for sensor signal in meters.
        """
        self.heading_rel = heading_rel
        self.min_dist = min_dist
        self.max_dist = max_dist
        self.set_vehicle_pos(Point(0, 0), 0)

    def __repr__(self):
        return f'Sensor {self.position} and {self.line}'
        
    def set_vehicle_pos(self, position, heading):
        """Update sensor with vehicle position.

        Args:
            position (Point): Vehicle x, y position in meters.
            heading (float): Vehicle heading in radians.
        """
        self.position = position
        heading = heading+self.heading_rel
        self.line = LineString([[self.position.x+self.min_dist*np.cos(heading),
                                 self.position.y+self.min_dist*np.sin(heading)],
                                [self.position.x+self.max_dist*np.cos(heading), 
                                 self.position.y+self.max_dist*np.sin(heading)]])

    def distance(self, maze):
        """Get distance from sensor to labyrinth.

        Args:
            maze (LineString): Labyrinth line object.

        Returns:
            float: Distance in meters. 0 if nothing intersects.
        """
        points = self.line.intersection(maze)

        if isinstance(points, Point):
            # Just the one point
            return points.distance(self.position)
        elif isinstance(points, MultiPoint):
            # Find distance to closest point
            distance = self.max_dist
            for point in points:
                d = point.distance(self.position)
                if d < distance:
                    distance = d
            return distance
        else:
            # No intersection
            return 0

    @property
    def xy(self):
        """Returns sensor line position for plotting."""
        return self.line.xy