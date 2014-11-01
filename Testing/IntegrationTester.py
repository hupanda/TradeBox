__author__ = 'PacAir'
import unittest
from Utility.MarketData import *
from Utility.Frequency import *
from Utility.BackTester import *
from Utility.ChartHelper import *
from Strategy.Strategy import *
import time


class IntegrationTester(unittest.TestCase):

    def setUp(self):
        start = "2010-01-01"
        end = "2010-12-31"
        frequency = Frequency.Day.value
        ref = MarketData("YAHOO/INDEX_GSPC")
        self.market_data = ref.get_data(start, end, frequency)
        self.data = pandas.DataFrame(np.repeat(1, len(self.market_data.index)))
        self.data['Close'] = self.market_data['Close'].tolist()
        self.strategyList = ["MA", "MT", "SP", "BB"]
        start = time.time()
        #for strategyName in self.strategyList:
        #    strategy = StrategyFactory.get_strategy(strategyName)
        #    strategy.get_result(self.data)
        #print time.time() - start

    #def test_all_strategy_at_once(self):
    #    start = time.time()
    #    for strategyName in self.strategyList:
    #        assert np.sum(self.data[strategyName]) == 1 or np.sum(self.data[strategyName]) == 0
    #    print time.time() - start

    def test_strategy_back_testing_with_chart_helper(self):
        start = time.time()
        result = BackTester.run(self.data, self.strategyList)
        print time.time() - start
        start = time.time()
        result2 = BackTester.run2(self.data, self.strategyList)
        print time.time() - start
        pnl = [col for col in result.columns if isinstance(col, str) and 'pnl' in col]
        ChartHelper().draw_chart(result[pnl], "Integration.png")
        assert result[pnl].equals(result2[pnl])

    def test_compare_ma_with_and_without_optimization(self):
        strategy_ma = StrategyFactory.get_strategy("MA")
        strategy_mab = StrategyFactory.get_strategy("MAB")
        strategy_ma.get_result(self.data)
        strategy_mab.get_result(self.data)
        result = BackTester.run2(self.data, ['MA','MAB'])
        pnl = [col for col in result.columns if isinstance(col, str) and 'pnl' in col]
        ChartHelper().draw_chart(result[pnl], "Integration_MA_optimizer_test.png")