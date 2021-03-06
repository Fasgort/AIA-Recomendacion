# -*- coding: utf-8 -*-

import csv
import numpy as np
import math
import operator
import sys

# Número de usuarios y películas en el conjunto de datos
user_size = 943 + 1 # Pos 0 vacía, pero es más cómodo
item_size = 1682 + 1 # Pos 0 vacía

# Provisional - Usuario y film a predecir
pUser = 23

# Settings
neighborhoodSize = 30
minItems = 20

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
pUser_nRatings = (data[pUser] != 0).sum()
if pUser_nRatings == 0:
    print("User has no ratings. Impossible to make a prediction.")
    sys.exit(0)
else:
    pUserMean = data[pUser].sum() / pUser_nRatings

# Calculo de vecindario
neighborhood = []
for nUser in range(user_size):
    if nUser == pUser:
        continue
    
    # Calculamos la media de valoración del usuario vecino
    nUser_nRatings = (data[nUser] != 0).sum()
    if nUser_nRatings == 0:
        continue
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
    
    if itemCount == 0 or sumRatings1 == 0:
        neighborhood.append((nUser, 0.0))
    elif itemCount < minItems:
        neighborhood.append((nUser, (sumRatings1 / (math.sqrt(sumRatings2) * math.sqrt(sumRatings3)) ) * (itemCount/minItems)))
    else:
        neighborhood.append((nUser, sumRatings1 / (math.sqrt(sumRatings2) * math.sqrt(sumRatings3))))
        
# Ordenamos vecindario por orden de silimitud
neighborhood.sort(key=operator.itemgetter(1), reverse=True)

# Calculo de predicción
recommendations = []
for pItem in range(item_size):
    if data[pUser][pItem] != 0:
        #print("ERROR: Rating already exists. Cannot be predicted.")
        #print("Rating for user " + str(pUser) + " and item " + str(pItem) + " is " + str(data[pUser][pItem]) + ".")
        continue
    else:
        
        neighbourCount = 0
        sumRating = 0
        sumSimilitude = 0
        
        for neighbour in range(neighborhoodSize):
            nUser = neighborhood[neighbour][0]
            nSimilitude = neighborhood[neighbour][1]
            nRating = data[nUser][pItem]
            if nSimilitude <= 0 or nRating == 0:
                continue
            nUser_nRatings = (data[nUser] != 0).sum()
            nUserMean = data[nUser].sum() / nUser_nRatings
            sumRating += nSimilitude * (nRating - nUserMean)
            sumSimilitude += nSimilitude
            neighbourCount += 1
        
        if neighbourCount == 0:
            #print("ERROR: No suitable neighbours could be found. Impossible to make a prediction.")
            continue
        else:
            prediction = nUserMean + sumRating/sumSimilitude
            if prediction > 5.0:
                prediction = 5.0
            elif prediction < 1.0:
                prediction = 1.0
            #print("Prediction for user " + str(pUser) + " and item " + str(pItem) + " is " + str(prediction) + ".")
            recommendations.append((pItem, prediction))

# Ordenamos recomendaciones por orden de silimitud
recommendations.sort(key=operator.itemgetter(1), reverse=True)

# Devolvemos los diez primeros resultados
print("User " + str(pUser) + " recommendations:\n")
for rec in range(50):
    print("Item " + str(recommendations[rec][0]) + " is expected to have a " + str(recommendations[rec][1]) + " rating.")