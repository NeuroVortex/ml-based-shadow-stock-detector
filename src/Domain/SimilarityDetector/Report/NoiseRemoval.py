import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

from src.Domain.SimilarityDetector.Plot.CandlePlotter import CandlePlotter
from src.Domain.SimilarityDetector.PreProcessing._noise_reducer import NoiseReducer


class NoiseRemoval:

    def smooth_data(self, df: pd.DataFrame, windows=3):
        smooth = NoiseReducer().reduce(df)
        # smooth = self.__smooth_data(df, windows)
        self.close_price_plot(df, smooth)
        return smooth
        # self.__plot(df, smooth)


    @classmethod
    def __smooth_data(cls, data_frame, window=3):
        df_smoothed = data_frame.copy()
        df_smoothed['Open'] = data_frame['Open'].rolling(window=window).mean()
        df_smoothed['High'] = data_frame['High'].rolling(window=window).mean()
        df_smoothed['Low'] = data_frame['Low'].rolling(window=window).mean()
        df_smoothed['Close'] = data_frame['Close'].rolling(window=window).mean()
        df_smoothed['Volume'] = data_frame['Volume'].rolling(window=window).mean()
        df_smoothed = df_smoothed.dropna()  # Drop rows with NaN values resulting from rolling mean
        return df_smoothed

    @classmethod
    def __plot(cls, df, smoothed_df):
        CandlePlotter.plot(df)
        CandlePlotter.plot(smoothed_df)

    @classmethod
    def close_price_plot(cls, df, smooth_df):
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['Close'], label='Original Close Prices', color='blue')
        plt.plot(smooth_df.index, smooth_df['Close'], label='Smoothed Close Prices', color='red')
        plt.title('Original and Smoothed Close Prices')
        plt.xlabel('Time')
        plt.ylabel('Close Price')
        plt.legend()
        plt.show()