import pandas as pd


class DateModifier:

    def modified(self, series_1: pd.DataFrame, series_2: pd.DataFrame):
        min_datetime_1, max_datetime_1 = series_1.index.min(), series_1.index.max()
        min_datetime_2, max_datetime_2 = series_2.index.min(), series_2.index.max()

        start_datetime = max(min_datetime_1, min_datetime_2)
        end_datetime = min(max_datetime_1, max_datetime_2)

        modified_series_1 = series_1[(start_datetime <= series_1.index) &
                                     (series_1.index <= end_datetime)]
        modified_series_2 = series_2[(start_datetime <= series_2.index) &
                                     (series_2.index <= end_datetime)]

        return self.__time_modification(modified_series_1, modified_series_2)

    @classmethod
    def __time_modification(cls, df_1: pd.DataFrame, df_2: pd.DataFrame):
        common_index = pd.date_range(start=min(df_1.index.min(), df_2.index.min()),
                                     end=max(df_1.index.max(), df_2.index.max()),
                                     freq='h')

        # Reindex and interpolate the series to align them on the common index
        series1_aligned = df_1.reindex(common_index).infer_objects(copy=False).interpolate(method='time')
        series2_aligned = df_2.reindex(common_index).infer_objects(copy=False).interpolate(method='time')
        series1_daily = series1_aligned.ffill().bfill()
        series2_daily = series2_aligned.ffill().bfill()
        return series1_daily, series2_daily
