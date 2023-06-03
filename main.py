import pandas as pd
import numpy as np
from backtest import Backtest
# from strategies import RandomStrategy
# from summary import Summary, plot_data
from VIX_strategy import create_df
from utils import adjust_types
# ITVS - ממנו גוזרים כניסות ויציאות לטרייד
# ITVS - (VIX / VIX3M).mean().rolling(length_moving_average)

def main():
    max_gain = 0
    max_return = 0
    max_sharpe = 0
    optimized_values = (0,0,0,0,0)
    # data = create_df(9, 1.15, 0.85, 8, 4)
    # b = Backtest(data, commission=1.5)
    # sharpe, gain = b.backtest()
    for i in range(6, 12, 1): # Moving Average Length
        for j in np.arange(1.01, 2.0, 0.01): # Buy Trigger
            for k in np.arange(0.5, 0.99, 0.01): # Sell Trigger
                for l in range(4, 12, 1): # RatioLB
                    for m in range(2, 6, 1): # Moving Average Ratio
                        data = create_df(i, j, k, l, m)
                        b = Backtest(data, commission=1.5)
                        sharpe, return_value, gain = b.backtest()
                        print(f"The Current Sharpe is: {sharpe}")
                        print(f"The Current return is: {return_value}")
                        print(f"The Current gain is: {gain}")
                        print("------------------------------------")
                        print()
                        if gain > max_gain:
                            max_gain = gain
                            max_sharpe = sharpe
                            max_return = return_value
                            optimized_values = (i,j,k,l,m)
    print(f"The Optimized Sharpe ratio is: {max_sharpe}")
    print(f"The Optimized return is: {max_return}")
    print(f"The Optimized total gain is: {max_gain}")
    print (optimized_values)
    return 0

if __name__ == '__main__':
    main()

