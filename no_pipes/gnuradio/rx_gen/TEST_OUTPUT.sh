#!/bin/bash
# SpyDR (SOFTWARE python DEFINED RADIO)
# Run the full TX/RX chain


# RX Chain
echo "Decoding..."
echo "demod"
python rx_1_qpsk_demod.py
echo "decode"
python rx_2_decode.py
echo "reconstruct"
python rx_3_reconstruct.py

echo "Output:"
echo ""
cat output_data.bin
rm rx1.npy rx2.npy
