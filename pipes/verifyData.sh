#!/bin/bash

# Comparing input and output files
echo "Comparing md5sum of input and output bins..."
INPUTmd5=$(md5sum input_data.bin)
INPUT=${INPUTmd5:0:32}
OUTPUTmd5=$(md5sum output_data.bin)
OUTPUT=${OUTPUTmd5:0:32}
echo "Input: " $INPUT
echo "Output: "$OUTPUT

if [ "$INPUT" = "$OUTPUT" ]; then
  echo "Output matches input"
else
  echo "Output does NOT match input"
fi
