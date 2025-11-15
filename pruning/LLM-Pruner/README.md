# LLM-Pruner

## Installation
```bash
bash scripts/install.sh
```

## Pruning
```bash
bash scripts/prune_llama-7b.sh
bash scripts/prune_llama2-7b.sh
bash scripts/prune_llama3.1-8b.sh
```

## Results
Base Model=Llama-7B; Ratio=0.25
| Source | Method | Importance Estimation | WikiText2 | PTB | BoolQ | PIQA | Hellaswag | Winogrande | ARC-E | ARC-C | OBQA | 
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Paper | -       | -         | 12.6 | 22.1 | 73.2 | 78.4 | 73.0 | 67.0 | 67.5 | 41.4 | 42.4 |
| Ours  | -       | -         | 12.6 |      | 73.1 | 78.4 | 73.0 | 67.1 | 67.5 | 41.4 | 42.4 |
| Paper | Block   | Element 1 | 19.1 |      | 57.1 | 75.7 | 66.8 | 59.8 | 60.9 | 36.5 | 40.0 |
| Ours  | Block   | Element 1 | 
| Paper | L2      | -         | 582  | 1022 | 59.8 | 58.0 | 37.0 | 52.4 | 33.1 | 28.6 | 29.8 | 
| Ours  | L2      | -         | 753  | 1167 | 60.2 | 58.7 | 37.1 | 53.2 | 32.9 | 27.8 | 29.8 |
| Paper | Random  | -         | 27.5 | 43.2 | 61.8 | 71.3 | 58.3 | 54.5 | 57.1 | 32.9 | 35.0 |
| Ours  | Random  | -         | 12.4 | 63.8 | 62.0 | 70.8 | 57.9 | 58.1 | 52.3 | 32.4 | 38.0 |
| Paper | Channel | -         | 74.6 | 154  | 62.8 | 62.7 | 41.4 | 51.1 | 41.4 | 27.9 | 30.4 |  
| Ours  | Channel | -         |
| Paper | Block   | Element 1 | 19.1 | 34.2 | 57.1 | 75.7 |	66.8 | 59.8 | 60.9 | 36.5 | 40.0 |
| Ours  | Block   | Element 1 | 10.6 | 52.9 | 
| Paper | Block   | Element 2 | 19.8 | 36.7 | 59.4 | 75.6 | 65.3 | 61.3 | 59.2 | 37.1 | 39.8 |
| Ours  | Block   | Element 2 | 
| Paper | Block   | Vector    | 22.3 | 41.8 | 61.4 | 71.7 | 57.3 | 54.2 | 55.8 | 34.0 | 38.4 |
| Ours  | Block   | Vector    | 