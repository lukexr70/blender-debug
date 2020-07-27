#!/bin/bash
#SBATCH -p dgx
#SBATCH --time=1:00:00

singularity exec --nv ./niuvt.sif "$@"
