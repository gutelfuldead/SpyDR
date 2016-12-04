# diff.py - Do two files match?
# Exercise: Rewrite this code to compare the files part at a time so it
# will not run out of RAM with large files.
import sys

with open(sys.argv[1], 'rb') as file1, open(sys.argv[2], 'rb') as file2:
    data1 = file1.read()
    data2 = file2.read()

if data1 != data2:
    print("Files do not match.")
else:
    print("Files match.")
