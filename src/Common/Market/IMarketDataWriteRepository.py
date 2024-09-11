from abc import abstractmethod
from .IMarketDataReadRepository import IMarketDataReadRepository
from ..Contract.Market import Orderbook, CandleStickTimeFrame, MarketCandleStick


class IMarketDataWriteRepository(IMarketDataReadRepository):

    @abstractmethod
    def add_market(self, ticker: str):
        raise NotImplementedError

    @abstractmethod
    def remove_market(self, ticker: str):
        raise NotImplementedError

    @abstractmethod
    def update_orderbook(self, ticker: str, orderbook: Orderbook):
        raise NotImplementedError

    @abstractmethod
    def update_candle(self, ticker: str,
                      time_frame: CandleStickTimeFrame,
                      candles: MarketCandleStick):
        raise NotImplementedError
