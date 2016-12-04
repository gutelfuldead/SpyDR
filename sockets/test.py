import numpy as np
import os
import time
from socket_funcs import socket_serv, open_socket_serv
from bool_func import int_to_bool


INPUT_NAME = 'raven_input.txt'
path = os.getcwd()
path = path + '/' + INPUT_NAME

fifo = open(path, "r")
data = ''
for i in fifo:
    data += i
fifo.close()

send_size = 512 # bytes
A = len(data)/send_size
pad = send_size - len(data)%send_size

int_data = np.empty(len(data)+pad,dtype=np.int8)
for i in range(0,len(int_data)):
  if i < len(data):
    int_data[i] = ord(data[i])
  else:
    int_data[i] = ord('.')

int_data = int_to_bool(int_data)

decode=[]
a = ''
for i in range(0,len(int_data)):
    a += str(int_data[i])
    if ((i+1)%8 == 0 and i !=0):
        decode.append(a)
        a = ''

message=''
for i in range(0,len(decode)):
    message += chr(int(decode[i],2))

print message
