import numpy as np
from copy import deepcopy

# Particle Swarm Optimization
def PSO(problem, **kwargs):

    max_iter = kwargs.get('max_iter', 100)
    pop_size = kwargs.get('pop_size', 100)
    c1 = kwargs.get('c1', 1.4962)
    c2 = kwargs.get('c2', 1.4962)
    w = kwargs.get('w', 0.7298)
    wdamp = kwargs.get('wdamp', 1.0)
    callback = kwargs.get('callback', None)
    resetting = kwargs.get('resetting', None)
    
    # Empty Particle Template
    empty_particle = {
        'position': None,
        'velocity': None,
        'cost': None,
        'details': None,
        'best': {
            'position': None,
            'cost': np.inf,
            'details': None,
        },
    }

    # Extract Problem Info
    cost_function = problem['cost_function']
    var_min = problem['var_min']
    var_max = problem['var_max']
    num_var = problem['num_var']
    
    # Initialize Global Best
    gbest = {
        'position': None,
        'cost': np.inf,
        'details': None,
    }

    # Create Initial Population
    pop = []
    for i in range(0, pop_size):
        pop.append(deepcopy(empty_particle))
        pop[i]['position'] = np.random.uniform(var_min, var_max, num_var)
        pop[i]['velocity'] = np.zeros(num_var)
        pop[i]['cost'], pop[i]['details'] = cost_function(pop[i]['position'])
        pop[i]['best']['position'] = deepcopy(pop[i]['position'])
        pop[i]['best']['cost'] = pop[i]['cost']
        pop[i]['best']['details'] = pop[i]['details']
        
        if pop[i]['best']['cost'] < gbest['cost']:
            gbest = deepcopy(pop[i]['best'])
        
    # PSO Loop
    for it in range(0, max_iter):
        do_resetting = resetting and ((it + 1) % resetting == 0)
        if do_resetting:
            print('Resetting particles...')

        for i in range(0, pop_size):
            
            if do_resetting:
                pop[i]['position'] = np.random.uniform(var_min, var_max, num_var)
                pop[i]['velocity'] = np.zeros(num_var)

            else:
                pop[i]['velocity'] = w*pop[i]['velocity'] \
                    + c1*np.random.rand(num_var)*(pop[i]['best']['position'] - pop[i]['position']) \
                    + c2*np.random.rand(num_var)*(gbest['position'] - pop[i]['position'])

                pop[i]['position'] += pop[i]['velocity']
                pop[i]['position'] = np.clip(pop[i]['position'], var_min, var_max)

            pop[i]['cost'], pop[i]['details'] = cost_function(pop[i]['position'])
            
            if pop[i]['cost'] < pop[i]['best']['cost']:
                pop[i]['best']['position'] = deepcopy(pop[i]['position'])
                pop[i]['best']['cost'] = pop[i]['cost']
                pop[i]['best']['details'] = pop[i]['details']

                if pop[i]['best']['cost'] < gbest['cost']:
                    gbest = deepcopy(pop[i]['best'])

        w *= wdamp
        print('Iteration {}: Best Cost = {}'.format(it + 1, gbest['cost']))
        
        if callable(callback):
            callback({
                'it': it + 1,
                'gbest': gbest,
                'pop': pop,
            })

    return gbest, pop
