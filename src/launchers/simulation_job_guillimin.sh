#!/bin/bash
#PBS -l procs=64
#PBS -l walltime=01:00:00
#PBS -A ymj-002-aa

module load gcc/4.9.1
module load MKL/11.2
module load openmpi/1.8.3-gcc

echo 'simulating on Guillimin: python '$TOPEVO_SIMULATION_BATCH_ROOT' 64 '$TOPEVO_SIMULATION_CONFIGS

cd $TOPEVO_SIMULATION_DIRECTORY

python $TOPEVO_SIMULATION_BATCH_ROOT 64 $TOPEVO_SIMULATION_CONFIGS
