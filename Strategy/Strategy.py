import abc
import pandas
import numpy as np
from BackTesting.BackTester import *
from scipy.optimize import minimize


class StrategyFactory(object):

    @staticmethod
    def get_strategy(name):
        if name == "MA":
            return StrategyMovingAverage(name)
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

    #this method should add a column to record the trading decision on each day
    def get_result(self, data):
        self.optimize_params(data)
        data[self.name] = np.repeat(0, len(data.index))
        pos = 0
        if len(data.index) >= self.long_window:
            for index, row in data[self.long_window - 1:].iterrows():
                curr = self.get_trading_decision(data[index - self.long_window + 1:index + 1])
                if (pos == 0 and curr == 1) or (pos == 1 and curr == -1):
                    data[self.name][index] = curr
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
        print long_average, short_average
        result = short_average - long_average
        return 0 if result == 0 else np.abs(result)/result


class StrategyMovingAverage(StrategyBase):

    def __init__(self, name):
        super(StrategyMovingAverage, self).__init__(name)
        self.long_window = 5
        self.short_window = 1

    def optimize_params(self, data):
        pass

    def get_trading_decision(self, data):
        return super(StrategyMovingAverage, self).get_trading_decision(data, self.long_window, self.short_window)
        #result = data.irow(len(data.index)-1)['Close'] - np.mean(data[:len(data.index)]['Close'])
        #return 0 if result == 0 else np.abs(result)/result


class StrategyMomentum(StrategyBase):

    def __init__(self, name):
        super(StrategyMomentum, self).__init__(name)
        self.long_window = 5
        self.short_window = 4

    def optimize_params(self, data):
        pass

    def get_trading_decision(self, data):
        return super(StrategyMomentum, self).get_trading_decision(data, self.long_window, self.short_window)


class StrategyBollingerBand(StrategyBase):

    def __init__(self, name):
        super(StrategyBollingerBand, self).__init__(name)
        self.long_window = 5
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
