library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity conv_encoder is
    generic (d_width : positive := 16);
    port (
        clk    : in std_logic;
        din    : in std_logic_vector(d_width-1 downto 0);
        rst    : in std_logic;
        en     : in std_logic;
        done   : out std_logic;
        dout   : out std_logic_vector(d_width*2 - 1 downto 0));
end conv_encoder;

architecture behavioral of conv_encoder is
  signal sig_shift_reg_0, sig_shift_reg_1 : std_logic := '0';
  begin
    conv_encoder : process (clk, rst)
      variable count : integer range -1 to din'length := din'length - 1;
    begin
      if (rst = '1') then
        count := din'length - 1; -- proceed through SLV in reverse order
        sig_shift_reg_0 <= '0';
        sig_shift_reg_1 <= '0';
        dout <= (others => '0');
        done <= '0';
      elsif (count < 0) then
        done <= '1';
      elsif (rising_edge(clk) and en = '1') then -- proceed through encoder
        sig_shift_reg_0 <= din(count);
        sig_shift_reg_1 <= sig_shift_reg_0;
        dout(count*2+1)   <= din(count) xor sig_shift_reg_0 xor sig_shift_reg_1; -- 111 binary
        dout(count*2)     <= din(count) xor sig_shift_reg_1;       -- 101 binary
        count := count - 1;
      end if;
    end process conv_encoder;
end behavioral;
