# Python program to find number of bins required using
# First Fit algorithm.
# Kode first fit dimodifikasi dari https://www.geeksforgeeks.org/dsa/bin-packing-problem-minimize-number-of-used-bins/
# Ditulis ulang oleh: Dennis Hubert
import copy
import random
import math
import globals_data
from globals_data import reset_globals, reset_gen
# Fungsi format mapping dari array[int] -> array[dict]

def format_weights(weight):
  format_weights = [
    {
      "id": f"BRG{index+1:03d}",  # 3-digit number, e.g. BRG001
      "ukuran": w
    }
      for index, w in enumerate(weight)
  ]
  return(format_weights)

def move_neighbor_uc(bin_rem, i, j, k):
    barang = bin_rem[j]['barang'].pop(k)

    bin_rem[i]['barang'].append(barang)

    # Update remaining dan total
    bin_rem[i]['remaining'] -= barang['ukuran']
    bin_rem[i]['total'] += barang['ukuran']
    bin_rem[j]['remaining'] += barang['ukuran']
    bin_rem[j]['total'] -= barang['ukuran']

    # Hapus kontainer jika sudah kosong
    if len(bin_rem[j]['barang']) == 0:
        bin_rem.pop(j)

    return bin_rem

def reindex(bin_rem):
  for index, b in enumerate(bin_rem):
    b['kontainer'] = f'Kontainer {index+1}'

# Fungsi untuk mencetak isi bin
def print_bins(bin_rem):
  reindex(bin_rem)
  for b in bin_rem:
    print(f"{b['kontainer']} (total: {b['total']})")
    for item in b['barang']:
      print(f"  * {item['id']} ({item['ukuran']})")

def heuristic_uc(bin_rem):
# Jika jumlah bin konstan, total ruang kosong selalu konstant. sehingga jumlah bin tidak perlu dihitung pada heuristic
# sum(remaining) = c * len(bin_rem) - sum(total) 
  h = 0
  for b in bin_rem:
    if (b['remaining'] < 0):
      h += abs(b['remaining']) * 10 # penalti 10x untuk overfill
    else:
      h += b['remaining'] # total ruang kosong
  return (h)
    

def worst(weight, c):
    n = len(weight)
    # List dari bin yang digunakan
    bin_rem = [] 
    # Meletakkan item satu per satu
    for i in range(n):
      new_bin = {
          'kontainer': f'Kontainer {i+1}',
          'remaining': c - weight[i]['ukuran'],
          'total': weight[i]['ukuran'],
          'barang': [weight[i]]
      }
      bin_rem.append(new_bin)
    
    return bin_rem

# Fungsi untuk inisialisasi bin (First Fit)
def first_fit(weight, c):

  n = len(weight)
  res = 0

  # List dari bin yang digunakan
  bin_rem = [] 

  # Meletakkan item satu per satu
  for i in range(n):
    placed = False

    # Meletakan item di bin yang ada
    for j in range(res):
      if bin_rem[j]['remaining'] >= weight[i]['ukuran']:
        # meletakkan Item di bin yang ada
        bin_rem[j]['barang'].append(weight[i])
        bin_rem[j]['remaining'] -= weight[i]['ukuran']
        bin_rem[j]['total'] += weight[i]['ukuran']
        placed = True
        break

    # Buat bin baru jika item tidak muat di bin yang ada
    if not placed:
      new_bin = {
          'kontainer': f'Kontainer {res+1}',
          'remaining': c - weight[i]['ukuran'],
          'total': weight[i]['ukuran'],
          'barang': [weight[i]]
      }
      bin_rem.append(new_bin)
      res += 1
        
  return bin_rem

def random_restart(bin, c):
    weight = [item for sublist in [b['barang'] for b in bin] for item in sublist]
    n = len(weight)
    # List dari bin yang digunakan
    bin_rem = [] 
    # Meletakkan item secara random
    random.shuffle(weight)
    for i in range(n):
      new_bin = {
          'kontainer': f'Kontainer {i+1}',
          'remaining': c - weight[i]['ukuran'],
          'total': weight[i]['ukuran'],
          'barang': [weight[i]]
      }
      bin_rem.append(new_bin)
    return bin_rem

def calculate_neighbors(bin_rem):
  states = []
  for i in bin_rem:
    for j in bin_rem:
      for k in range(len(j['barang'])):
        if i != j:
          new_state = move_neighbor_uc(copy.deepcopy(bin_rem), bin_rem.index(i), bin_rem.index(j), k)
          states.append([new_state, heuristic_uc(new_state)])
  return states

def calculate_neighbors_uc(bin_rem):
  states = []
  for i in bin_rem:
    for j in bin_rem:
      for k in range(len(j['barang'])):
        if i != j:
          new_state = move_neighbor_uc(copy.deepcopy(bin_rem), bin_rem.index(i), bin_rem.index(j), k)
          states.append([new_state, heuristic_uc(new_state)])
  return states

def SAHC_uc(bin, iterasi):
  reset_globals()
  for i in range(iterasi):
    current = heuristic_uc(bin)
    globals_data.display_heur.append((i, current))
    if current == 0:
      break
    # Hitung semua neighbor
    neighbors = calculate_neighbors_uc(bin)

    # Temukan neighbor terbaik (heuristic terkecil)
    best_neighbor, best_value = min(neighbors, key=lambda x: x[1])

    # lakukan steepest descent jika ada perbaikan
    if best_value < current:
      bin = best_neighbor
      
    else:
      # print(f"Iterasi ke-{i+1}: tidak ada perbaikan (H={current})")
      break
  return bin

def SMHC_uc(bin, iterasi, Max_no_improve):
  reset_globals()
  sidestep = 0
  i = 0
  while (i < iterasi and sidestep < Max_no_improve):
    current = heuristic_uc(bin)
    globals_data.display_heur.append((i, current))
    if current == 0:
      print(f"Iterasi ke-{i+1}: solusi optimal ditemukan (H=0)")
      globals_data.display_heur.append(current)
      break
    # Hitung semua neighbor
    neighbors = calculate_neighbors_uc(bin)

    # Temukan neighbor terbaik (heuristic terkecil)
    best_neighbor, best_value = min(neighbors, key=lambda x: x[1])
    
    # lakukan steepest descent jika ada perbaikan atau sidestep
    if best_value < current:
      bin = best_neighbor
      print(f"Iterasi ke-{i+1}: perbaikan ditemukan (H={best_value})")
    elif (best_value == current):
      bin = best_neighbor
      print(f"Iterasi ke-{i+1}: sidestep dilakukan (H={best_value})")
      sidestep += 1
    else:
      print(f"Iterasi ke-{i+1}: tidak ada perbaikan (H={current})")
      sidestep += 1
    i += 1
  return bin

def RRHC_uc(bins, iterasi, Max_no_improve):
  reset_globals()
  restart = 0
  i = 0
  best_bin = bins
  best_bin_value = heuristic_uc(bins)
  while i < iterasi and restart < Max_no_improve:
    current = heuristic_uc(bins)
    globals_data.display_heur.append((i, current, best_bin_value))
    if current == 0:
      print(f"Iterasi ke-{i+1}: solusi optimal ditemukan (H=0)")
      globals_data.display_heur.append((i, heuristic_uc(bin)))
      break
    # Hitung semua neighbor
    neighbors = calculate_neighbors(bins)

    # Temukan neighbor terbaik (heuristic terkecil)
    best_neighbor, best_value = min(neighbors, key=lambda x: x[1])

    # lakukan steepest descent jika ada perbaikan
    if (best_value < current):
      bins = best_neighbor
      print(f"Iterasi ke-{i+1}: perbaikan ditemukan (H={best_value})")
      if best_value < best_bin_value:
        best_bin = best_neighbor
        best_bin_value = best_value
        print(f"Solusi terbaik diperbarui (H={best_bin_value})")
    else:
    # restart jika tidak ada perbaikan 
      print(f"Iterasi ke-{i+1}: tidak ada perbaikan (H={best_bin_value}), melakukan random restart")
      bins = random_restart(bins, 10)
      restart += 1
    i += 1
  return (best_bin)

def SHC_uc(bin, iterasi):
  for i in range(iterasi):
    current = heuristic_uc(bin)
    globals_data.display_heur.append((i, current))
    if current == 0:
      print(f"Iterasi ke-{i+1}: solusi optimal ditemukan (H=0)")
      globals_data.display_heur.append(heuristic_uc(bin))
      break
    # Hitung semua neighbor
    neighbors = calculate_neighbors(bin)

    # Temukan neighbor secara random
    best_neighbor, best_value = random.choice(neighbors)

    # lakukan descent jika ada perbaikan
    if best_value < current:
      bin = best_neighbor
      print(f"Iterasi ke-{i+1}: perbaikan ditemukan (H={best_value})")
    else:
      print(f"Iterasi ke-{i+1}: tidak ada perbaikan (H={current})")
  return bin

def simmulated_annealing_uc(bin, iterasi, T=100):
  reset_globals()
  for i in range(iterasi):
    current = heuristic_uc(bin)
    globals_data.display_heur.append((i, current))
    if current == 0:
      print(f"Iterasi ke-{i+1}: solusi optimal ditemukan (H=0)")
      break
    # Hitung semua neighbor
    neighbors = calculate_neighbors(bin)
    next_state, next_value = random.choice(neighbors)
    deltaE = next_value - current
    
    if deltaE < 0:
      bin = next_state
      current = next_value
      print(f"Iterasi ke-{i+1}: perbaikan ditemukan (H={current})")
      

    else:
      # Jika lebih buruk, terima dengan probabilitas e^(-ΔE/T)
      p = math.exp(-deltaE / T)
      if random.random() < p:
        bin = next_state
        current = next_value
        print(f"Iterasi ke-{i+1}: diterima solusi lebih buruk (H={current}, p={p:.3f})")
      else:
        print(f"Iterasi ke-{i+1}: ditolak (H={current})")
    # Turunkan suhu
    T = T * 0.95
    globals_data.display_heur.append((i, heuristic_uc(bin)))
  return bin

def genetic_algorithm_uc(bin, population_size, generations, mutation_rate, fitness_threshold, c, formatted_weights):
  parents = []
  best_overall = {'Fitness': float('-inf'),
    'bin': None}
  fitsum = 0
  reset_gen()
  for population in range(population_size):
    new_bin = SAHC_uc(random_restart(bin, c), 100)
    new_parent = {
        'Fitness': 100 / (1 + heuristic_uc(new_bin)),
        'bin': new_bin,
    }
    fitsum += new_parent['Fitness']
    parents.append(new_parent)
  for gen in range(generations):
    fitsum = 0
    # Inisialisasi populasi awal
    # normalisasi fitness
    for p in parents:
      p['Fitness'] = 100 / (1 + heuristic_uc(p['bin']))
    # Urutkan berdasarkan fitness
    parents = sorted(parents, key=lambda x: x['Fitness'], reverse=True)
    # Pilih 20% terbaik
    top = math.ceil(population_size * fitness_threshold/100)  # ceil agar minimal 1 elemen
    selected = parents[:top]
    # lakukan crossover dan mutasi untuk membuat populasi baru
    children = crossover_uc(selected, population_size, c, formatted_weights)
    parents = mutate(children, mutation_rate)
    best = max(parents, key=lambda x: x['Fitness'])
    globals_data.display_genetic.append((gen, best_overall['Fitness'], best['Fitness']))
    if best['Fitness'] > best_overall['Fitness']:
      best_overall = best
      print(f"Generasi ke-{gen+1}: solusi terbaik diperbarui (Fitness={best_overall['Fitness']:.2f})")
    else:
      print(f"Generasi ke-{gen+1}: tidak ada perbaikan (Fitness={best_overall['Fitness']:.2f})")
  return(best_overall['bin'])

def mutate(children, mutation_rate):
  for child in children:
    if random.random() * 100 < mutation_rate:
      bins = child['bin']  
      # Pilih satu bin secara acak
      if len(bins) > 0:
        selected_bin = random.choice(bins)
        barang_list = selected_bin['barang']

        # Pastikan ada minimal 2 barang untuk ditukar
        if len(barang_list) >= 2:
          # Pilih dua indeks acak yang berbeda
          i, j = random.sample(range(len(barang_list)), 2)
          
          # Tukar posisi barang
          barang_list[i], barang_list[j] = barang_list[j], barang_list[i]
  return children

def repair_bin_uc(child, c, formatted_weights):
    bins = child

    # Kumpulkan semua item yang ada di setiap bin
    all_items = []
    for b in bins:
        for item in b['barang']:
            all_items.append(item)

    # Hilangkan duplikasi berdasarkan ID
    seen = set() # untuk melacak ID yang sudah ditemui
    unique_items = []
    for item in all_items:
        if item['id'] not in seen:
            seen.add(item['id'])
            unique_items.append(item)

    # Temukan item yang hilang
    missing_items = [i for i in formatted_weights if i['id'] not in seen]

    for b in bins:
        b['barang'].clear()
        b['total'] = 0
        b['remaining'] = c

    # Masukkan kembali item satu per satu
    for item in unique_items + missing_items:
      for b in bins:
        if b['remaining'] >= item['ukuran']:
            b['barang'].append(item)
            b['total'] += item['ukuran']
            b['remaining'] -= item['ukuran']
            break
    # lakukan kembali Steepest ascend hill climbing untuk memperbaiki overfill
    bins = SAHC_uc(bins, 50)
    
    # Update fitness dan bin
    child_repaired = {
    'bin': bins,
    'Fitness': heuristic_uc(bins)
    }
    return child_repaired

def crossover_uc(selected, population_size, c, formatted_weights):
  children = []
  for population in range(population_size//2):
    # pilih dua parent secara random
    parent1 = random.choice(selected)
    parent2 = random.choice(selected)
    
    # Tentukan titik crossover
    min_len = min(len(parent1['bin']), len(parent2['bin']))
    if min_len <= 1:
      continue  # skip kalau cuma 1 bin

    cross_point = random.randint(1, min_len - 1)
    # Crossover satu titik
    child_bin1 = parent1['bin'][:cross_point] + parent2['bin'][cross_point:]
    child_bin2 = parent2['bin'][:cross_point] + parent1['bin'][cross_point:]
    child1  = repair_bin_uc(child_bin1, c, formatted_weights)
    child2  = repair_bin_uc(child_bin2, c, formatted_weights)
    children.append(child1)
    children.append(child2)
  return children

# contoh penggunaan
if __name__ == "__main__":
    weight = [9,2,5,4,7,1,3,8,6,2,5,4,7,1,3,8,6]
    formatted = format_weights(weight)
    c = 10
    bins = worst(formatted, c)
    print_bins(genetic_algorithm_uc(bins, 10, 10, 10, 20, c, formatted))
