import numpy as np


class BackTester:

    def __init__(self):
        pass

    @staticmethod
    def run(data, strategy_list):
        strategy_list.append("Benchmark")
        data["Benchmark"] = [1] + np.repeat(0, len(data.index)-1).tolist()
        for strategy in strategy_list:
            result = []
            pos = 0
            pnl = 1
            for index in data.index.tolist():
                if pos == 1:
                    pnl *= (data['Close'][index] / data['Close'][index-1])
                result.append(pnl)
                #update pos
                if data[strategy][index] != 0:
                    pos += (-1)**pos
            data[strategy + "_pnl"] = result
        return data

    # @staticmethod
    # def run(data, strategy_list):
    #     strategy_list.append("Benchmark")
    #     for strategy in strategy_list:
    #         result = []
    #         for index, row in data.iterrows():
    #             result.append(BackTester.run_back_testing(data[:index+1], strategy))
    #         data[strategy + "_pnl"] = result
    #     return data
    #
    # @staticmethod
    # def run_back_testing(data, strategy):
    #     result = 1
    #     if strategy == "Benchmark":
    #         data[strategy] = [1] + np.repeat(0, len(data.index)-1).tolist()
    #
    #     pnl = data["Close"] * data[strategy]
    #     pnl = filter(lambda item: item != 0, pnl.tolist())
    #     if len(pnl) > 0:
    #         buy = [1/a for a in pnl if a > 0]
    #         sell = [-a for a in pnl if a < 0]
    #         result *= np.product(buy) * np.product(sell)
    #         if pnl[len(pnl)-1] > 0:
    #             result *= data["Close"][len(data["Close"])-1]
    #     return result
