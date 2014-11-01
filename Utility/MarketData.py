import Quandl


class MarketData:

    def __init__(self, ticker):
        self.ticker = ticker
        self.token = "D_evzTd5fDUQtV6WPD-v"

    def get_data(self, start, end, frequency):
        return Quandl.get(self.ticker, trim_start=start, trim_end=end, authtoken=self.token, collapse=frequency)