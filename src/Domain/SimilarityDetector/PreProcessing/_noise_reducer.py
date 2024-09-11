import pandas as pd
from scipy.ndimage import gaussian_filter1d


class NoiseReducer:
    def __init__(self):
        self.__sigma = 2  # Standard deviation for Gaussian kernel

    def reduce(self, candle) -> pd.DataFrame:
        new_candle = candle
        new_candle['Open'] = gaussian_filter1d(candle['Open'], sigma=self.__sigma)
        new_candle['High'] = gaussian_filter1d(candle['High'], sigma=self.__sigma)
        new_candle['Low'] = gaussian_filter1d(candle['Low'], sigma=self.__sigma)
        new_candle['Close'] = gaussian_filter1d(candle['Close'], sigma=self.__sigma)
        return new_candle

