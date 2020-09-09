import arnold
from gym import spaces, Env
from shapely.geometry import LineString, Point

class Maze(Env):
    GOAL_DIST_FOR_SUCCESS = 0.1

    """Single asset env with immediate reward. Simplest case."""
    def __init__(self, vehicle, sensors, start_pos, start_heading, maze, goal):
        """Initialize environment.

        Args:
            vehicle (Arnold): Vehicle object
            sensors (list of Sensor): All sensors.
            start_pos (Point): Start position.
            start_heading (float): Start direction.
            maze (LineString): Labyrinth of walls.
            goal (LineString): Finish line.
        """
        self.observation_space  = spaces.Box(0, # min value
                                            sensors[0].max_dist, # max value
                                            shape=len(sensors),
                                            dtype=np.float32)

        self.action_space       = spaces.Box(-1.0,
                                             +1.0,
                                             shape=2,
                                             dtype=np.float32)

        self.vehicle = vehicle
        self.sensors = sensors
        self.start_pos = start_pos
        self.start_heading = start_heading
        self.maze = maze
        self.goal = goal
        self.reset()

    def step(self, action):
        """Run one timestep of the environment's dynamics.

        Accepts an action and returns a tuple (observation, reward, done, info).
        
        Args:
            action (object): An action provided by the environment.
        
        Returns:
            observation (object): Agent's observation of the current environment.
            reward (float) : Amount of reward returned after previous action.
            done (boolean): Whether the episode has ended, in which case further step() calls will return undefined results.
            info (dict): Contains auxiliary diagnostic information (helpful for debugging, and sometimes learning).
        """
        assert self.action_space.contains(action), '%r (%s) invalid'%(action, type(action))

        """
		Actions based on the previous timestep is given by the agent.
		The environment now acts on actions and observes consequences.
		"""

        reward = 0

        if action[0] != 0 or action[1] != 0:
            reward = 1

        control = arnold.ControlInput(self.heading, 
                                      0.1, 
                                      np.sign(action[0]), 
                                      np.sign(action[1]),
                                      np.abs(action[0]),
                                      np.abs(action[1]))

        # Move the agent
        dx, dy, deltah = self.vehicle.step(control)
        self.position.x += dx
        self.position.y += dy
        self.heading += deltah

        observation = []
        goal_distance = []
        for sensor in self.sensors:
            sensor.set_vehicle_position(self.position, self.heading)
		
            # The agent observes the environment through its sensors
            observation.append(sensor.distance(self.maze))

            # For the agent to finish, the goal must be visible with the sensors.
            # It is not acceptable to be close to the goal through a wall.
            # But this is not implemented yet. Right now we only do closest distance
            # to any sensor (MVP).
            dist = sensor.distance(self.goal)
            if dist > 0:
                goal_distance.append(dist)

        if goal_distance and np.min(goal_distance) < self.GOAL_DIST_FOR_SUCCESS:
            reward = 100
            done = True
        else:
            done = False

        return observation, reward, done, {}

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        
        Returns:
            observation (object): The initial observation of the space. Initial reward is assumed to be 0.
        """
        # Reset vehicle and sensor positions (and headings)
        self.position = self.start_pos
        self.heading = self.start_heading
        for sensor in self.sensors:
            sensor.set_vehicle_position(self.position, self.heading)

    def render(self, mode=None):
        """Renders the environment.

        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.)
        
        Arg:
            mode (str): The mode to render with.
        """
        pass

    def close(self):
        """Override in your subclass to perform any necessary cleanup..p
        
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        pass