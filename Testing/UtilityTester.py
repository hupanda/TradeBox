__author__ = 'PacAir'
import unittest
import concurrent
from MarketData.MarketData import *
from MarketData.Frequency import *
from BackTesting.BackTester import *
import pandas
import numpy as np
import time
import concurrent.futures


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


class BackTestingTester(unittest.TestCase):

    def setUp(self):
        self.backTester = BackTester()
        self.data = pandas.DataFrame(np.repeat(1, 10))
        self.data["MA"] = [0] * 10

    def tearDown(self):
        print "Actual", self.actual, " | Expected", self.expected, " | Diff", self.expected - self.actual

    def action(self):
        self.actual = BackTester.run_back_testing(self.data, "MA")
        self.expected = 1
        decisions = self.data.query(self.data.MA != 0)
        if len(decisions) != 0:
            for index, row in decisions.iterrows():
                self.expected = self.expected / row['Close'] if row['MA'] > 0 else self.expected * row['Close']

            if decisions.tail(1).MA.tolist()[0] > 0:
                self.expected *= self.data.tail(1).Close.tolist()[0]

        return np.abs(self.actual - self.expected) < 10 * np.finfo(float).eps

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


def try_multiple_operations(item):
    new_value = item**1000


class POCTester(unittest.TestCase):

    def setUp(self):
        pass

    def test_multi_threading(self):

        start = time.time()
        for number in np.random.rand(100, 1):
            try_multiple_operations(number)
        print time.time() - start

        start = time.time()
        executor = concurrent.futures.ProcessPoolExecutor(10)
        future = [executor.submit(try_multiple_operations, number) for number in np.random.rand(100, 1)]
        concurrent.futures.wait(future)
        print time.time() - start

