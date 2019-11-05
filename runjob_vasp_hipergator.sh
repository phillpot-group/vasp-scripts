#!/bin/bash
#SBATCH --job-name=CUSTOM    # Name of the job; only 8 characters will be visible on hipergator
#SBATCH --account=phillpot   # Account you are working under; always 'phillpot' unless you have access to another queue
#SBATCH --qos=phillpot       # Queue you are submitting to
#SBATCH --mail-type=CUTSOM   # events which will trigger an email notification; choose many from NONE,BEGIN,END,FAIL
#SBATCH --mail-user=CUSTOM   # email address to conteact in the event of a 'mail-type' event occuring
#SBATCH --ntasks=16          # Number of CPUs to use; 1 cpu per atom is a decent rule of thumb for vasp
#SBATCH -N 1                 # Number of nodes to use; each hipergator node contains 32 cpus; use the minimum number of nodes
#SBATCH --mem-per-cpu=CUSTOM # amount of memory to use on each cpu; refer to the notification emails to tune efficiency
#SBATCH --distribution=cyclic:cyclic # work distribution scheme
#SBATCH --time=24:00:00              # time limit for the job; hours:minutes:seconds
#SBATCH --output=job.out             # file which stdout is redirected to
#SBATCH --error=job.err              # file which stderr is redirected to

# This is the compile chain as of November 5, 2019.
module load intel/2016.0.109
module load impi/5.1.1

# $VASP_BIN should point to the location of your VASP executable
srun --mpi=pmi2 $VASP_BIN > vasp.log
