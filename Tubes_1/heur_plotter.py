from utils import format_weights,move_neighbor_uc, reindex, print_bins, heuristic_uc, worst, first_fit, random_restart, calculate_neighbors, calculate_neighbors_uc, SAHC_uc, SMHC_uc, RRHC_uc, SHC_uc, simmulated_annealing_uc, genetic_algorithm_uc, mutate, repair_bin_uc, crossover_uc   

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

weight = [9,2,5,4,7,1,3,8,6,2,5,4,7,1,3,8,6]
formatted = format_weights(weight)
c = 10
bins = worst(formatted, c)
print_bins(genetic_algorithm_uc(bins, 10, 10, 10, 20, c, formatted))