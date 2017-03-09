# -*- coding: utf-8 -*-

import csv
import numpy as np

# Número de usuarios y películas en el conjunto de datos
user_size = 943 + 1 # Pos 0 vacía, pero es más cómodo
item_size = 1682 + 1 # Pos 0 vacía

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

