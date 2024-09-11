from ._date_modifier import DateModifier
from ._impute import Impute
from ._noise_reducer import NoiseReducer
from ._pca_feature_reducer import PCAFeatureReducer
from ._normalizer import DataNormalizer
from ..Plot.StockTrendPlotter import StockTrendPlotter


class PreProcessor:
    def __init__(self, plot: bool = False, time_windows_day: int = 7):
        self.__windows_hours: int = time_windows_day * 24
        self.__date_modifier = DateModifier()
        self.__impute = Impute()
        self.__noise_reducer = NoiseReducer()
        self.__pca_feature_reducer = PCAFeatureReducer()
        self.__plot = plot
        self.__plotter = StockTrendPlotter(num_columns=3)

    def pre_process(self, df_1, df_2):
        time_modified_series_1, time_modified_series_2 = self.__date_modifier.modified(df_1, df_2)
        noise_reduced_series_1 = self.__noise_reducer.reduce(time_modified_series_1)
        noise_reduced_series_2 = self.__noise_reducer.reduce(time_modified_series_2)

        if self.__plot:
            self.__plot_preprocessing(df_1, time_modified_series_1, noise_reduced_series_1)
            self.__plot_preprocessing(df_2, time_modified_series_2, noise_reduced_series_2)

        return noise_reduced_series_1, noise_reduced_series_2

    @classmethod
    def normalize(cls, series):
        return DataNormalizer.normalize(series)

    def fill_na(self, data):
        return self.__impute.fill_missing(data)

    def reduced_features(self, data_array, pca_component=3):
        return self.__pca_feature_reducer.reduce_feature(data_array, pca_component)

    def __plot_preprocessing(self, series, time_modified_series, noise_reduced_series):
        series = {'Original Series': series,
                  'time_modified_series': time_modified_series,
                  'noise_reduced_series': noise_reduced_series}
        self.__plotter.plot(candle_series=series,
                            column_name='Close',
                            x_label='Time',
                            y_label='Price',
                            title='PreProcessing')
