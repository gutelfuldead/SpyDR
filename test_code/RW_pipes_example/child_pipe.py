import os
import numpy as np

## TEST SET FOR NP.INT
# fifoname = './pipefifo'                      # must open same name
#
# N = 200
# a = np.zeros(N,dtype=np.int8)
#
# pipeout = os.open(fifoname, os.O_WRONLY)     # open fifo pipe file as fd
# os.write(pipeout,str(N))
#
# for i in range(0,N):
#     if (np.random.randint(0,100) >= 50):
#         a[i] = 1
#     os.write(pipeout, chr(a[i]))
# os.close(pipeout)

#TEST SET FOR NP.FLOAT

def write_np_flt_fifo(data, fifoname):
    """
    Input is dtype=np.float16,
    first writes the length of the array then
    writes %1.4f formatted float values as string of 6 bytes
    BLOCKING
    """
    try:
        os.mkfifo(fifoname)
    except:
        pass
    N = str(len(data))
    N = N.rjust(4, '0')
    pipe = os.open(fifoname, os.O_WRONLY)
    os.write(pipe, str(N)) # send length of the array
    for i in range(0,int(N)):
        os.write(pipe, str("%+1.4f" % data[i]))
    os.close(pipe)
    return

data = np.empty(200, dtype=np.float16)
for i in range(0,len(data)):
    data[i] = (-1)**i*i*2.0/102
print(data)
write_np_flt_fifo(data, "pipefifo")
