# region imports
from AlgorithmImports import *
# endregion

class RetrospectiveFluorescentPinkCamel(QCAlgorithm):
    def initialize(self):
        self.set_start_date(2020, 1, 10)
        self.set_end_date(2022, 1, 10)
        self.set_cash(100000)
        self.spy = self.add_equity("SPY", Resolution.Daily).symbol

        self.movingAverage = self.sma("SPY", 30, Resolution.Daily)
        closingPrice = self.history(self.spy, 30, Resolution.Daily)["close"]
        for time, price in closingPrice.loc[self.spy].items():
            self.movingAverage.update(time, price)

    def on_data(self, data: Slice):
        if not self.movingAverage.IsReady:
            return
        
        hist = self.history(self.spy, timedelta(365), Resolution.Daily)
        low = min(hist["low"])
        high = min(hist["high"])

        price = self.securities[self.spy].price

        if price * 1.05 >= high and self.sma.current.value < price:
            if not self.portfolio[self.spy].is_long:
                self.set_holdings(self.spy,1)
        elif price * 0.95 <= low and self.sma.current.value > price:
            if not self.portfolio[self.spy].is_short:
                self.set_holdings(self.spy,-1)
        else:
            self.liquidate()

        self.Plot("BenchMark", "High", high)
        self.Plot("BenchMark", "Low", low)
        self.Plot("BenchMark", "SMA", movingAverage)
