import logging
import time

import pandas as pd

from src.Domain.Contract.Sampling import SamplingConf
from src.Domain.SimilarityDetector.Classification import Classifier
from src.Domain.SimilarityDetector.Dataset import DatasetMaker


class MLBasedSimilarityDetector:
    def __init__(self, model_name, file_path, model_path, sampling_count, sampling_conf: SamplingConf = SamplingConf()):
        self.__model_path = model_path
        self.__datasets_maker = DatasetMaker(file_path+model_name, sampling_count, sampling_conf)
        self.__classifier = Classifier(model_name)
        self.__file_path = file_path
        self.__logger = logging.getLogger(__name__)

    def update_conf(self, sampling_count: int = None, sampling_conf: SamplingConf = None):
        self.__datasets_maker.update_conf(sampling_count, sampling_conf)

    def start(self, goal_candles: dict[str, pd.DataFrame]):
        if not self.__classifier.load_model(self.__model_path):
            self.train(goal_candles)

    def train(self, goal_candles: dict[str, pd.DataFrame]):
        print('Similarity Detector start to Running')
        t_1 = time.time()
        self.__prepare_datasets(goal_candles)
        t_2 = time.time()
        print(f'Data Set Generated in {t_2 - t_1} seconds')
        self.__train()
        t_3 = time.time()
        print(f'Model Trained in {t_3 - t_2} seconds')

    def __prepare_datasets(self, goal_candles):
        self.__datasets_maker.generate_dataset(goal_candles)

    def __train(self):
        self.__classifier.train(self.__datasets_maker.data_set)
        self.__classifier.validate()
        self.__classifier.save_model(self.__model_path)

    def is_similar(self, pct_distance: float, ta_distance: float, cumulative_return: float):
        feature = pd.DataFrame({'series_distance': [pct_distance],
                                'ta_distance': [ta_distance],
                                'return_distance': [cumulative_return]}, dtype=float)
        return self.__classifier.is_similar(feature)
