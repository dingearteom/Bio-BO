#!/usr/bin/env bash

objective_names=(3_DivMig_8_Sim 4_DivNoMig_9_Sim 4_DivMig_11_Sim 4_DivMig_18_Sim 5_DivNoMig_9_Sim)

for i in "${objective_names[@]}"; do
  echo "BayesianOptimization on $i is being executed"
  python3 -m compare.Comparison_script_BayesianOptimization "${i}" 50 300
done