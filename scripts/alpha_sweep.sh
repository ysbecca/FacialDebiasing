#!/bin/bash

#SBATCH --account=bdlds05
#SBATCH --time=6:0:0
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --gres=gpu:1

module load cuda

source /nobackup/projects/bdlds05/rsstone/miniconda/etc/profile.d/conda.sh
conda activate pyvis

path_to_code="../code/main.py"


python $path_to_code --run_mode "train" --epochs 100 --alpha 0.001