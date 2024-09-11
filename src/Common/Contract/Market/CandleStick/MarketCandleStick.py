from src.Common.Contract.Market.CandleStick import CandleStick
from typing import NamedTuple
import pandas as pd


class MarketCandleStick(NamedTuple):
    candles: list[CandleStick]

    def to_dataframe(self):
        data = {
            "Open": [candle.Open for candle in self.candles],
            "Low": [candle.Low for candle in self.candles],
            "High": [candle.High for candle in self.candles],
            "Close": [candle.Close for candle in self.candles],
            "Volume": [candle.Volume for candle in self.candles],
            "OpeningTime": [candle.OpeningTime for candle in self.candles]
        }

        return pd.DataFrame(data)

    def to_dict(self):
        return {
            "Open": [candle.Open for candle in self.candles],
            "Low": [candle.Low for candle in self.candles],
            "High": [candle.High for candle in self.candles],
            "Close": [candle.Close for candle in self.candles],
            "Volume": [candle.Volume for candle in self.candles],
            "OpeningTime": [candle.OpeningTime for candle in self.candles]
        }

    def to_json(self):
        return {
            "Open": [str(candle.Open) for candle in self.candles],
            "Low": [str(candle.Low) for candle in self.candles],
            "High": [str(candle.High) for candle in self.candles],
            "Close": [str(candle.Close) for candle in self.candles],
            "Volume": [str(candle.Volume) for candle in self.candles],
            "OpeningTime": [str(candle.OpeningTime) for candle in self.candles]
        }