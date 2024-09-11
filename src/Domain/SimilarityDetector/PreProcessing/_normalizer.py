import pandas as pd


class DataNormalizer:

    @classmethod
    def normalize(cls, data_series: pd.Series) -> pd.Series:
        return (data_series - data_series.min()) / (data_series.max() - data_series.min())
