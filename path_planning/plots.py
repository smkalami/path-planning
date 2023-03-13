import matplotlib.pyplot as plt

def plot_path(sol, ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()
    path = sol.get_path()
    path_line, = ax.plot(path[:,0], path[:,1], **kwargs)
    return path_line

def update_path(sol, path_line):
    path = sol.get_path()
    path_line.set_xdata(path[:,0])
    path_line.set_ydata(path[:,1])
    fig = plt.gcf()
    fig.canvas.draw()
    fig.canvas.flush_events()

def plot_environment(environment, ax=None, obstacles_style={}, start_style={}, goal_style={}):
    if ax is None:
        ax = plt.gca()

    ax.set_aspect('equal', adjustable='box')

    # Plot obstacles as circle
    if not 'color' in obstacles_style:
        obstacles_style['color'] = 'k'
    for obstacle in environment.obstacles:
        ax.add_patch(plt.Circle(obstacle.center, obstacle.radius, **obstacles_style))

    # Plot start
    if not 'color' in start_style:
        start_style['color'] = 'r'
    if not 'markersize' in start_style:
        start_style['markersize'] = 12
    ax.plot(environment.start[0], environment.start[1], 's', **start_style)

    # Plot goal
    if not 'color' in goal_style:
        goal_style['color'] = 'g'
    if not 'markersize' in goal_style:
        goal_style['markersize'] = 12
    ax.plot(environment.goal[0], environment.goal[1], 's', **goal_style)

    # Set axis limits
    ax.set_xlim([0, environment.width])
    ax.set_ylim([0, environment.height])

