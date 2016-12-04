import numpy as np
import math
N = 75
input_stream = np.random.random_integers(0,100,size=N)

#############
# Interleaver
#############
mat_dim = int(math.sqrt(len(input_stream)))
interleave_mat = np.zeros((mat_dim,mat_dim), dtype=np.int)
interleave_out = np.zeros(mat_dim**2, dtype=np.int)

for i in range(0,mat_dim):
    for j in range(0,mat_dim):
        interleave_mat[i][j] = input_stream[i*mat_dim + j]
for i in range(0,mat_dim):
    for j in range(0,mat_dim):
        interleave_out[i*mat_dim + j] = interleave_mat[j][i]

################
# De-Interleaver
################
deinterleave_mat = np.zeros((mat_dim,mat_dim), dtype=np.int)
deinterleave_out = np.zeros(mat_dim**2, dtype=np.int)
for i in range(0,mat_dim):
    for j in range(0,mat_dim):
        deinterleave_mat[i][j] = interleave_out[i*mat_dim + j]
for i in range(0,mat_dim):
    for j in range(0,mat_dim):
        deinterleave_out[i*mat_dim + j] = deinterleave_mat[j][i]
output_stream = deinterleave_out

error_count = sum(1 for a,b in zip(input_stream, output_stream) if a != b)
if len(input_stream) > len(output_stream):
    error_count += len(input_stream) - len(output_stream)
print("Number of errors: {}").format(error_count)
print("input stream: {}").format(input_stream)
print("output stream: {}").format(output_stream)
