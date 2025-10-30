import matplotlib.pyplot as plt
from utils import format_weights,move_neighbor_uc, reindex, print_bins, heuristic_uc, worst, first_fit, random_restart, calculate_neighbors, calculate_neighbors_uc, SAHC_uc, SMHC_uc, RRHC_uc, SHC_uc, simmulated_annealing_uc, genetic_algorithm_uc, mutate, repair_bin_uc, crossover_uc, lower_bound 
import globals_data
import numpy as np
import math

# Jalankan algoritma
# test case
# weights_1 = [2, 5, 4, 7, 1, 3, 6, 8, 9, 2, 5, 3, 7, 4, 6, 1, 8, 9, 2, 5]
# weights_2 = [1, 2, 1, 3, 2, 4, 3, 1, 2, 3, 4, 2, 1, 3, 2, 4, 3, 1, 2, 3]
# weights_3 = [2, 5, 4, 7, 1, 3, 6, 8, 9, 2, 5, 3, 7, 4, 6, 1, 8, 9, 2, 5, 3, 7, 2, 4, 5]

# formatted = format_weights(weights_3)
# c = 10
# result_arr = []
# bin_awal = worst(formatted, c)
#final_bin = simmulated_annealing_uc(bin_awal, 200, 100)
# final_bin = genetic_algorithm_uc(bin_awal, 10, 10, 10, 10, c, formatted)
# print_bins(final_bin)
# print(heuristic_uc(final_bin))
# final_bin = genetic_algorithm_uc(bin_awal, 10, 10, 10, 20, c, formatted)

# for i in range(5):
#     final_bin = genetic_algorithm_uc(bin_awal, 10, 20, 10, 20, c, formatted)
#     #genetic_algorithm_uc(bin, population_size, generations, mutation_rate, fitness_threshold, c, formatted_weights)
#     # Ambil data dari global list
#     # iters = [x[0] for x in globals_data.display_genetic]
#     # heur_values = [x[1] for x in globals_data.display_genetic]
#     result_arr.append(heuristic_uc(final_bin))
    
# mean = np.mean(result_arr)
# std = np.std(result_arr)
# print(result_arr)
# print(mean)
# print(std)
# print(f"Data {i}: mean = {mean:.2f}, std = {std:.2f}")
# iters = [x[0] for x in globals_data.display_heur]
# heur_values = [x[1] for x in globals_data.display_heur]
# # exp = [x[2] for x in globals_data.display_heur]

# #Plot grafik
# plt.figure(figsize=(8, 5))
# plt.plot(iters, heur_values, marker='o', linestyle='-', linewidth=2, label='H')
# plt.title('heur')
# plt.xlabel('iteration')
# plt.ylabel('H')
# plt.grid(True)
# plt.show() 

# plt.figure(figsize=(8, 5))
# plt.plot(iters, exp, marker='o', linestyle='-', linewidth=2, label='exp')
# plt.title('exp')
# plt.xlabel('iteration')
# plt.ylabel('exp')
# plt.grid(True)
# plt.show() 

# x = np.array([25, 50, 75, 100])
# y = np.array([18, 36, 18.6, 56.8])
# # Regresi linear
# b = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean())**2)
# a = y.mean() - b * x.mean()
# print(f"Regresi linear: y = {a:.2f} + {b:.2f}x")

# # Koefisien korelasi
# r = np.corrcoef(x, y)[0, 1]
# print(f"Koefisien korelasi r = {r:.3f}")
# b = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean())**2)
# a = y.mean() - b * x.mean()

# # Buat nilai y prediksi untuk garis regresi
# y_pred = a + b * x

# # Plot
# plt.scatter(x, y, color='blue', label='Data points')  # titik data
# plt.plot(x, y_pred, color='red', label=f'Regression line: y={a:.2f}+{b:.2f}x')  # garis regresi
# plt.xlabel('Temperature')
# plt.ylabel('H')
# plt.title('Scatter plot dengan regresi linear')
# plt.legend()
# plt.grid(True)
# plt.show()