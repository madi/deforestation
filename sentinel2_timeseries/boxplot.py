import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from load_data import *

######### Change paths according to locations in your machine ##########
deltas_file = "/home/leomarg/deltas_test.csv"
file_location = '/home/leomarg/ndvi_big_areas1.csv'
########################################################################

deltas = read_deltas(deltas_file, file_location)
deltas1 = []
for i in (range(len(deltas))):
    deltas1.append(deltas.iloc[i])

fig, ax = plt.subplots()
pos = np.array(range(len(deltas1))) + 1
bp = ax.boxplot(deltas1, positions=pos, notch=1)
ax.set_xlabel('date')
ax.set_ylabel('delta')
plt.show()

# TODO: put actual dates on the x-axis






