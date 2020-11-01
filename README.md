# Trading_reinforcement_learning_simulator
Objects used to keep track of stocks and shorts held as well as capital remaining

Trading_bots.py
------------------------------------------------------------------------------------
Class used to initialise trading objects.
The trading objects keep track of current capital and stocks held.

Previous tests showed overall better performance if closing a position was controlled by crossing predefined thresholds
rather than using ML or an RL agent to choose the best position to close.
Therefore,  help_sell and help_close_short methods close long and short positions if they cross a threshold to realise 
gains or to avoid further losses in the case that the prediction was incorrect.

Trader_1p_threshold, Trader_1p5_threshold and  Trader_2p_threshold create differing levels to realise gains and 
avoid losses which is then used in testing to find the most profitable configuration.

