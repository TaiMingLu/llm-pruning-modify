#!/bin/bash

conda create -n wanda python=3.9 -y
conda activate wanda

conda install pytorch==1.10.1 torchvision==0.11.2 torchaudio==0.10.1 cudatoolkit=11.3 -c pytorch -c conda-forge
pip install "numpy<2" "pyarrow<14.0.0" transformers==4.43.3 datasets==2.11.0 wandb sentencepiece accelerate==0.31.0

# conda create -n wanda-eval python=3.9 -y
# conda activate wanda-eval
# cd lm-evaluation-harness 
# pip install -e .