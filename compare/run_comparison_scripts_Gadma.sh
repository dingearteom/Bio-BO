#!/usr/bin/env bash

objective_names=(1_Bot_4_Sim 2_ExpDivNoMig_5_Sim 2_DivMig_5_Sim 2_BotDivMig_8_Sim 3_DivMig_8_Sim 4_DivNoMig_9_Sim 4_DivMig_11_Sim 4_DivMig_18_Sim 5_DivNoMig_9_Sim)

for i in "${objective_names[@]}"; do
  echo "Gadma on $i is being executed"
  python3 -m compare.Comparison_script_Gadma "${i}" 50 300
done