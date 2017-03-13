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
minUsers = 20

# Leemos el fichero u.data, y guardamos los resultados en una matriz
data = np.zeros((item_size, user_size), dtype=int)
with open('resources\\ml-100k\\u.data') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=' ')
    for row in csvreader:
        string = " ".join(row)
        split = string.split("\t")
        user = int(split[0])
        item = int(split[1])
        value = int(split[2])
        data[item][user] = value

# Precálculos necesarios
users_nRatings = (data != 0).sum(0)
users_sumRatings = data.sum(0)
recommendations = []
neighborhood = dict()

# ------------------
# --- Predicción ---
# ------------------

# Calculamos la media de valoración del usuario
pUser_nRatings = users_nRatings[pUser]
if pUser_nRatings == 0:
    print("User has no ratings. Impossible to make a prediction.")
    sys.exit(0)
else:
    pUserMean = users_sumRatings[pUser] / pUser_nRatings

for pItem in range(item_size):
    if data[pItem,pUser] == 0:
        continue
    # Calculo de vecindario
    neighborhoodItem = []
    for nItem in range(item_size):
        if nItem == pItem:
            continue
        
        # Operaciones de suma
        sumRatings1 = 0
        sumRatings2 = 0
        sumRatings3 = 0
        userCount = 0
        
        for user in range(user_size):
            # Calculamos la media de valoración del usuario 
            user_nRatings = users_nRatings[user]
            if user_nRatings == 0:
                continue
            userMean = users_sumRatings[user] / user_nRatings
            
            pUserValueP = data[pItem,user]
            pUserValueN = data[nItem,user]
            if pUserValueP == 0 or pUserValueN == 0:
                continue
            pUserValueP -= userMean
            pUserValueN -= userMean
            sumRatings1 += pUserValueP * pUserValueN
            sumRatings2 += pUserValueP**2
            sumRatings3 += pUserValueN**2
            userCount += 1
        
        if userCount == 0 or sumRatings1 == 0:
            neighborhoodItem.append((nItem, 0.0))
        elif userCount < minUsers:
            neighborhoodItem.append((nItem, (sumRatings1 / (math.sqrt(sumRatings2) * math.sqrt(sumRatings3)) ) * (userCount/minUsers)))
        else:
            neighborhoodItem.append((nItem, sumRatings1 / (math.sqrt(sumRatings2) * math.sqrt(sumRatings3))))
            
    # Ordenamos vecindario por orden de silimitud
    neighborhoodItem.sort(key=operator.itemgetter(1), reverse=True)
    neighborhood[pItem] = neighborhoodItem

for pItem in range(item_size):
    # Calculo de predicción
    if pItem not in neighborhood.keys():
        continue
    else:
        
        neighbourCount = 0
        sumRating = 0
        sumSimilitude = 0
        
        for neighbour in range(neighborhoodSize):
            nItem = neighborhood[pItem][neighbour][0]
            nSimilitude = neighborhood[pItem][neighbour][1]
            nRating = data[nItem,pUser]
            if nSimilitude <= 0 or nRating == 0:
                continue
            sumRating += nSimilitude * nRating
            sumSimilitude += nSimilitude
            neighbourCount += 1
        
        if neighbourCount == 0:
            #print("ERROR: No suitable neighbours could be found. Impossible to make a prediction.")
            continue
        else:
            prediction = sumRating/sumSimilitude
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