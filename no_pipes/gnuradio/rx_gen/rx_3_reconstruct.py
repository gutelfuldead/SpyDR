import numpy as np
import os
from fifo_ops import write_fifo

FILE_NAME_IN = "rx2.npy"
data = np.load(FILE_NAME_IN)
decode=[]
a = ''
for i in range(0,len(data)):
    a = a + str(data[i])
    if ((i+1)%8 == 0 and i !=0):
        decode.append(a)
        a = ''

message=''
for i in range(0,len(decode)):
    message = message + chr(int(decode[i],2))#message.append(chr(int(decode[i],2)))

write_fifo(message, "output_data.bin")
