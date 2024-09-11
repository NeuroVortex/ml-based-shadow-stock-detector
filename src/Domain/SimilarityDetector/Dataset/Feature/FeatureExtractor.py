from multiprocessing import Pool

import pandas as pd

from src.Domain.SimilarityDetector.Dataset.Distance.DTWCalculator import DTWCalculator
from src.Domain.SimilarityDetector.Dataset.Feature.TechnicalFeatures import TechnicalFeatures
from src.Domain.SimilarityDetector.PreProcessing.pre_processor import PreProcessor


class FeatureExtractor:
    def __init__(self):
        self.__technical_feature = TechnicalFeatures
        self.__pre_processor = PreProcessor()
        self.__dtw_calculator = DTWCalculator

    @staticmethod
    def calculate_distance(args):
        self, goal_candle, (candidate_candle, result) = args
        return self._calculate_distance(goal_candle, candidate_candle), result

    def extract_sample(self, goal_candle, samples):

        with Pool() as pool:
            tasks = [(self, goal_candle, sample) for sample in samples]
            results = pool.map(FeatureExtractor.calculate_distance, tasks)

        return results

    def extract(self, goal_candle, candidate_candle):
        pct_distance, ta_distance, cumulative_return_2 = self._calculate_distance(goal_candle, candidate_candle)
        return pct_distance, ta_distance, cumulative_return_2

    def _calculate_distance(self, goal_candle, candidate_candle: pd.DataFrame):
        try:
            ts_1, ts_2 = self.__pre_processor.pre_process(goal_candle.copy(), candidate_candle)
            pct_distance, ta_distance, cumulative_return_2 = self.__track(ts_1, ts_2)
            return pct_distance, ta_distance, cumulative_return_2
        except Exception as e:
            print(e)

    def __track(self, time_series_1, time_series_2):
        ta_ts_reduced_1, cumulative_return_1 = self.__get_reduced_ta_series(time_series_1)
        ta_ts_reduced_2, cumulative_return_2 = self.__get_reduced_ta_series(time_series_2)
        ts_pct_1 = self.__technical_feature.get_price_change(time_series_1)
        ts_pct_2 = self.__technical_feature.get_price_change(time_series_2)
        pct_distance = self.__dtw_calculator.calculate(ts_pct_1.values, ts_pct_2.values)
        ta_distance = self.__dtw_calculator.calculate(ta_ts_reduced_1, ta_ts_reduced_2)
        cumulative_distance = self.__dtw_calculator.calculate(cumulative_return_1.values, cumulative_return_2.values)
        # distance = self.__weight * pct_distance + (1 - self.__weight) * ta_distance
        # print('Series Distance:', pct_distance)
        # print('Ta Distance:', ta_distance)
        # print('Ta Distance:', cumulative_distance)
        # print('Composition Distance:', distance)
        return pct_distance, ta_distance, cumulative_distance

    def __get_reduced_ta_series(self, time_series):
        ta_series = self.__technical_feature.add_ta_features(time_series)
        drop_column = ['Open', 'High', 'Low', 'Close', 'Volume', 'others_cr']
        cumulative_return = ta_series['others_cr']
        filled_ta_series = self.__pre_processor.fill_na(ta_series.drop(columns=drop_column))
        filled_cumulative_return = cumulative_return.fillna(0)
        ta_series_reduced = self.__pre_processor.reduced_features(filled_ta_series, 3)
        return ta_series_reduced, filled_cumulative_return
