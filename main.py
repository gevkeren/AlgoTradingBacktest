import pandas as pd
import numpy as np
from backtest import Backtest
# from strategies import RandomStrategy
# from summary import Summary, plot_data
from VIX_strategy import create_df
from utils import adjust_types
# ITVS - ממנו גוזרים כניסות ויציאות לטרייד
# ITVS - (VIX / VIX3M).mean().rolling(length_moving_average)


def max_draw_down_calc(df):
    maxDD = 0
    iVal = 0
    jVal = 0
    DD = 0

    for i in range(0, len(df['Capital'])):
        bechmark = df['Capital'][i]
        for j in range(i + 1, len(df['Capital'])):
            if (df['Capital'][j] > bechmark):
                break
            DD = (df['Capital'][j] / df['Capital'][i]) - 1
            DD = df['Capital'][j] - df['Capital'][i]
            if (DD < maxDD):
                maxDD = DD
                iVal = i
                jVal = j
    return maxDD

def main():
    # data = create_df(9, 1.15, 0.85, 8, 4)
    # We optimized each parameter separately to narrow down our final optimization domain
    # These are the values we want to optimize:
    best_moving_average_length = [8,9]
    best_buy_triggers = [1.13, 1.14, 1.12, 1.15]
    best_sell_triggers = [0.92, 0.85, 0.86, 0.83]
    best_ratioLB = [8, 9, 10]
    best_moving_average_ratio = [3,4,5]

    # Initializing to lists that will contain all sharpe ratios and all total_gains
    # We will sort these lists at the end
    best_sharpes = []
    best_gains = []
    best_values = []
    for moving_average_length in best_moving_average_length:
        for buy_trigger in best_buy_triggers: # Buy Trigger
            for sell_trigger in best_sell_triggers: # Sell Trigger
                for ratioLB in best_ratioLB:
                    for moving_average_ratio in best_moving_average_ratio:
                        values = (moving_average_length, buy_trigger, sell_trigger, ratioLB, moving_average_ratio)
                        data = create_df(moving_average_length, buy_trigger, sell_trigger, ratioLB, moving_average_ratio)
                        # Draw Down calculation
                        draw_down = max_draw_down_calc(data)
                        b = Backtest(data, commission=1.5)
                        sharpe, return_value, gain = b.backtest()
                        # print(f"The Current Sharpe is: {sharpe}")
                        # print(f"The Current return is: {return_value}")
                        print(f"For values of {moving_average_length} - {buy_trigger} - {sell_trigger} - {ratioLB} - {moving_average_ratio}")
                        print(f"The Current gain is: {gain}")
                        print(f"The Current sharpe is: {sharpe}")
                        print("------------------------------------")
                        best_gains.append([values, round(gain, 2), draw_down])
                        best_sharpes.append([values, round(sharpe, 7), draw_down])
    # Now we have gathered all the necessary information
    # Sorting the lists:
    best_sharpes = sorted(best_sharpes, key=lambda x: x[1], reverse=True)
    best_gains = sorted(best_gains, key=lambda x: x[1], reverse=True)
    # Slicing the best 10 values for each list we will pick one of these values
    best_sharpes = best_sharpes[:10]
    best_gains = best_gains[:10]
    for gain in best_gains:
        best_values.append(gain[0])
    print(f"Best Gains  : {best_gains}")
    print(f"Best Sharpes: {best_sharpes}")
    print("Best Values:")
    for value in best_values:
        print(value)
    return 0
# Best Values:
# (8, 1.13, 0.92, 9, 4) - 397621
# (8, 1.13, 0.85, 9, 4) - 396701
# (8, 1.13, 0.86, 9, 4) - 396026
# (8, 1.13, 0.83, 9, 4) - 394476
# (8, 1.12, 0.92, 9, 4) - 389983
# (8, 1.12, 0.85, 9, 4) - 389063
# (8, 1.12, 0.86, 9, 4) - 388388
# (8, 1.14, 0.92, 9, 4) - 386996
# (8, 1.12, 0.83, 9, 4) - 386838
# (8, 1.14, 0.85, 9, 4) - 386076
if __name__ == '__main__':
    main()

