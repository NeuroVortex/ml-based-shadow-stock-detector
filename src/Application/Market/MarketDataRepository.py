import threading
from typing import Union

from src.Common.Contract.Market import Orderbook, MarketCandleStick, CandleStickTimeFrame
from src.Common.Market import IMarketDataWriteRepository


class MarketDataRepository(IMarketDataWriteRepository):
    def get_market_snapshot(self):
        pass

    def __init__(self):
        self.__orderbooks: dict[str, Orderbook] = {}
        self.__candleSticks: dict[str, dict[str, MarketCandleStick]] = {}
        self.__lock = threading.RLock()

    def add_market(self, ticker: str):
        with self.__lock:
            if ticker not in self.__orderbooks:
                self.__orderbooks.update({ticker: Orderbook([], [])})

            if ticker not in self.__candleSticks:
                self.__candleSticks.update({ticker: {}})

    def remove_market(self, ticker: str):
        with self.__lock:
            self.__orderbooks.pop(ticker, None)
            self.__candleSticks.pop(ticker, None)

    def update_orderbook(self, ticker: str, orderbook: Orderbook):
        if ticker in self.__orderbooks:
            self.__orderbooks.update({ticker: orderbook})

    def update_candle(self, ticker: str, time_frame: CandleStickTimeFrame, candles: MarketCandleStick):
        self.__candleSticks.update({ticker: {time_frame.name: candles}})

    def get_orderbook(self, ticker: str) -> Orderbook:
        return self.__orderbooks.get(ticker, Orderbook([], []))

    def get_candle(self, ticker: str, time_frame: CandleStickTimeFrame) -> Union[MarketCandleStick, None]:
        time_based_candles: Union[dict, None] = self.__candleSticks.get(ticker, None)

        if time_based_candles:
            return time_based_candles.get(time_frame.name, None)

        return time_based_candles

