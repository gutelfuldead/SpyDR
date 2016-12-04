library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity conv_encoder is
    generic (d_width : positive := 16);
    port (
        clk    : in std_logic;
        din    : in std_logic;
        rst    : in std_logic;
        -- go     : in std_logic;
        dout   : out std_logic_vector(1 downto 0));
end conv_encoder;

architecture behavioral of conv_encoder is
  component d_ff is
    port (
        clk : in std_logic;
        rst : in std_logic;
        D   : in std_logic;
        Q   : out std_logic);
  end component d_ff;

  signal sig_ff0_out, sig_ff1_out : std_logic := '0';
  begin
    ff0 : d_ff
      port map (clk    => clk,
                rst    => rst,
                D      => din,
                Q      => sig_ff0_out);
    ff1 : d_ff
      port map (clk    => clk,
                rst    => rst,
                D      => sig_ff0_out,
                Q      => sig_ff1_out);

    dout(1) <= din xor sig_ff0_out xor sig_ff1_out;
    dout(0) <= din xor sig_ff1_out;

end behavioral;
