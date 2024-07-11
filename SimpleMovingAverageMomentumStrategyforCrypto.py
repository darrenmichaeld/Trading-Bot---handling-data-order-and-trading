from AlgorithmImports import *

class CryptoMomentumAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set start date
        self.SetEndDate(2022, 1, 1)    # Set end date
        self.SetCash(100000)           # Set strategy cash
        
        # Add BTC to the algorithm
        self.btc = self.AddCrypto("BTCUSD", Resolution.Daily).Symbol
        
        # Define moving average period
        self.moving_average_period = 50
        
        # Create a Simple Moving Average indicator
        self.moving_average = self.SMA(self.btc, self.moving_average_period, Resolution.Daily)

    def OnData(self, data):
        if not data.ContainsKey(self.btc):
            return
        
        # Check if moving average is ready
        if not self.moving_average.IsReady:
            return

        price = data[self.btc].Close
        moving_average = self.moving_average.Current.Value

        # Buy when price is above the moving average
        if price > moving_average and not self.Portfolio[self.btc].Invested:
            self.SetHoldings(self.btc, 1)
        
        # Sell when price is below the moving average
        elif price < moving_average and self.Portfolio[self.btc].Invested:
            self.Liquidate(self.btc)
