library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity tb_conv_encoder is
end tb_conv_encoder;

architecture BHV of tb_conv_encoder is

  constant TEST_WIDTH : positive := 16;
  constant clk_time : time := 12.5 ns;

  signal s_clk   : std_logic;
  signal s_en    : std_logic;
  signal s_rst   : std_logic;
  signal s_dout_valid : std_logic;
  signal s_din : std_logic_vector(TEST_WIDTH-1 downto 0);
  signal hw_data_out : std_logic_vector(TEST_WIDTH*2-1 downto 0);
  signal expected : std_logic_vector(TEST_WIDTH*2-1 downto 0);
  signal sw_data_out : std_logic_vector(TEST_WIDTH*2-1 downto 0);
  signal s_ff0, s_ff1 : std_logic;

  component conv_encoder_top is
    generic (d_width : positive := 16);
    port (
        din        : in std_logic_vector(d_width-1 downto 0);
        clk        : in std_logic := '0';
        en         : in std_logic := '0';
        rst        : in std_logic := '1';
        dout_valid : out std_logic;
        dout       : out std_logic_vector(d_width*2-1 downto 0));
  end component conv_encoder_top;

  begin
    expected <= "00111000011001111110001011001110";

    UUT : conv_encoder_top
      generic map ( d_width => TEST_WIDTH )
      port map (
        din => s_din,
        clk => s_clk,
        en  => s_en,
        rst => s_rst,
        dout_valid => s_dout_valid,
        dout => hw_data_out);

    clock_gen : process
      begin
        s_clk <= '0' after clk_time, '1' after 2*clk_time;
      wait for 2*clk_time;
    end process clock_gen;

    tb: process
      -- variable dout_temp : std_logic_vector(TEST_WIDTH*2-1 downto 0);
      variable ff0,ff1 : std_logic := '0';
      begin

        s_rst <= '1';
        s_en  <= '0';
        s_din <= (others => '0');
        wait for 100 ns;

        s_rst <= '0';
        s_din <= "0101110010100010";
        wait for 100 ns;
        s_en  <= '1';
        while s_dout_valid = '0' loop
          wait for clk_time * 2;
        end loop;

        s_ff0 <= '0';
        s_ff1 <= '0';
        for i in 0 to TEST_WIDTH-1 loop
          -- sw_data_out(TEST_WIDTH*2-1-(i*2+1))   <= s_din(i) xor ff0 xor ff1;
          -- sw_data_out(TEST_WIDTH*2-1-(i*2))     <= s_din(i) xor ff1;
          sw_data_out(i*2+1)   <= s_din(i) xor s_ff0 xor s_ff1;
          sw_data_out(i*2)     <= s_din(i) xor s_ff1;
          s_ff1 <= s_ff0;
          s_ff0 <= s_din(i);
        end loop;

        wait for 100 ns;

        assert(s_dout_valid = '1') report "d_out never reports finished";
        assert(to_integer(unsigned(hw_data_out)) = to_integer(unsigned(sw_data_out))) report "output is incorrect...";

    end process tb;
  end BHV;
