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
    max_sharpe = 0
    optimized_values = (0,0,0,0,0)
    for i in range(3, 15, 1): # Moving Average Length
        for j in np.arange(1.01, 3.0, 0.01): # Buy Trigger
            for k in np.arange(0.05, 0.99, 0.01): # Sell Trigger
                for l in range(2, 16, 1): # RatioLB
                    for m in range(2, 8, 1): # Moving Average Ratio
                        data = create_df(i, j, k, l, m)
                        b = Backtest(data, commission=1.5)
                        sharpe, gain = b.backtest()
                        if gain > max_gain:
                            max_gain = gain
                            max_sharpe = sharpe
                            optimized_values = (i,j,k,l,m)
    print (optimized_values)
    return 0

if __name__ == '__main__':
    main()

