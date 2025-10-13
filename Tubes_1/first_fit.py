# Python program to find number of bins required using
# First Fit algorithm.
# Kode first fit dimodifikasi dari https://www.geeksforgeeks.org/dsa/bin-packing-problem-minimize-number-of-used-bins/
# Ditulis ulang oleh: Dennis Hubert
import copy
import random
import math
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

def move_neighbor(bin_rem, i, j, k):
    barang = bin_rem[j]['barang'].pop(k)

    # Pastikan kontainer tujuan masih cukup ruang
    if bin_rem[i]['remaining'] >= barang['ukuran']:
        bin_rem[i]['barang'].append(barang)

        # Update remaining dan total
        bin_rem[i]['remaining'] -= barang['ukuran']
        bin_rem[i]['total'] += barang['ukuran']
        bin_rem[j]['remaining'] += barang['ukuran']
        bin_rem[j]['total'] -= barang['ukuran']

        # Hapus kontainer jika sudah kosong
        if len(bin_rem[j]['barang']) == 0:
            bin_rem.pop(j)
    else:
        # balikkan barang ke kontainer asal jika tidak muat
        bin_rem[j]['barang'].insert(k, barang)

    return bin_rem

# Fungsi untuk mencetak isi bin
def print_bins(bin_rem):
  for b in bin_rem:
    print(f"{b['kontainer']} (total: {b['total']})")
    for item in b['barang']:
      print(f"  * {item['id']} ({item['ukuran']})")

# Fungsi heuristic: total ruang kosong
def heuristic(bin_rem):
# Jika jumlah bin konstan, total ruang kosong selalu konstant. sehingga jumlah bin tidak perlu dihitung pada heuristic
# sum(remaining) = c * len(bin_rem) - sum(total) 
  h = 0
  for b in bin_rem:
    h += b['remaining'] # total ruang kosong
  return (h)  
    
# Fungsi untuk inisialisasi bin (First Fit)
def firstFit(weight, c):
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

# Fungsi untuk inisialisasi bin (worst fit)
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

# Fungsi untuk menghitung semua neighbor
def calculate_neighbors(bin_rem):
  states = []
  for i in bin_rem:
    for j in bin_rem:
      for k in range(len(j['barang'])):
        if i != j:
          new_state = move_neighbor(copy.deepcopy(bin_rem), bin_rem.index(i), bin_rem.index(j), k)
          states.append([new_state, heuristic(new_state)])
  return states

# steepest ascent hill climbing
def SAHC(bin, iterasi):
  for i in range(iterasi):
    current = heuristic(bin)
    if current == 0:
      print(f"Iterasi ke-{i+1}: solusi optimal ditemukan (H=0)")
      break
    # Hitung semua neighbor
    neighbors = calculate_neighbors(bin)

    # Temukan neighbor terbaik (heuristic terkecil)
    best_neighbor, best_value = min(neighbors, key=lambda x: x[1])

    # lakukan steepest descent jika ada perbaikan
    if best_value < current:
      bin = best_neighbor
      print(f"Iterasi ke-{i+1}: perbaikan ditemukan (H={best_value})")
    else:
      print(f"Iterasi ke-{i+1}: tidak ada perbaikan (H={current})")
  return bin

# side move hill climbing
def SMHC(bin, iterasi, Max_no_improve):
  sidestep = 0
  i = 0
  while i < iterasi and sidestep < Max_no_improve:
    current = heuristic(bin)
    if current == 0:
      print(f"Iterasi ke-{i+1}: solusi optimal ditemukan (H=0)")
      break
    # Hitung semua neighbor
    neighbors = calculate_neighbors(bin)

    # Temukan neighbor terbaik (heuristic terkecil)
    best_neighbor, best_value = min(neighbors, key=lambda x: x[1])

    # lakukan steepest descent jika ada perbaikan atau sidestep
    if best_value <= current:
      bin = best_neighbor
      print(f"Iterasi ke-{i+1}: perbaikan ditemukan (H={best_value})")
    else:
      print(f"Iterasi ke-{i+1}: tidak ada perbaikan (H={current})")
      sidestep += 1
    i += 1
  return bin

# stochastic hill climbing
def SHC(bin, iterasi):
  for i in range(iterasi):
    current = heuristic(bin)
    if current == 0:
      print(f"Iterasi ke-{i+1}: solusi optimal ditemukan (H=0)")
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
    
# simmulated annealing 
def Simmulated_annealing(bin, iterasi, T=100):
  for i in range(iterasi):
    current = heuristic(bin)
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
  return bin
    



# Driver program
# weight = [2, 5, 4, 7, 1, 3, 8]
weight = [9,2,5,4,7,1,3,8,6,2,5,4,7,1,3,8,6]
formatted_weights = format_weights(weight)
c = 10
# print("Jumlah bin dengan first fit : ",firstFit(formatted_weights, c))
# print_bins(firstFit(formatted_weights, c))
# print("Heuristic (total ruang kosong):", heuristic(firstFit(formatted_weights, c)))
# print_bins(SMHC(firstFit(formatted_weights, c), 100, 10))
# print_bins(SHC(firstFit(formatted_weights, c), 100))
# print_bins(worst(formatted_weights, c))
print_bins(Simmulated_annealing(worst(formatted_weights, c), 100))