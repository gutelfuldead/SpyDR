library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity tb_d_ff is
end tb_d_ff;

architecture BHV of tb_d_ff is

  constant TEST_WIDTH : positive := 16;
  constant clk_time : time := 12.5 ns;

  signal s_clk   : std_logic;
  signal s_ff_set    : std_logic;
  signal s_D   : std_logic;
  signal s_Q : std_logic;


  component d_ff is
    port (
        clk : in std_logic;
        ff_set : in std_logic;
        D : in std_logic;
        Q : out std_logic);
  end component d_ff;

  begin

    UUT : d_ff
    port map(
      clk => s_clk,
      ff_set => s_ff_set,
      D => s_D,
      Q => s_Q);

    clock_gen : process
      begin
        s_clk <= '0' after clk_time, '1' after 2*clk_time;
      wait for 2*clk_time;
    end process clock_gen;

    tb: process
      begin

        wait for 2*clk_time;
        s_ff_set <= '1';
        s_D <= '0';
        wait for 4*clk_time;
        s_ff_set <= '0';
        s_D <= '1';
        wait for 8*clk_time;
        s_D <= '0';

    end process tb;
  end BHV;
