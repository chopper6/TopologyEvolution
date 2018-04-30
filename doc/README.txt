topologyEvolution is a project to evolve a population of networks to minimize the difficulty of NP-Hard instances

note that some features have not been tested for awhile, these are marked by (!)
in less elegant cases, asserts may be used to ensure that certain parameter combos are not used (since not yet implemented)


OTHER DETAILS
- workers only execute 1 generation and have a static population size
- note that if stop_condition = size, must include a grow_frequency mutation > 0 
- instances.py is very outdated. If you want to record data on knapsack instances it will need to be reworked


PARAMETER DETAILS

# files
KP_solver_source         = full path
KP_solver_binary         = full path
output_directory         = full path


# general
debug 				boolean; sequential run without mpi, often easier to debug
directed			boolean, directed or undirected graph (if false two nodes can only share one edge)
single_cc			boolean, maintain single connected component


# knapsack
pressure			% of nodes or edges that are in the knapsack problem (0-100)
tolerance			number of damages allowed in knapsack solution
advice_on			= nodes | edges; which objects knapsack problem is applied to  
BD_criteria              	= both|source|target, which nodes are benefits and damages are allocated to
sampling_rounds_multiplier	# instances = # nodes | edges * sampling_rounds_multiplier
sampling_rounds_max		caps # instances


# start and stop
initial_net_type        = random | load; load uses network_file parameter
		 	  other options available, but have not been used for awhile see init_nets.py
starting_size           = #nodes
stop_condition		= generation | size; determines which of the following configs are relevant
ending_size             = #nodes
max_generations         
edge_to_node_ratio     

network_file  = /home/2014/choppe1/Documents/EvoNet/virt_workspace/data/output/108_lowDeg/rewire_attempt_contd/nets/1200


# population
number_of_workers       
num_worker_nets         
percent_survive         percent of total population used for next generation


# output
num_data_output     	comprised of degree distribution and several features
num_net_output        	full net is output, can be used for 'load'


# fitness
leaf_metric             = RGAR; can add other options if desired
leaf_power              = 2; leaf_metric is exponentially weighted relative to hub_metric
hub_metric              = ETB; can also use control|Bin, the later is along the lines of direct (first-order) evolution
fitness_operation       = multiply; can also use leaf|hub|add|power
fitness_direction       = max|min


# bias
biased                   boolean; bias the distribution of states
bias_on                  nodes | edges; does not need to be the same as pressure_on, although may make more sense if so
global_edge_bias         all objects have this same bias
bias_distribution        = uniform, normal, see bias.py for more; all objects have the same distribution (but may vary between one another)


# mutation				all mutations are per generation, if < 1 there is a probabilistic chance that they occur
add_edge_mutation_frequency     	(!)
remove_edge_mutation_frequency  	(!)
rewire_mutation_frequency       	(frequently used)
sign_mutation_frequency         	(!)
reverse_edge_mutation_frequency 	(!)
grow_mutation_frequency         	(!)
shrink_mutation_frequency       	(frequently used)


# partially implemented 		these remain in case future changes desire multiple simulations, possibly with the same advice (~ direct evolution)
num_sims	= 1			(!)
advice_creation	= each			(!)



