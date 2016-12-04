import numpy as np

def int_to_bool(data):
    '''
    Takes integer value converts it to a single zero padded byte
    '''
    a = np.zeros(8,dtype=np.int8)
    bin_data = np.zeros(len(data)*8,dtype=np.int8)
    for i in range(0,len(data)):
		# formats data in 8bit binary without the 0b prefix
	    a = format(ord(chr(data[i])),'b').zfill(8)
	    for j in range(0,len(a)):
	        bin_data[i*len(a) + j] = a[j]
    return bin_data

def pack_bits(data):
    '''
    Add extra element indexing how many surplus bits will be packed
    '''
    nbits = len(data)
    rem = nbits % 8
    nbytes = nbits/8
    if rem: nbytes += 1
    packed = np.empty(1+nbytes, dtype=np.uint8)
    packed[0] = rem
    packed[1:] = np.packbits(data)
    # extra = 8 - len(data) % 8
    # packed = np.packbits(data)
    # packed = np.insert(packed,0,extra)
    return packed


def unpack_bits(data_packed):
    '''
    data_packed == packed data w/ extra bits
    Strips the excess bits when unpacking
    '''
    rem = data_packed[0]
    data_packed = data_packed.astype(dtype=np.uint8)
    unpacked = np.unpackbits(data_packed[1:])
    if rem:
        unpacked = unpacked[:-(8-rem)]
    # extra = data_packed[0]
    # data_packed = data_packed.astype(dtype=np.uint8)
    # data_packed = np.delete(data_packed, 0)
    # unpacked = np.unpackbits(data_packed)
    # index = np.empty(extra,dtype=np.int8)
    # for i in range(0,extra):
    #     index[i] = len(unpacked) - i - 1
    # unpacked = np.delete(unpacked, index)
    return unpacked


# import numpy as np
#
# def int_to_bool(data):
#     '''
#     Takes integer value converts it to a single zero padded byte
#     '''
#     a = np.zeros(8,dtype=np.int8)
#     bin_data = np.zeros(len(data)*8,dtype=np.int8)
#     for i in range(0,len(data)):
# 		# formats data in 8bit binary without the 0b prefix
# 	    a = format(ord(chr(data[i])),'b').zfill(8)
# 	    for j in range(0,len(a)):
# 	        bin_data[i*len(a) + j] = a[j]
#     return bin_data
#
# def pack_bits(data):
#     '''
#     Add extra element indexing how many surplus bits will be packed
#     '''
#     extra = 8 - len(data) % 8
#     packed = np.packbits(data)
#     packed = np.insert(packed,0,extra)
#     return packed
#
#
# def unpack_bits(data_packed):
#     '''
#     data_packed == packed data w/ extra bits
#     length_orig == original data length BEFORE packing
#     Strips the excess bits when unpacking
#     '''
#     extra = data_packed[0]
#     print data_packed
#     data_packed = np.delete(data_packed, 0)
#     print data_packed
#     unpacked = np.unpackbits(data_packed)
#     index = np.empty(extra,dtype=np.int8)
#     for i in range(0,extra):
#         index[i] = len(unpacked) - i - 1
#     unpacked = np.delete(unpacked, index)
#     return unpacked
