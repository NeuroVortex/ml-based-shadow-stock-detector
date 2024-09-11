from abc import abstractmethod

from src.Common.Contract.Market import CandleStickTimeFrame, MarketCandleStick, Orderbook


class IMarketDataReadRepository:

    @abstractmethod
    def get_orderbook(self, ticker: str) -> Orderbook:
        raise NotImplementedError

    @abstractmethod
    def get_candle(self, ticker: str, time_frame: CandleStickTimeFrame) -> MarketCandleStick:
        raise NotImplementedError
