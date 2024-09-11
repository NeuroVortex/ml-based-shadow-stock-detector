from decimal import Decimal
from datetime import datetime
import pandas as pd


class CandleDataFrame:
    def __init__(self, candle_price_df: pd.DataFrame, datetime_series: list[str]):
        self.__create(candle_price_df, datetime_series)

    def __create(self, candle_price_df, datetime_series):
        self.__candle = pd.DataFrame(candle_price_df, dtype=float)
        self.__candle['OpeningTime'] = pd.to_datetime(datetime_series)
        self.__candle.set_index('OpeningTime', inplace=True)
        self.__size = self.__candle.values.size

    def __transform_candle(self, candle_df: pd.DataFrame):
        self.__candle: pd.DataFrame = candle_df.loc[:].apply(
            lambda x: pd.Series(self.__transform_to_float(x), index=['Open', 'Low', 'High', 'Close', 'Volume',
                                                                     'OpeningTime']),
            axis=1)

    @property
    def candle(self):
        return self.__candle

    @property
    def size(self):
        return self.__size

    @classmethod
    def __transform_to_decimal(cls, df: pd.Series):
        return [Decimal(df['Open']), Decimal(df['Low']), Decimal(df['High']), Decimal(df['Close']),
                Decimal(df['Volume']), datetime.strptime(df['OpeningTime'], '%Y-%m-%dT%H:%M:%S')]

    @classmethod
    def __transform_to_float(cls, df: pd.Series):
        return [float(df['Open']), float(df['Low']), float(df['High']), float(df['Close']),
                float(df['Volume']), datetime.strptime(df['OpeningTime'], '%Y-%m-%dT%H:%M:%S')]
