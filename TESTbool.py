from bool_func import *
x=np.array(10)
for i in range(0,len(x)):
  x[i] = x%2
pack = pack_bits(x)
unpack = unpack_bits(pack)
print pack
print unpack
