import abc


class StrategyFactory():

    def __init__(self):
        pass

    @staticmethod
    def get_strategy(name, data):
        if name == "MA":
            return StrategyMovingAverage(data)
        elif name == "BB":
            return StrategyBolingerBound(data)
        elif name == "MT":
            return StrategyMomentum(data)
        elif name == "SP":
            return StrategySupport(data)
        else:
            return ""


class StrategyBase(object):

    def __init__(self, data):
        self.data = data

    @abc.abstractmethod
    def get_trading_decision(self, data):
        pass


class StrategyMomentum(StrategyBase):

    def get_trading_decision(self):
        self.data


class StrategyBolingerBound(StrategyBase):

    def get_trading_decision(self):
        self.data


class StrategyMovingAverage(StrategyBase):

    def get_trading_decision(self):
        self.data


class StrategySupport(StrategyBase):

    def get_trading_decision(self):
        self.data
