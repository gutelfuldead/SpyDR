#!/bin/bash
# Run the full TX/RX chain
# Press ctrl+c to stop all python scripts and clean up variables
# press ctrl+z to end program

# trap ctrl-c and call ctrl_c()
trap ctrl_c SIGINT
function ctrl_c()
    {
        echo ""
        echo ""
        echo "Killing all running Python scripts..."
        for pid in `ps -ef | grep python | grep -v grep | awk '{print $2}'` ; do kill $pid ; done

        sleep 1s

        # Comparing input and output files
        echo ""
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

	      echo ""
	      echo "OUTPUT"
	      cat output_data.bin
	      echo ""
        echo ""
        echo "--cleaning up--"
        echo "Removing *bin *uds *npy"
        rm *.bin *.uds *.npy

    }

echo "running tx_1_create_data"
./tx_1_create_data.py > /dev/null

echo "running tx_2_read_data"
./tx_2_read_data.py & > /dev/null

echo "running tx_3_FEC"
./tx_3_FEC.py & > /dev/null

echo "running tx_4_qpsk_mod"
./tx_4_qpsk_mod.py & > /dev/null

echo "running awgn_burst_errors_CHANNEL"
./awgn_burst_errors_CHANNEL.py & > /dev/null

echo "running rx_1_qpsk_demod"
./rx_1_qpsk_demod.py & > /dev/null

echo "running rx_2_decode"
./rx_2_decode.py & > /dev/null

echo "running rx_3_reconstruct"
./rx_3_reconstruct.py &

while true; do read x; done;
