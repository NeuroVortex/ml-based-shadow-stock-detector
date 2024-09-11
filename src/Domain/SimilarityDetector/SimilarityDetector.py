from multiprocessing import Pool

import pandas as pd

from src.Application.Market.MarketCandleDataRepository import MarketCandleDataRepository
import logging

from src.Domain.SimilarityDetector.Dataset.Feature.FeatureExtractor import FeatureExtractor
from src.Domain.SimilarityDetector.MLBasedSimilarityDetector import MLBasedSimilarityDetector
from src.Domain.SimilarityDetector.Plot.StockTrendPlotter import StockTrendPlotter


class SimilarityDetector:
    def __init__(self, file_path: str, model_name: str, model_path: str, data_repo: MarketCandleDataRepository,
                 plot=False):
        self.__data_repo = data_repo
        self.__plotter = StockTrendPlotter()
        self.__plot_chart = plot
        self.__similar_stocks = []
        self.__logger = logging.getLogger(__name__)
        self.__initiate(file_path, model_name, model_path)

    def __initiate(self, file_path, model_name, model_path):
        self.__candles: dict[str, pd.DataFrame] = self.__data_repo.get_candles()
        self.__feature_extractor = FeatureExtractor()
        self.__similarity_detector = MLBasedSimilarityDetector(model_name=model_name,
                                                               model_path=model_path,
                                                               file_path=file_path,
                                                               sampling_count=40)

    def __update(self):
        self.__candles = self.__data_repo.get_candles()

    def start(self):
        self.__similarity_detector.start(self.__candles)

    def train(self):
        self.__similarity_detector.train(self.__candles)

    @staticmethod
    def calculate_parallel(args):
        self, ticker, goal_candle, candle = args
        return self._calculate(goal_candle, candle), ticker

    def calculate(self, goal_ticker, goal_candle):

        similar_stocks = []

        if bool(goal_candle.size):
            with Pool() as pool:
                tasks = [(self, ticker, goal_candle, candidate_candle) for
                         ticker, candidate_candle in self.__candles.items()]
                result = pool.map(SimilarityDetector.calculate_parallel, tasks)

        for (is_similar, ticker) in result:
            if is_similar:
                similar_stocks.append(ticker)

        self.__similar_stocks = similar_stocks

        if self.__plot_chart:
            self.__plot_result(goal_ticker, similar_stocks)

        return similar_stocks

    def _calculate(self, goal_candle, candidate_candle):
        pct_distance, ta_distance, cumulative_return = self.__feature_extractor.extract(goal_candle, candidate_candle)
        is_similar = self.__similarity_detector.is_similar(pct_distance, ta_distance, cumulative_return)
        print(f"series distance: {pct_distance}, "
              f"ta distance: {ta_distance},"
              f" cumulative distance: {cumulative_return}, "
              f"similarity: {is_similar}")
        return True if is_similar else False

    def __plot_result(self, goal_ticker, similar_tickers: list[str]):

        for ticker in similar_tickers:
            self.__plot(goal_ticker, ticker)

    def __plot(self, goal_ticker, ticker: str):
        series = {goal_ticker: self.__candles.get(goal_ticker).candle,
                  ticker: self.__candles.get(ticker).candle}
        self.__plotter.plot(candle_series=series,
                            column_name='Close',
                            x_label='Time',
                            y_label='Price',
                            title='Compare Similarity')

    @property
    def similar_stocks(self):
        return self.__similar_stocks
