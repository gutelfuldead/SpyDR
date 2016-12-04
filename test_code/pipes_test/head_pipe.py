#!/usr/bin/python2.7
# Pipe Head
import numpy as np
from fifo_ops import write_pipe

N=41000
pipename = "test.pipe"
a=np.random.random(N)
# a = range(0,N)
write_pipe(a,pipename)
del a
