import pandas as pd


class Backtest:
    def __init__(self,
                 data: pd.DataFrame,
                 commission: float,

    ):
        self.data = data
        self.commission = commission

    def __repr__(self):
        return "<Backtest " + str(self) + ">"


    def backtest(self):
        global prev_state
        data = self.data
        # print(data)
        # print(data.iloc[-1])
        total_gain = data.iloc[-1]['Capital']
        investing_value = data.iloc[0]['Capital']
        # investing_value = 50000
        total_return = total_gain / investing_value
        std = data['Close'].std()
        Rf = 5
        sharpe_ratio = (total_return - Rf) / std
        return sharpe_ratio, total_return, total_gain



