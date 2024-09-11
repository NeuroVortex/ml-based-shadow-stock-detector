import time

import pandas as pd

from src.Application.Data.SampleDataStore import SampleDataStore
from src.Domain.Contract.Sampling import SamplingConf
from src.Domain.SimilarityDetector.Dataset.Feature.FeatureExtractor import FeatureExtractor
from src.Domain.SimilarityDetector.Dataset.Sampling.SampleWorker import SampleWorker


class DatasetMaker:
    def __init__(self, file_path, sampling_count, sampling_conf: SamplingConf = SamplingConf()):
        self.__feature_extractor = FeatureExtractor()
        self.__sample_worker = SampleWorker(sampling_count, sampling_conf)
        self.__file_path = file_path
        self.__data_store = SampleDataStore()
        self.__initiate()

    def __initiate(self):
        self.__datasets = pd.DataFrame(columns=['series_distance', 'ta_distance', 'return_distance', 'result'],
                                       dtype=float)

    def update_conf(self, sampling_count: int = None, sampling_conf: SamplingConf = None):
        self.__sample_worker.update_conf(sampling_count, sampling_conf)

    def generate_dataset(self, goal_candles: dict[str, pd.DataFrame]):
        candidate_candles = self.__generate_dataset(goal_candles)
        [self.__generate_features(goal_candles.get(ticker), samples) for ticker, samples in candidate_candles.items()]

    def __generate_dataset(self, candles: dict[str, pd.DataFrame]):
        candidate_candles = {}

        for ticker, candle in candles.items():
            generated_samples = self.__generate_samples(ticker, candle.copy())
            candidate_candles.update({ticker: generated_samples})

        self.__data_store.save(candidate_candles, self.__file_path)

        return candidate_candles

    def __generate_samples(self, ticker, candle: pd.DataFrame):
        print(f'Dataset generator start to generate dataset of ticker {ticker}')
        t1 = time.time()
        samples: dict[str, list[pd.DataFrame]] = self.__sample_worker.generate_sample(candle)
        t2 = time.time()
        print(f'sample generated in {t2 - t1} seconds')
        return samples

    def __generate_features(self, candle, candidate_samples: dict[str, list[pd.DataFrame]]):
        candidate = [(stock_candle, 1) for stock_candle in candidate_samples['SimilarCandles']]
        candidate += [(stock_candle, 0) for stock_candle in candidate_samples.get("DissimilarCandles")]

        results = self.__feature_extractor.extract_sample(candle, candidate)

        for result in results:
            (pct_distance, ta_distance, cumulative_return), result_value = result
            self.__submit_result(pct_distance, ta_distance, result_value)

    def __submit_result(self, pct_distance, ta_distance, result):
        # self.__datasets.loc[len(self.__datasets)] = {'series_distance': pct_distance,
        #                                              'ta_distance': ta_distance,
        #                                              'return_distance': return_distance,
        #                                              'result': result}
        self.__datasets.loc[len(self.__datasets)] = {'series_distance': pct_distance,
                                                     'ta_distance': ta_distance,
                                                     'result': result}

    @property
    def data_set(self):
        return self.__datasets
