__author__ = 'PacAir'
import unittest
from Strategy.Strategy import *


class StrategyTester(unittest.TestCase):

    def setUp(self):
        self.data = 1
        self.factory = StrategyFactory()

    def test_factory_should_return_correct_class(self):
        strategy1 = self.factory.get_strategy("MA", self.data)
        strategy2 = self.factory.get_strategy("MT", self.data)
        strategy3 = self.factory.get_strategy("SP", self.data)
        strategy4 = self.factory.get_strategy("BB", self.data)
        result = strategy1.__class__.__name__ == "StrategyMovingAverage"
        result = result and strategy2.__class__.__name__ == "StrategyMomentum"
        result = result and strategy3.__class__.__name__ == "StrategySupport"
        result = result and strategy4.__class__.__name__ == "StrategyBolingerBound"
        self.assertTrue(result)