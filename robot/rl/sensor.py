import numpy as np
from shapely.geometry import LineString, Point, MultiPoint


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