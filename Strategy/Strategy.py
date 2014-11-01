import abc
import pandas
import numpy as np
from Utility.BackTester import *


class StrategyFactory(object):

    @staticmethod
    def get_strategy(name):
        if name == "MA":
            return StrategyMovingAverage(name)
        elif name == "MAB":
            return StrategyMovingAverageBase(name)
        elif name == "BB":
            return StrategyBollingerBand(name)
        elif name == "MT":
            return StrategyMomentum(name)
        elif name == "SP":
            return StrategySupport(name)
        else:
            return ""


class StrategyBase(object):

    @abc.abstractmethod
    def __init__(self, name):
        self.data = pandas.DataFrame()
        self.long_window = 0
        self.short_window = 0
        self.name = name
        self.simulation_window = 100

    #this method should add a column to record the trading decision on each day
    def get_result(self, data):
        data[self.name] = np.repeat(0, len(data.index))
        #self.optimize_params(data)
        return self.get_result_detail(data)

    def get_result_detail(self, data, optimizing=False):
        pos = 0
        if optimizing:
            data[self.name] = np.repeat(0, len(data.index))
        if len(data.index) >= self.long_window:
            for index in np.arange(len(data.index))[self.long_window - 1:]:
                if not optimizing and index > self.simulation_window:
                    self.optimize_params(data[index - self.simulation_window:index].copy())
                curr = self.get_trading_decision(data[index - self.long_window + 1:index + 1].copy())
                if (pos == 0 and curr == 1) or (pos == 1 and curr == -1):
                    data[self.name][data.index[index]] = curr
                    pos += (-1) ** pos
        return data

    #this method should decide the parameters for the algorithm
    @abc.abstractmethod
    def optimize_params(self, data):
        pass

    #data object expected to be a DataFrame object
    #this method should return whether we should trade on next day
    @abc.abstractmethod
    def get_trading_decision(self, data, long_window=0, short_window=0):
        long_average = np.mean(data.tail(self.long_window if long_window == 0 else long_window)['Close'])
        short_average = np.mean(data.tail(self.short_window if short_window == 0 else short_window)['Close'])
        result = short_average - long_average
        return 0 if result == 0 else np.abs(result)/result


class StrategyMovingAverage(StrategyBase):

    def __init__(self, name):
        super(StrategyMovingAverage, self).__init__(name)
        self.long_window = 15
        self.short_window = 1

    def optimize_params(self, data):
        optimized_window = 0
        result = []
        max_result = 0
        for long_window in np.arange(30)[5:]:
            self.long_window = long_window
            temp_result = BackTester.run_back_testing(self.get_result_detail(data.copy(), True), self.name)
            if optimized_window == 0 or temp_result > max_result:
                optimized_window = long_window
                max_result = temp_result
            print long_window, ":", temp_result
            if long_window > 11 and temp_result == result[-1] and temp_result == result[-2]:
                break
            else:
                result.append(temp_result)
        self.long_window = optimized_window
        print self.name, "optimized long_window:", optimized_window

    def get_trading_decision(self, data):
        try:
            long_average = np.mean(data.tail(self.long_window)['Close'])
            result = data['Close'].tolist()[-1] - long_average
        except:
            wtf = 0

        return 0 if result == 0 else np.abs(result)/result


class StrategyMovingAverageBase(StrategyBase):

    def __init__(self, name):
        super(StrategyMovingAverageBase, self).__init__(name)
        self.long_window = 15
        self.short_window = 1

    def optimize_params(self, data):
        pass

    def get_trading_decision(self, data):
        return super(StrategyMovingAverageBase, self).get_trading_decision(data, self.long_window, self.short_window)



class StrategyMomentum(StrategyBase):

    def __init__(self, name):
        super(StrategyMomentum, self).__init__(name)
        self.long_window = 26
        self.short_window = 13

    def optimize_params(self, data):
        pass

    def get_trading_decision(self, data):
        return super(StrategyMomentum, self).get_trading_decision(data, self.long_window, self.short_window)


class StrategyBollingerBand(StrategyBase):

    def __init__(self, name):
        super(StrategyBollingerBand, self).__init__(name)
        self.long_window = 30
        self.short_window = 1

    def optimize_params(self, data):
        super(StrategyBollingerBand, self).optimize_params(data)

    def get_trading_decision(self, data):
        std = np.std(data[:self.long_window-1]['Close'])
        mean = np.mean(data[:self.long_window-1]['Close'])
        upper = mean + 2 * std
        lower = mean - 2 * std
        this_price = data.tail(1)['Close'].tolist()[0]
        return -1 if this_price < lower else (1 if this_price > upper else 0)


class StrategySupport(StrategyBase):

    def __init__(self, name):
        super(StrategySupport, self).__init__(name)
        self.long_window = 5
        self.short_window = 1

    def optimize_params(self, data):
        super(StrategySupport, self).optimize_params(data)

    def get_trading_decision(self, data):
        max_price = np.max(data[:self.long_window-1]['Close'])
        min_price = np.min(data[:self.long_window-1]['Close'])
        this_price = data.tail(1)['Close'].tolist()[0]
        return -1 if this_price < min_price else (1 if this_price > max_price else 0)
