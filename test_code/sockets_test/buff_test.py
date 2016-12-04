#!/usr/bin/python2.7
# test buffer
import numpy as np
from buffer_rw import *

N = 200
buff_name = "buffTest.txt"
a = np.random.random(N)
write_buffer(buff_name,a)
b = read_buffer(buff_name)

print (a==b)
