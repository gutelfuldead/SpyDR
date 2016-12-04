#!/usr/bin/python2.7
# Pipe Head
import numpy as np
from fifo_ops import read_pipe

pipename = "test.pipe"

dat = read_pipe(pipename)
