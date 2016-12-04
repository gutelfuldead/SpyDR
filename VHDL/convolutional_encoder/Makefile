GHDL=ghdl
GHDLFLAGS=
MODULES=\
		conv_encoder.o \
		tb_conv_encoder \

test: $(MODULES)
				./tb_conv_encoder --vcd=wave_output.vcd
# Binary depends on the object file
%: %.o
				$(GHDL) -e $(GHDLFLAGS) $@

# Object file depends on source
%.o: %.vhd
				$(GHDL) -a $(GHDLFLAGS) $<

clean:
				echo "Cleaning up..."
				rm -f *.o *_testbench work*.cf e*.lst conv_encoder tb_conv_encoder wave_output.vcd
