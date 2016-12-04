library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity conv_encoder_top is
  generic (d_width : positive := 16);
  port (
      din : in std_logic_vector(d_width-1 downto 0);
      clk : in std_logic;
      en  : in std_logic;
      rst : in std_logic;
      dout_valid : out std_logic;
      dout       : out std_logic_vector(d_width*2-1 downto 0));
  end;

architecture behavioral of conv_encoder_top is

  component conv_encoder is
    generic (d_width : positive := 16);
    port (
        clk : in std_logic;
        din : in std_logic;
        rst : in std_logic;
        dout : out std_logic_vector(1 downto 0));
    end component conv_encoder;

  signal s_rst : std_logic;
  signal s_dout : std_logic_vector(1 downto 0);
  signal s_din : std_logic := '0';
  signal TEMP : integer := 0;
  begin

    U_CONV_ENC : conv_encoder
      generic map (d_width => d_width)
      port map (clk => clk,
                din => s_din,
                rst => s_rst,
                dout => s_dout);

    s_rst <= rst;
    s_din <= din(TEMP);
    -- dout(TEMP*2)   <= s_dout(0);
    -- dout(TEMP*2+1) <= s_dout(1);

    logic: process(clk, rst, en)
      variable count : integer range 0 to d_width := 0;
    begin
      if (rst = '1') then
        dout <= (others => '0');
        count := 0;
        -- s_din <= '0';
        dout_valid <= '0';
      elsif (rising_edge(clk) and en = '1' and count < din'length-1) then
        -- s_din <= din(count);
        -- if count >= 2 then
        dout(count*2)     <= s_dout(0);
        dout(count*2 + 1) <= s_dout(1);
      -- end if;
        count := count + 1;
      elsif (count >= din'length - 1) then
        dout_valid <= '1';
        -- count := 0;
        -- s_din <= '0';
      end if;
      TEMP <= count;
    end process logic;
end behavioral;
