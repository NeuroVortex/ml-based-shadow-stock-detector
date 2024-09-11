from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

from src.Domain.SimilarityDetector.PreProcessing import PreProcessor


class DTWCalculator:

    @classmethod
    def calculate(cls, time_series_1, time_series_2):
        ts1_normalized = PreProcessor.normalize(time_series_1)
        ts2_normalized = PreProcessor.normalize(time_series_2)
        distance, _ = fastdtw(ts1_normalized.reshape(-1, 1), ts2_normalized.reshape(-1, 1), dist=euclidean)
        return distance
