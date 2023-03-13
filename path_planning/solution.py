import numpy as np
from scipy.interpolate import CubicSpline

class SplinePath:
    """Class to represent a path as a cubic spline."""

    # Constructor
    def __init__(self, environment, control_points=[], resolution=100):
        self.environment = environment
        self.control_points = control_points
        self.resolution = resolution
        
    # Create random control points
    @staticmethod
    def random(environment, num_control_points=10, resolution=100):
        control_points = np.random.rand(num_control_points, 2) * np.array([environment.width, environment.height])
        return SplinePath(environment, control_points, resolution)
    
    # Create control points from list
    @staticmethod
    def from_list(environment, xy, resolution=100, normalized=False):
        control_points = np.array(xy).reshape(-1, 2)
        if normalized:
            control_points[:,0] *= environment.width
            control_points[:,1] *= environment.height
            
        return SplinePath(environment, control_points, resolution)

    # Get path
    def get_path(self):
        
        # Add start and goal to control points
        start = self.environment.start
        goal = self.environment.goal
        points = np.vstack((start, self.control_points, goal))

        # Create spline
        t = np.linspace(0, 1, len(points))
        cs = CubicSpline(t, points, bc_type='clamped')

        # Get path
        tt = np.linspace(0, 1, self.resolution)
        path = cs(tt)

        # Clip path to environment
        path = self.environment.clip_path(path)
        
        return path
        

