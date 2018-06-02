import math
import reducer, solver, fitness, util
from ctypes import cdll

def pressurize(configs, Net, instance_file_name, advice):
    # configs:
    pressure = math.ceil((float(configs['pressure']) / 100.0))
    sampling_rounds_multiplier = float(configs['sampling_rounds_multiplier']) #FRACTION of curr number of EDGES
    if (util.is_it_none(configs['sampling_rounds_max']) == None): max_sampling_rounds = None
    else: max_sampling_rounds = int(configs['sampling_rounds_max'])
    knapsack_solver = cdll.LoadLibrary(configs['KP_solver_binary'])
    advice_upon = configs['advice_upon']
    leaf_metric = str(configs['leaf_metric'])
    leaf_pow = float(configs['leaf_power'])
    hub_metric = str(configs['hub_metric'])
    fitness_operator = str(configs['fitness_operation'])

    net = Net.net #not great syntax, but Net is an individual in a population, whereas net is it's graph representation

    #num_samples_relative = min(max_sampling_rounds, len(net.nodes()) * sampling_rounds)
    num_samples_relative = max(1, int(len(net.edges())*sampling_rounds_multiplier) )
    if (max_sampling_rounds): num_samples_relative = min(num_samples_relative, max_sampling_rounds)

    if (advice_upon =='nodes'): pressure_relative = int(pressure * len(net.nodes()))
    elif (advice_upon =='edges'): pressure_relative = int(pressure * len(net.edges()))
    else:
        print("ERROR in pressurize(): unknown advice_upon: " + str(advice_upon))
        return


    leaf_fitness, hub_fitness, solo_fitness = 0, 0, 0
    reset_BDs(net)

    kp_instances = reducer.reverse_reduction(net, pressure_relative, num_samples_relative, advice, configs)

    if (instance_file_name != None): open(instance_file_name, 'w')

    for kp in kp_instances:
        a_result = solver.solve_knapsack(kp, knapsack_solver)
        inst_solo_fitness, inst_leaf_fitness, inst_hub_fitness = fitness.kp_instance_properties(a_result, leaf_metric, leaf_pow, hub_metric, fitness_operator, net, instance_file_name)
        leaf_fitness += inst_leaf_fitness
        hub_fitness += inst_hub_fitness
        solo_fitness += inst_solo_fitness

    leaf_fitness /= num_samples_relative
    hub_fitness /= num_samples_relative
    solo_fitness /= num_samples_relative

    Net.fitness, Net.leaf_fitness, Net.hub_fitness = solo_fitness, leaf_fitness, hub_fitness


def reset_BDs(net):
    for n in net.nodes():
        net.node[n]['benefits'] = 0
        net.node[n]['damages'] = 0

