import numpy as np

class Environment:
    """Class to represent the environment in which the mobile robot is operating."""

    # Constructor
    def __init__(self, width=100, height=100, robot_radius=0, obstacles=[], start=None, goal=None):
        self.width = width
        self.height = height
        self.robot_radius = robot_radius
        self.obstacles = obstacles
        self.start = start
        self.goal = goal

    # Method to add an obstacle to the environment
    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    # Method to add a list of obstacles to the environment
    def add_obstacles(self, obstacles):
        self.obstacles.extend(obstacles)

    # Method to remove all obstacles from the environment
    def clear_obstacles(self):
        self.obstacles = []

    # Method to check if a point is in collision with an obstacle
    def in_collision(self, point):
        for obstacle in self.obstacles:
            if obstacle.in_collision(point, self.robot_radius):
                return True
        return False

    # Method to check if a path is in collision with an obstacle
    def path_in_collision(self, path):
        for point in path:
            if self.in_collision(point):
                return True
        return False

    # Method to check if a point is in the environment
    def in_environment(self, point):
        min_x = 0 + self.robot_radius
        max_x = self.width - self.robot_radius
        min_y = 0 + self.robot_radius
        max_y = self.height - self.robot_radius
        return (min_x <= point[0] <= max_x) and (min_y <= point[1] <= max_y)

    # Method to check if a path is in the environment
    def path_in_environment(self, path):
        for point in path:
            if not self.in_environment(point):
                return False
        return True

    # Method to clip a point to the environment
    def clip_point(self, point):
        min_x = 0 + self.robot_radius
        max_x = self.width - self.robot_radius
        min_y = 0 + self.robot_radius
        max_y = self.height - self.robot_radius
        return np.array([np.clip(point[0], min_x, max_x), np.clip(point[1], min_y, max_y)])

    # Method to clip a path to the environment
    def clip_path(self, path):
        clipped_path = []
        for point in path:
            clipped_path.append(self.clip_point(point))
        return np.array(clipped_path)
    
    # Method to check if a point is in the goal region
    def in_goal(self, point):
        return np.linalg.norm(point - self.goal) <= self.robot_radius

    # Method to check if a path is in the goal region
    def path_in_goal(self, path):
        return self.in_goal(path[-1])
    
    # Method to check if a point is in the start region
    def in_start(self, point):
        return np.linalg.norm(point - self.start) <= self.robot_radius

    # Method to check if a path is in the start region
    def path_in_start(self, path):
        return self.in_start(path[0])

    # Count number of violations
    def count_violations(self, path):
        
        # Initialization
        violations = 0
        details = {
            'start_violation': False,
            'goal_violation': False,
            'environment_violation': False,
            'environment_violation_count': 0,
            'collision_violation': False,
            'collision_violation_count': 0,
        }
        
        # Check the start
        if not self.path_in_start(path):
            violations += 1
            details['start_violation'] = True

        # Check the goal
        if not self.path_in_goal(path):
            violations += 1
            details['goal_violation'] = True

        for point in path:
            if not self.in_environment(point):
                violations += 1
                details['environment_violation_count'] += 1
            
            for obstacle in self.obstacles:
                if obstacle.in_collision(point, self.robot_radius):
                    violations += 1
                    details['collision_violation_count'] += 1

        details['environment_violation'] = details['environment_violation_count'] > 0
        details['collision_violation'] = details['collision_violation_count'] > 0
        
        return violations, details

    # Method to check if a path is valid
    def path_is_valid(self, path):
        return self.count_violations(path) == 0
    
    # Compute the length of a path
    def path_length(self, path):
        length = 0
        for i in range(len(path) - 1):
            length += np.linalg.norm(path[i] - path[i + 1])
        return length
    

class Obstacle:
    """Class to represent an obstacle in the environment."""

    # Constructor
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    # Method to check if a point is in collision with the obstacle
    def in_collision(self, point, robot_radius=0):
        return np.linalg.norm(point - self.center) <= self.radius + robot_radius
    
