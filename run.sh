#!/bin/bash
#/usr/bin/env

# note that number of threads = # workers + 1

if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters. Need #threads, then input_file."
fi

nohup mpirun --mca mpi_warn_on_fork 0 -n $1 python3 /home/2014/choppe1/Documents/TopologyEvolution/src/evolve_root.py /home/2014/choppe1/Documents/TopologyEvolution/data/input/$2 > /home/2014/choppe1/Documents/TopologyEvolution/data/output/slog &
