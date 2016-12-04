library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity fsm is
  generic ( d_width : positive := 16);
  port (
    clk : in std_logic;
    rst : in std_logic;
    en  : in std_logic;
    done : out  std_logic;
    ff_set  : out std_logic);
end fsm;

architecture FLOW of fsm is

  type STATE_TYPE is (S_INIT, S_WORKING, S_DONE);
  signal state, next_state : STATE_TYPE;

begin


  determine_state: process(clk,rst)
  begin
    if(rst = '1') then
      state <= S_INIT;
    elsif (rising_edge(clk)) then
      state <= next_state;
    end if;
  end process determine_state;

  states : process(en, state, clk)
  begin
    ff_set <= '0';
    done <= '0';
    next_state <= state;

    case state is
      when S_INIT =>
        -- set all D-FFs to zero output
        ff_set  <= '1';
        if en = '1' then
          next_state <= S_WORKING;
        end if;
      when S_WORKING =>
        ff_set  <= '0';
        -- if s_count >= d_width then
        --   next_state <= S_DONE;
        -- end if;
      when S_DONE =>
        done <= '1';
        next_state <= S_INIT;
    end case;

  end process states;
end FLOW;
