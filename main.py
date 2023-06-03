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
    # data = create_df(9, 1.15, 0.85, 8, 4)
    # We optimized each parameter separately to narrow down our final optimization domain
    # These are the values we want to optimize:
    best_buy_triggers = [1.13, 1.14, 1.12, 1.15]
    best_sell_triggers = [0.92, 0.85, 0.86, 0.83]
    best_moving_average_length = [8,9]
    best_ratioLB = [8, 9, 10]
    best_moving_average_ratio = [3,4,5]

    # Initializing to lists that will contain all sharpe ratios and all total_gains
    # We will sort these lists at the end
    best_sharpes = []
    best_gains = []
    for moving_average_length in best_moving_average_length:
        for buy_trigger in best_buy_triggers: # Buy Trigger
            for sell_trigger in best_sell_triggers: # Sell Trigger
                for ratioLB in best_ratioLB:
                    for moving_average_ratio in best_moving_average_ratio:
                        values = (moving_average_length, buy_trigger, sell_trigger, ratioLB, moving_average_ratio)
                        data = create_df(moving_average_length, buy_trigger, sell_trigger, ratioLB, moving_average_ratio)
                        b = Backtest(data, commission=1.5)
                        sharpe, return_value, gain = b.backtest()
                        # print(f"The Current Sharpe is: {sharpe}")
                        # print(f"The Current return is: {return_value}")
                        print(f"For values of {moving_average_length} - {buy_trigger} - {sell_trigger} - {ratioLB} - {moving_average_ratio}")
                        print(f"The Current gain is: {gain}")
                        print(f"The Current sharpe is: {sharpe}")
                        print("------------------------------------")
                        best_gains.append([values, gain])
                        best_sharpes.append([values, sharpe])
    # Now we have gathered all the necessary information
    # Sorting the lists:
    best_sharpes = sorted(best_sharpes, key=lambda x: x[1], reverse=True)
    best_gains = sorted(best_gains, key=lambda x: x[1], reverse=True)
    # Slicing the best 10 values for each list we will pick one of these values
    best_sharpes = best_sharpes[:10]
    best_gains = best_gains[:10]
    print(f"Best sharpes: {best_sharpes}")
    print(f"Best gains: {best_gains}")
    return 0

if __name__ == '__main__':
    main()

