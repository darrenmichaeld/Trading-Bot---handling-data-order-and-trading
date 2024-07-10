# region imports
from AlgorithmImports import *
# endregion

class FocusedFluorescentPinkAntelope(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2023, 1, 9)
        self.set_end_date(2024, 1, 9)
        self.set_cash(100000)
        self.spy = self.add_equity("SPY", Resolution.Hour).Symbol

        # Initializing data, entry ticket, stop market ticket, entry time, stop order fill time, and highest price
        self.entryTicket = None
        self.stopMarketTicket = None
        self.entryTime = datetime.min
        self.stopOrderFillTime = datetime.min
        self.highestPrice = 0

    def on_data(self, data: Slice):
        # waiting 30 days after last exit
        if(self.time - self.stopOrderFillTime).days < 30:
            return

        # set price
        price = self.securities[self.spy].price
        
        # send entry limit order
        if not self.portfolio.invested and not self.transactions.get_open_orders(self.spy):
            quantity = self.calculate_order_quantity(self.spy, 0.9)
            self.entryTicket = self.limit_order(self.spy, quantity, price, "Entry Order")
            self.entryTime = self.time

        # move limit price if not filled after 1 day
        if(self.time - self.entryTime).days > 1 and self.entryTicket.status != OrderStatus.Filled:
            self.entryTime = self.time
            updateFields = UpdateOrderFields()
            updateFields.limit_price = price
            self.entryTicket.update(updateFields)

        # move trailing stop price
        if self.stopMarketTicket is not None and self.portfolio.invested:
            if price > self.highestPrice:
                self.highestPrice = price
                updateFields = UpdateOrderFields()
                updateFields.stop_price = price * 0.95
                self.stopMarketTicket.update(updateFields)
        pass

    def onOrderEvent(self, orderEvent):
        # condition where the order has not been filled
        if OrderStatus.status != OrderStatus.filled:
            return

        # send stop loss order if entry limit order is filled
        if self.entryTicket is not None and self.entryTicket.order_id == OrderEvent.order_id:
            self.stopMarketTicket = self.stop_market_order(self.spy, -self.entryTicket.quantity, 0.95 * self.entryTicket.average_fill_price)
            
        # safe fill time or stop loss order time
        if self.stopMarketTicket is not None and self.stopMarketTicket.order_id == OrderEvent.order_id:
            self.stopOrderFillTime = self.time
            self.highestPrice = 0
        pass
           
