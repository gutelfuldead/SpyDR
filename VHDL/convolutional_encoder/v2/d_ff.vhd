library ieee;
  use ieee.std_logic_1164.all;

entity d_ff is
    port (
        clk : in std_logic;
        rst : in std_logic;
        D : in std_logic;
        Q : out std_logic);
end;

architecture behavioral of d_ff is
  signal s_Q : std_logic;
begin
    process(clk, rst)
    begin
      -- if (rst = '1' and rising_edge(clk)) then
      if (rst = '1') then
        s_Q <= '0';
      elsif (rising_edge(clk)) then
        s_Q <= D;
      end if;
    end process;
  Q <= s_Q;
end behavioral;
