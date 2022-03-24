#!/bin/bash

#SBATCH --account=bdlds05
#SBATCH --time=6:0:0
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --array=0-2

module load cuda

source /nobackup/projects/bdlds05/rsstone/miniconda/etc/profile.d/conda.sh
conda activate pyvis

path_to_code="../code/main.py"
task_id=0


ALPHAS=(0.001 0.01 0.1)


for a in "${ALPHAS[@]}"
do
	if [ $task_id = $SLURM_ARRAY_TASK_ID ]
	then
		echo $task_id
		echo "alpha is $a"
		# task
		python $path_to_code --run_mode "train" --epochs 100 --alpha $a

		exit 0
	fi
	let task_id=$task_id+1
done