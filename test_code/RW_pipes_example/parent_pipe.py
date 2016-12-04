import os
import numpy as np

## TEST SET FOR NP.INT
# fifoname = './pipefifo'
#
# pipein = os.open(fifoname, os.O_RDONLY)                 # open fifo as stdio object
# N = int(os.read(pipein,3))
# read = np.zeros(N,dtype=np.int8)
#
# for i in range(0,N):
#     read[i] = ord(os.read(pipein,1))           # blocks until data sent
# print read
# os.close(pipein)
# print ("length = {}, type = {}").format(len(read),type(read))

## TEST SET FOR NP.FLOAT

def read_np_flt_fifo(fifoname):
    """

    """
    try:
        os.mkfifo(fifoname)
    except:
        pass
    pipe = os.open(fifoname, os.O_RDONLY)
    N = int(os.read(pipe,4)) # recover N
    read = np.empty(N,dtype=np.float16)
    for i in range(0,N):
        read[i] = float(os.read(pipe,7))
    os.close(pipe)
    return read

test = read_np_flt_fifo("pipefifo")
print test
print(type(test[2]))
print(len(test))
