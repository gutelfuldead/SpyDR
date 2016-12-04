#!/usr/bin/python2.7

import numpy as np
import os

x = np.zeros(10,dtype=np.int8)
for i in range(0,len(x)):
    if i%2 != 1:
        x[i] = 1
x = np.insert(x,0,2)
print (x)
x = np.delete(x,0)
print (x)
data_size = 2
data = np.random.randint(0,9,data_size)
tx=''
for i in range(0,data_size):
    tx += chr(data[i])
data = tx
a = np.zeros(8,dtype=np.int8)
bin_data = np.zeros(len(data)*8+2,dtype=np.int8)

for i in range(0,len(data)):
    # formats data in 8bit binary without the 0b prefix
    a = format(ord(data[i]),'b').zfill(8)
    for j in range(0,len(a)):
        bin_data[i*len(a) + j] = a[j]
        # print("a[j] = {}, bool(a[j]) = {}").format(a[j], bool(int(a[j])))
bin_data[len(bin_data)-1] = 1
bin_data[len(bin_data)-2] = 1

print ("original data:  {}").format(bin_data)
b_dat = np.packbits(bin_data)
b_dat_unpacked = np.unpackbits(b_dat)
print ("unpacked data:  {}").format(b_dat_unpacked)
extra = 8 - (len(bin_data) % 8)
print ("excess bits: {}").format(extra)
index = np.empty(extra)
for i in range(0,extra):
    index[i] = len(bin_data)+i
b_dat_unpacked = np.delete(b_dat_unpacked,index)
print("corrected data: {}").format(b_dat_unpacked)



path = os.getcwd()
path = path + '/bool_data.bin'
data_file = open(path, "wb")
data_file.write(b_dat)
data_file.close()
