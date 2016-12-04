library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity tb_conv_encoder is
end tb_conv_encoder;

architecture BHV of tb_conv_encoder is

  constant TEST_WIDTH : positive := 16;
  constant clk_time : time := 12.5 ns;

  signal sig_clk    : std_logic;
  signal sig_din    : std_logic_vector(TEST_WIDTH-1 downto 0);
  signal sig_rst    : std_logic;
  signal sig_en     : std_logic;
  signal sig_done   : std_logic;
  signal hw_dout    : std_logic_vector(TEST_WIDTH*2 - 1 downto 0);
  signal sw_expected: std_logic_vector(TEST_WIDTH*2 -1 downto 0);

  component conv_encoder is
    generic (d_width : positive := 16);
    port (
        clk    : in std_logic;
        din    : in std_logic_vector(d_width-1 downto 0);
        rst    : in std_logic;
        en     : in std_logic;
        done   : out std_logic;
        dout   : out std_logic_vector(d_width*2 - 1 downto 0));
  end component conv_encoder;

  begin
    sw_expected <= "00111000011001111110001011001110";

    UUT : conv_encoder
      generic map ( d_width => TEST_WIDTH )
      port map (
        clk => sig_clk,
        din => sig_din,
        rst => sig_rst,
        en  => sig_en,
        done => sig_done,
        dout => hw_dout);

    clock_gen : process
      begin
        sig_clk <= '0' after clk_time, '1' after 2*clk_time;
      wait for 2*clk_time;
    end process clock_gen;

    tb: process
      variable a,b : std_logic := '0';
      variable sw_out : std_logic_vector(TEST_WIDTH*2-1 downto 0);
      begin

        sw_out := (others => '0');
        sig_rst <= '1';
        sig_en  <= '0';
        sig_din <= (others => '0');
        wait for 100 ns;

        sig_rst <= '0';
        sig_din <= "0101110010100010"; -- ORIGINAL SEQUENCE
        -- sig_din <= "0100010100111010";    -- WORKING: Reverse order input...
        wait for 100 ns;
        sig_en  <= '1';
        while sig_done = '0' loop
          wait for clk_time * 2;
        end loop;
        wait for 100 ns;

        assert(to_integer(unsigned(hw_dout)) /= to_integer(unsigned(sw_expected))) report "OUTPUT CORRECT";
        assert(to_integer(unsigned(hw_dout)) = to_integer(unsigned(sw_expected))) report "OUTPUT DOES NOT MATCH";

    end process tb;
  end BHV;
