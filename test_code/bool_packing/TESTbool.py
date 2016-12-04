from bool_func import *
x=np.zeros(8*9+5, dtype=np.int8)
for i in range(0,len(x)):
  x[i] = i%2
pack = pack_bits(x)
unpack = unpack_bits(pack)

print len(x)
print len(unpack)
print x
print unpack
if x.all == unpack.all:
    print"TRUE"
