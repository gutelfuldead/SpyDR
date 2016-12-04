import numpy as np

N=100
a=np.random.randint(0,100, N)

for i in range(0,N-1):
  print( a[i].to_bytes(8) ^ a[i+1].to_bytes(8))
