import matplotlib.pyplot as plt
from utils import format_weights,move_neighbor_uc, reindex, print_bins, heuristic_uc, worst, first_fit, random_restart, calculate_neighbors, calculate_neighbors_uc, SAHC_uc, SMHC_uc, RRHC_uc, SHC_uc, simmulated_annealing_uc, genetic_algorithm_uc, mutate, repair_bin_uc, crossover_uc   
import globals_data

# weight = [9, 2, 5, 4, 7, 1, 3, 8, 6, 2, 5, 4, 7, 1, 3, 8, 6]
# weight = [9, 2, 5, 4, 7, 1]
# formatted_weights = format_weights(weight)
# c = 10
# print("Jumlah bin dengan first fit : ",firstFit(formatted_weights, c))
# print_bins(firstFit(formatted_weights, c))
# print("Heuristic (total ruang kosong):", heuristic(firstFit(formatted_weights, c)))
# print_bins(SMHC(firstFit(formatted_weights, c), 100, 10))
# print_bins(SHC(firstFit(formatted_weights, c), 100))
# print_bins(worst(formatted_weights, c))
# print_bins(RRHC_uc(worst(formatted_weights, c), 100, 10))

#def Genetic_algorithm_uc(bin, population_size, generations, mutation_rate dalam persen , fitness_threshold dalam persen, c):
# print_bins(genetic_algorithm_uc(worst(formatted_weights, c), 10, 10, 10, 20, 10))

# weight = [9,2,5,4,7,1,3,8,6,2,5,4,7,1,3,8,6]
# formatted = format_weights(weight)
# c = 10
# bins = worst(formatted, c)
# print_bins(genetic_algorithm_uc(bins, 10, 10, 10, 20, c, formatted))

# Jalankan algoritma
# test case
weights_1 = [2, 5, 4, 7, 1, 3, 6, 8, 9, 2, 5, 3, 7, 4, 6, 1, 8, 9, 2, 5]
weights_2 = [1, 2, 1, 3, 2, 4, 3, 1, 2, 3, 4, 2, 1, 3, 2, 4, 3, 1, 2, 3]
weights_3 = [2, 5, 4, 7, 1, 3, 6, 8, 9, 2, 5, 3, 7, 4, 6, 1, 8, 9, 2, 5, 3, 7, 2, 4, 5]
weights_4 = [9, 8, 2, 2, 2, 2]
formatted = format_weights(weights_4)
c = 10
bin_awal = worst(formatted, c)
final_bin = SMHC_uc(bin_awal, 100, 30)

# Ambil data dari global list
iters = [x[0] for x in globals_data.display_heur]
heur_values = [x[1] for x in globals_data.display_heur]

# Plot grafik
plt.figure(figsize=(8, 5))
plt.plot(iters, heur_values, marker='o', linestyle='-', linewidth=2)
plt.title('Heuristic growth over iteration (Steepest Ascent Hill Climbing)')
plt.xlabel('Iteration')
plt.ylabel('Value Heuristic (Inverted)')
plt.grid(True)
plt.show() 
#print_bins(final_bin)
print(heuristic_uc(final_bin))