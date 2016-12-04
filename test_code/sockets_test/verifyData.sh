#!/bin/bash

# Comparing input and output files
echo "Comparing md5sum of input and output bins..."
INPUTmd5=$(md5sum input.txt)
INPUT=${INPUTmd5:0:32}
OUTPUTmd5=$(md5sum output.txt)
OUTPUT=${OUTPUTmd5:0:32}
INSIZE=$(stat --printf="%s" input.txt)
OUTSIZE=$(stat --printf="%s" output.txt)
echo "Input: " $INPUT "size: " $INSIZE
echo "Output: "$OUTPUT "size: " $OUTSIZE

if [ "$INPUT" = "$OUTPUT" ]; then
  echo "Output matches input"
else
  echo "Output does NOT match input"
fi
