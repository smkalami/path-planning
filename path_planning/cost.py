from path_planning.solution import SplinePath
from path_planning.environment import Environment

START_VIOLATION_PENALTY = 1
GOAL_VIOLATION_PENALTY = 1
ENV_VIOLATION_PENALTY = 0.2
COLLISION_PENALTY = 1

def PathPlanningCost(sol: SplinePath):

    # Get path
    path = sol.get_path()

    # Length of path
    length = sol.environment.path_length(path)

    # Violations of path
    _, details = sol.environment.count_violations(path)

    # Cost
    cost = length

    # Add penalty for start violation
    if details['start_violation']:
        cost *= 1 + START_VIOLATION_PENALTY

    # Add penalty for goal violation
    if details['goal_violation']:
        cost *= 1 + GOAL_VIOLATION_PENALTY

    # Environment violation
    if details['environment_violation']:
        cost *= 1 + details['environment_violation_count']*ENV_VIOLATION_PENALTY

    # Collision violation
    if details['collision_violation']:
        cost *= 1 + details['collision_violation_count']*COLLISION_PENALTY

    # Add details
    details['sol'] = sol
    details['path'] = path
    details['length'] = length
    details['cost'] = cost
    
    return cost, details

def EnvCostFunction(environment: Environment, num_control_points=10, resolution=100):
    def CostFunction(xy):
        sol = SplinePath.from_list(environment, xy, resolution, normalized=True)
        return PathPlanningCost(sol)
    
    return CostFunction
