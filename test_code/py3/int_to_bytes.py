i = 16

# Create one byte from the integer 16
single_byte = i.to_bytes(1, byteorder='big', signed=True) 
print(single_byte)

# Create four bytes from the integer
four_bytes = i.to_bytes(4, byteorder='big', signed=True)
print(four_bytes)

# Compare the difference to little endian
print(i.to_bytes(4, byteorder='little', signed=True))

# Create bytes from a list of integers with values from 0-255
bytes_from_list = bytes([255, 254, 253, 252])
print(bytes_from_list)

# Create a byte from a base 2 integer
one_byte = int('11110000', 2)
print(one_byte)
