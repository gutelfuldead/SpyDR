import numpy as np
import os
from fifo_ops import read_pipe

FILE_NAME_IN = "rx2.fifo"
path = os.getcwd()
path = path + '/output_data.bin'

data = read_pipe(FILE_NAME_IN)

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

data_file = open(path, "wb")
data_file.write(message)
data_file.close()

# print "Output Data: {}".format(message)
