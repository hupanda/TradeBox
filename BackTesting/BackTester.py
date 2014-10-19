import numpy as np


class BackTester:

    def __init__(self):
        pass

    @staticmethod
    def run_back_testing(data, strategy):

        result = 1
        pnl = data["Close"] * data[strategy]
        pnl = filter(lambda a: a != 0, pnl.tolist())
        if len(pnl) > 0:
            buy = [1/a for a in pnl if a > 0]
            sell = [-a for a in pnl if a < 0]
            result *= np.product(buy) * np.product(sell)
            if pnl[len(pnl)-1] > 0:
                result *= data["Close"][len(data["Close"])-1]
        return result