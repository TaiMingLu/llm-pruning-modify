#!/bin/bash

set -euo pipefail

source /usr/local/anaconda3/2024.02/etc/profile.d/conda.sh
conda activate wanda

methods=(
    wanda
    sparsegpt
    magnitude
)

sparsities=(
    unstructured
    2:4
    4:8
)

PROJ_DIR=$(pwd)
# model_path=meta-llama/Llama-3.1-8B
model_path=/n/fs/vision-mix/yx1168/model_ckpts/Llama-3.1-8B
model_name=$(basename ${model_path})
save_dir=${PROJ_DIR}/../../checkpoints
log_dir=${PROJ_DIR}/outputs

cd $PROJ_DIR/src
for method in "${methods[@]}"; do
    for sparsity in "${sparsities[@]}"; do
        echo "[INFO] Pruning with method: $method and sparsity: $sparsity"
        python main.py \
            --model ${model_path} \
            --prune_method ${method} \
            --sparsity_ratio 0.5 \
            --sparsity_type ${sparsity} \
            --save ${log_dir}/${method}/${sparsity}/ \
            --save_model ${save_dir}/${method}/${model_name}_${method}_${sparsity} \
            --eval_zero_shot
    done
done