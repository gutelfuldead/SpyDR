#!/usr/bin/python2.7

###################################
# Create test data for transmission
###################################

import numpy as np
import random
import os

data_size = 512
data = np.random.randint(0,1000,data_size)
tx=''
for i in range(0,data_size):
    tx += str(data[i])

path = os.getcwd()
path = path + '/input_data.bin'
data_file = open(path, "wb")
data_file.write(tx)
data_file.close()

# print(len(tx))
# print("input data: {} ").format(tx)
