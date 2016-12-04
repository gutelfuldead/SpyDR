#!/usr/bin/python2.7

# test count and outcount algorithm
import numpy as np

width = 16
count = 0
out_count = 0

for i in range (0, width):
    # print ("count = {}, out_count = {},{}").format(count,out_count, out_count+1 )
    count = i
    out_count = 2*i+2

# check output of VHDL
input_stream = [0,1,0,1,1,1,0,0,1,0,1,0,0,0,1,0]
input_stream = np.asarray(input_stream)
N = len(input_stream)
output_stream = np.zeros(len(input_stream)*2+2, dtype=np.int)   # len_2x
selA = np.zeros(len(input_stream), dtype=np.int)
selB = np.zeros(len(input_stream), dtype=np.int)
print("python takes left most element as index 0 ie A=[0,1] -> A[0]=0")
print("VHDL takes right most element as index [0] ie A=std_logic_vector='01' -> A(0)=1")
# r=1/2 k=3 Convolutional Encoder
ff0 = ff1 = 0
for i in range(0,len(input_stream)):
    selA[i] = input_stream[i] ^ ff0 ^ ff1
    selB[i] = input_stream[i] ^ ff1
    ff1 = ff0
    ff0 = input_stream[i]
output_stream = np.hstack( zip(selA,selB) )

expected_out = [0,0,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,0,0,0,1,0,1,1,0,0,1,1]
expected_out = np.asarray(expected_out)
# print("expected out  = {}").format(expected_out)
print("input stream  = {}").format(input_stream)
print ("=============CORRECT=============")

print("output stream = {}").format(output_stream)
# print("len input {},  output = {}").format(len(input_stream),len(output_stream))
# print("len(output)-len(input)*2 {}").format(len(output_stream) - len(input_stream)*2)



print ("=============NEW=============")
# r=1/2 k=3 Convolutional Encoder
ff0 = ff1 = 0
for i in range(0,len(input_stream)):
    output_stream[(i*2)] = input_stream[i] ^ ff0 ^ ff1
    output_stream[(i*2+1)]   = input_stream[i] ^ ff1
    ff1 = ff0
    ff0 = input_stream[i]
print("output stream = {}").format(output_stream)
