# -*- coding: utf-8 -*-

import csv
import numpy as np

# Número de usuarios y películas en el conjunto de datos
user_size = 943 + 1 # Pos 0 vacía, pero es más cómodo
item_size = 1682 + 1 # Pos 0 vacía

# Provisional - Usuario y film a predecir
pUser = 5
pItem = 20

# Settings
neighborhoodSize = 20

# Leemos el fichero u.data, y guardamos los resultados en una matriz
data = np.zeros((user_size, item_size), dtype=int)
with open('resources\\ml-100k\\u.data') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=' ')
    for row in csvreader:
        string = " ".join(row)
        split = string.split("\t")
        user = int(split[0])
        item = int(split[1])
        value = int(split[2])
        data[user][item] = value

# ------------------
# --- Predicción ---
# ------------------

# Calculamos la media de valoración del usuario
pUser_nRatings = np.count_nonzero(data[pUser])
pUserMean = data[pUser].sum() / pUser_nRatings
print(pUser_nRatings)
print(pUserMean)

# Calculo de vecindario
for nUser in range(user_size):
    if nUser == pUser:
        continue
    
    # Calculamos la media de valoración del usuario vecino
    nUser_nRatings = np.count_nonzero(data[nUser])
    nUserMean = data[nUser].sum() / nUser_nRatings
    
    # Operaciones de suma
    sumRatings1 = 0
    sumRatings2 = 0
    sumRatings3 = 0
    itemCount = 0
    
    for item in range(item_size):
        pUserValue = data[pUser][item]
        nUserValue = data[nUser][item]
        if pUserValue == 0 or nUserValue == 0:
            continue
        pUserValue -= pUserMean
        nUserValue -= nUserMean
        sumRatings1 += pUserValue * nUserValue
        sumRatings2 += pUserValue**2
        sumRatings3 += nUserValue**2
        itemCount += 1
        
        
