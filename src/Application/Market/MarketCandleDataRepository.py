import pandas as pd


class MarketCandleDataRepository:

    def __init__(self):
        self.__candle_repo: dict[str, pd.DataFrame] = {}

    def add_or_update(self, ticker, candle: pd.DataFrame):
        self.__candle_repo.update({ticker: candle})

    def get_by_ticker(self, ticker: str) -> pd.DataFrame:
        return self.__candle_repo.get(ticker).copy()

    def get_candles(self) -> dict[str, pd.DataFrame]:
        return self.__candle_repo.copy()

    def get_tickers(self) -> list[str]:
        return list(self.__candle_repo.keys())
