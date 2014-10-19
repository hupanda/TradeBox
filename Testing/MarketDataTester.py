__author__ = 'PacAir'
import unittest
from MarketData.MarketData import *
from MarketData.Frequency import *
from Strategy.Strategy import *
from BackTesting.BackTester import *
import pandas
import numpy as np


class MarketDataTester(unittest.TestCase):

    def setUp(self):
        self.ticker = "YAHOO/INDEX_GSPC"
        self.ref = MarketData(self.ticker)

    def action(self):
        self.data = self.ref.get_data(self.start, self.end, self.frequency)

    def test_frequency_should_return_correct_value(self):
        assert Frequency.Month.value == "monthly"

    def test_quandl_should_return_some_data(self):
        self.start = "2013-01-01"
        self.end = "2013-12-31"
        self.frequency = Frequency.Day.value
        self.action()
        assert len(self.data.index) > 0

    def test_quandl_should_return_correct_monthly_data(self):
        self.start = "2013-01-01"
        self.end = "2013-12-31"
        self.frequency = Frequency.Month.value
        self.action()
        assert len(self.data.index) == 12


class StrategyTester(unittest.TestCase):

    def setUp(self):
        self.data = pandas.DataFrame()
        self.strategyList = {"MA": "StrategyMovingAverage", "MT": "StrategyMomentum",
                             "SP": "StrategySupport", "BB": "StrategyBollingerBand"}

    def test_factory_should_return_correct_class(self):
        result = True
        for strategyName in self.strategyList:
            strategy = StrategyFactory.get_strategy(strategyName, self.data)
            result = result and strategy.__class__.__name__ == self.strategyList[strategyName]
        assert result

    def test_strategy_should_return_no_signal_given_flat_data(self):
        self.data = pandas.DataFrame(np.repeat(1, 10))
        result = []
        for strategyName in self.strategyList:
            strategy = StrategyFactory.get_strategy(strategyName, self.data)
            result.append(strategy.get_trading_decision())
        assert all(r == 0 for r in result)


class BackTestingTester(unittest.TestCase):

    def setUp(self):
        self.backTester = BackTester()
        self.data = pandas.DataFrame(np.repeat(1, 10))
        self.data["MA"] = [0] * 10

    def action(self):
        actual = BackTester.run_back_testing(self.data, "MA")
        decisions = self.data.query(self.data.MA != 0)
        expected = 1
        if len(decisions) != 0:
            for index, row in decisions.iterrows():
                expected = expected / row['Close'] if row['MA'] > 0 else expected * row['Close']

            if decisions.tail(1).MA.tolist()[0] > 0:
                expected *= self.data.tail(1).Close.tolist()[0]

        return np.abs(actual - expected) < 10 * np.finfo(float).eps

    def test_pnl_should_be_1_without_trading(self):
        self.data["Close"] = np.repeat(1, 10)
        assert self.action()

    def test_pnl_should_be_the_last_price_if_buy_n_hold(self):
        self.data["Close"] = np.random.rand(10, 1)
        self.decision_setup([0], [])
        assert self.action()

    def test_pnl_should_be_the_price_diff_if_buy_n_sell_once(self):
        self.data["Close"] = np.random.rand(10, 1)
        pos = np.random.randint(0, 9, 2)
        self.decision_setup([pos[0]], [pos[1]])
        assert self.action()

    def test_pnl_should_be_the_price_diff_if_buy_n_sell_twice(self):
        self.data["Close"] = np.random.rand(10, 1)
        pos = np.random.randint(0, 9, 4)
        self.decision_setup([pos[0], pos[2]], [pos[1], pos[3]])
        assert self.action()

    def decision_setup(self, buys, sells):
        for buy in buys:
            self.data["MA"][buy] = 1
        for sell in sells:
            self.data["MA"][sell] = -1