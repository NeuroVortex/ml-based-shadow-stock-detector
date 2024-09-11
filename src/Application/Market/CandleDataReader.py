import json

from src.Common.Contract.Market.CandleStick.candle_df import CandleDataFrame
from src.Application.Market.MarketCandleDataRepository import MarketCandleDataRepository


class CandleDataReader:
    def __init__(self, market_data_repo: MarketCandleDataRepository, stock_num: float = None,
                 specific_asset: list[str] = None):
        self.__data_repo = market_data_repo
        self.__stock_num = stock_num
        self.__specific_asset = specific_asset if bool(specific_asset) else []

    @classmethod
    def __read(cls, file_address: str) -> dict:
        file = open(file_address, encoding="utf-8")
        _candles = json.load(file)
        file.close()
        return _candles

    def read_from_file(self, file_address: str):
        _candles = self.__read(file_address)
        self.__serializer(_candles)

    def read_from_dict(self, _candles: dict):
        self.__serializer(_candles)

    def __serializer(self, _candles: dict):
        self.__stock_num = self.__stock_num if self.__stock_num is not None else len(_candles['tickers'])
        for ticker, candle in list(_candles['tickers'].items())[:self.__stock_num]:
            candle_price = candle.copy()
            datetime_series = candle['OpeningTime']
            candle_price.pop('OpeningTime')
            candle_df = CandleDataFrame(candle_price_df=candle_price, datetime_series=datetime_series)
            self.__data_repo.add_or_update(ticker, candle_df.candle)

        for ticker in self.__specific_asset:
            candle = _candles['tickers'].get(ticker, None)
            if candle:
                candle_price = candle.copy()
                datetime_series = candle['OpeningTime']
                candle_price.pop('OpeningTime')
                candle_df = CandleDataFrame(candle_price_df=candle_price, datetime_series=datetime_series)
                self.__data_repo.add_or_update(ticker, candle_df.candle)


