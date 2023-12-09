#!/bin/bash -e
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --time=02:00:00
#SBATCH --job-name=jobName
#SBATCH --output=slurm_%j.out
#SBATCH --error=slurm_%j.err
#SBATCH --chdir=/scratch/sca321/cloud/proj2/cloud-and-ml-RAG
#SBATCH --mem-per-cpu=24G
#SBATCH --gres=gpu:1

module purge


singularity exec --nv --overlay /scratch/sca321/cloud/proj2/conda/overlay-50G-10M.ext3:ro \
	    /scratch/work/public/singularity/cuda11.6.124-cudnn8.4.0.27-devel-ubuntu20.04.4.sif  \
	    /bin/bash -c "source /ext3/env.sh; python train.py --config configs/Depth-L.yml;"
