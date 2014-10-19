import abc


class StrategyFactory(object):

    @staticmethod
    def get_strategy(name, data):
        if name == "MA":
            return StrategyMovingAverage(data)
        elif name == "BB":
            return StrategyBollingerBand(data)
        elif name == "MT":
            return StrategyMomentum(data)
        elif name == "SP":
            return StrategySupport(data)
        else:
            return ""


class StrategyBase(object):

    def __init__(self, data):
        self.data = data

    #data object expected to be a DataFrame object
    #this method should return whether we should trade on next day
    @abc.abstractmethod
    def get_trading_decision(self, data):
        pass


class StrategyMomentum(StrategyBase):

    def get_trading_decision(self):
        return 0


class StrategyBollingerBand(StrategyBase):

    def get_trading_decision(self):
        return 0


class StrategyMovingAverage(StrategyBase):

    def get_trading_decision(self):
        return 0


class StrategySupport(StrategyBase):

    def get_trading_decision(self):
        return 0
