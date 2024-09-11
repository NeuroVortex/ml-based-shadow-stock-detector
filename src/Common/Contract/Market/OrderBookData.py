from .OrderData import OrderData
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderBookData:
    bids: list[OrderData]
    asks: list[OrderData]

    def changeToDict(self):
        return {
            "bids": list(map(lambda x: x.__dict__, self.bids)),
            "asks": list(map(lambda x: x.__dict__, self.asks))
        }
