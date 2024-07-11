from AlgorithmImports import *

class CryptoBollingerBandsAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2022, 1, 1)
        self.SetCash(100000)
        
        self.btc = self.AddCrypto("BTCUSD", Resolution.Daily).Symbol
        
        self.bollinger_period = 20
        self.bollinger_std_dev = 2
        
        self.bollinger = self.BB(self.btc, self.bollinger_period, self.bollinger_std_dev, MovingAverageType.Simple, Resolution.Daily)

    def OnData(self, data):
        if not data.ContainsKey(self.btc):
            return
        
        if not self.bollinger.IsReady:
            return

        price = data[self.btc].Close
        upper_band = self.bollinger.UpperBand.Current.Value
        lower_band = self.bollinger.LowerBand.Current.Value
        middle_band = self.bollinger.MiddleBand.Current.Value

        # Calculate position size based on the width of the Bollinger Bands
        band_width = upper_band - lower_band
        position_size = 0.01 * band_width / middle_band  # Example position sizing formula
        
        # Buy when price touches or falls below the lower Bollinger Band
        if price <= lower_band and not self.Portfolio[self.btc].Invested:
            self.SetHoldings(self.btc, position_size)
        
        # Sell when price touches or rises above the upper Bollinger Band
        elif price >= upper_band and self.Portfolio[self.btc].Invested:
            self.Liquidate(self.btc)
