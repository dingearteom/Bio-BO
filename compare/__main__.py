from compare.Draw_comparison import DrawComparison


objective_names = ['1_Bot_4_Sim', '2_ExpDivNoMig_5_Sim', '2_DivMig_5_Sim']
for objective_name in objective_names:
    model = DrawComparison(f'Y_best_BayesianOptimization_{objective_name}_saved',
                           f'Y_best_Gadma_{objective_name}_saved', f'comparison_{objective_name}', real=False)
    model.draw()
