from gym import spaces, Env
from shapely.geometry import LineString, Point

class Maze(Env):
    """Single asset env with immediate reward. Simplest case."""
    def __init__(self, start_point, start_heading, maze, goal, sensors):
        """Initialize environment.

        Args:
            start_point (Point): Start point.
            start_heading (array): Start direction.
            maze (LineString): Labyrinth of walls.
            goal (LineString): Finish line.
            sensors (list of Sensor): All sensors.
        """
        # self.observation_space = spaces.Box(lower, upper, dtype=np.float32)
        # self.action_space = spaces.Discrete(2)
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
        pass

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        
        Returns:
            observation (object): The initial observation of the space. Initial reward is assumed to be 0.
        """
        pass

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