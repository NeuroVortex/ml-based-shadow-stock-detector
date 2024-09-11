from src.Common.Contract.Market.Orderbook import OrderbookRow
from dataclasses import dataclass


@dataclass(frozen=True)
class Orderbook:
    bids: list[OrderbookRow]
    asks: list[OrderbookRow]

    def to_dict(self):
        return {
            "bids": list(map(lambda x: x.to_dict(), self.bids)),
            "asks": list(map(lambda x: x.to_dict(), self.asks))
        }
