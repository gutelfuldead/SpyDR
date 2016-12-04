# Indexing problems...
import numpy as np

N = 70
Mp = 9
A = N/Mp
LO = N % Mp
data = range(0,N)

print("{} = {}").format(N,(A*Mp + LO))
print("A={},Mp={},LO={}").format(A,Mp,LO)
for i in range(0,A):
    print(data[i*Mp:i*Mp+Mp])
print(data[-LO:])
