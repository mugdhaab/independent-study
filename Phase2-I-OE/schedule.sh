#!/bin/bash
#SBATCH --account marasovic-gpu-np
#SBATCH --partition marasovic-gpu-np
#SBATCH --ntasks-per-node=32
#SBATCH --nodes=1
#SBATCH --gres=gpu:a100:1
#SBATCH --time=8:00:00
#SBATCH --mem=160GB
#SBATCH --mail-user=mugdha.abhyankar@utah.edu
#SBATCH --mail-type=FAIL,END


conda activate venv

wandb disabled
export TRANSFORMER_CACHE="/scratch/general/vast/u1409693/huggingface_cache"

python3 flant5.py --model flan-t5-large --shot 2  --task I-E-O