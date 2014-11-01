__author__ = 'PacAir'
import unittest
import pandas
import numpy as np
from MarketData.MarketData import *
from MarketData.Frequency import *
from Strategy.Strategy import *


class CommonStrategyTester(unittest.TestCase):

    def setUp(self):
        self.data = pandas.DataFrame(np.repeat(1, 10))
        self.data.columns = ['Close']
        self.strategyList = {"MA": "StrategyMovingAverage", "MT": "StrategyMomentum",
                             "SP": "StrategySupport", "BB": "StrategyBollingerBand"}

    def test_factory_should_return_correct_class(self):
        result = True
        for strategyName in self.strategyList:
            strategy = StrategyFactory.get_strategy(strategyName)
            result = result and strategy.__class__.__name__ == self.strategyList[strategyName]
        assert result

    def test_strategy_should_return_no_signal_given_flat_data(self):
        result = []
        for strategyName in self.strategyList:
            strategy = StrategyFactory.get_strategy(strategyName)
            result.append(strategy.get_trading_decision(self.data))
        assert all(r == 0 for r in result)


class MAStrategyTester(unittest.TestCase):

    def setUp(self):
        self.name = "MA"
        self.data = pandas.DataFrame(np.repeat(1, 10))
        self.data.columns = ['Close']
        self.strategy = StrategyFactory.get_strategy(self.name)

    def test_strategy_should_return_buy_signal_with_last_high_price(self):
        self.data["Close"][9] = 2
        assert self.strategy.get_trading_decision(self.data) == 1

    def test_strategy_should_return_sell_signal_with_last_low_price(self):
        self.data["Close"][9] = 0.5
        assert self.strategy.get_trading_decision(self.data) == -1

    def test_strategy_should_return_1_buy_signal_with_increasing_price(self):
        self.data["Close"] = self.data.index
        result = self.strategy.get_result(self.data)
        assert np.sum(abs(result[self.name])) == 1

    def test_strategy_should_return_no_signal_with_decreasing_price(self):
        self.data["Close"] = self.data.index[::-1]
        result = self.strategy.get_result(self.data)
        assert np.sum(abs(result[self.name])) == 0

    def test_strategy_with_up_and_down_data(self):
        self.data["Close"][1:4] = 2
        result = self.strategy.get_result(self.data)
        assert np.sum(abs(result[self.name])) == 0

    def test_strategy_with_real_data(self):
        start = "2013-12-01"
        end = "2013-12-31"
        frequency = Frequency.Day.value
        ref = MarketData("YAHOO/INDEX_GSPC")
        market_data = ref.get_data(start, end, frequency)
        self.data = pandas.DataFrame(np.repeat(1, len(market_data.index)))
        self.data['Close'] = market_data['Close'].tolist()
        result = self.strategy.get_result(self.data)


class MomentumStrategyTester(MAStrategyTester):

    def setUp(self):
        self.name = "MT"
        self.data = pandas.DataFrame(np.repeat(1, 10))
        self.data.columns = ['Close']
        self.strategy = StrategyFactory.get_strategy(self.name)

    def test_strategy_with_up_and_down_data(self):
        self.data["Close"][1:4] = 2
        result = self.strategy.get_result(self.data)
        assert np.sum(abs(result[self.name])) > 0


class SupportStrategyTester(MAStrategyTester):

    def setUp(self):
        self.name = "SP"
        self.data = pandas.DataFrame(np.repeat(1, 10))
        self.data.columns = ['Close']
        self.strategy = StrategyFactory.get_strategy(self.name)


class BollingerStrategyTester(MAStrategyTester):

    def setUp(self):
        self.name = "BB"
        self.data = pandas.DataFrame(np.repeat(1, 10))
        self.data.columns = ['Close']
        self.strategy = StrategyFactory.get_strategy(self.name)