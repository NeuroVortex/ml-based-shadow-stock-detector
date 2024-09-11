import pandas as pd
from matplotlib import pyplot as plt

from src.Domain.Contract.Sampling.SamplingConf import SamplingConf
from src.Domain.SimilarityDetector.Dataset.Sampling.DissimilarCandleGenerator import DissimilarCandleGenerator
from src.Domain.SimilarityDetector.Dataset.Sampling.SimilarCandlestickGenerator import SimilarCandlestickGenerator


class SampleWorker:
    def __init__(self, sample_count: int = 100, sampling_conf: SamplingConf = SamplingConf()):
        self.__dis_sim_generator = DissimilarCandleGenerator()
        self.__sim_generator = SimilarCandlestickGenerator()
        self.__sampling_conf = sampling_conf
        self.__sampling_count = sample_count

    def update_conf(self, sampling_count=None, sampling_conf: SamplingConf = None):
        self.__sampling_count = sampling_count if bool(sampling_count) else self.__sampling_count
        self.__sampling_conf = sampling_conf if bool(sampling_conf) else self.__sampling_conf

    def generate_sample(self, goal_candle: pd.DataFrame) -> dict[str, list[pd.DataFrame]]:
        print('Sample Worker start to generate samples')
        generated_similar_candles = self.__sim_generator.generate_samples(
            goal_candle=goal_candle,
            sampling_count=self.__sampling_count,
            fluctuation_range=self.__sampling_conf.sim_fluctuation_range,
            volatility_range=self.__sampling_conf.sim_volatility_range,
            return_adjustment=self.__sampling_conf.sim_return_adjustment)
        generated_dissimilar_candles = self.__dis_sim_generator.generate_samples(
            goal_candle=goal_candle,
            sampling_count=self.__sampling_count,
            price_range=self.__get_price_range(goal_candle),
            fluctuation_range=self.__sampling_conf.dis_sim_fluctuation_range,
            volume_range=self.__sampling_conf.dis_sim_volume_range,
            return_window=self.__sampling_conf.return_window,
            volatility_range=self.__sampling_conf.dis_sim_volatility_range
        )

        return {
            'SimilarCandles': generated_similar_candles,
            'DissimilarCandles': generated_dissimilar_candles
        }

    @classmethod
    def __get_price_range(cls, goal_candle: pd.DataFrame):
        max_price = goal_candle['High'].max() * 2
        min_price = goal_candle['High'].min() / 2
        return max_price, min_price

    @classmethod
    def visualize(cls, base_df, sample_df):
        plt.figure(figsize=(14, 7))
        # plt.subplot(3, 1, 1)
        plt.plot(base_df.index, base_df['Close'], label='Original Close')
        plt.plot(sample_df.index, sample_df['Close'], label='Generated Close', linestyle='--')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.title('Close Prices')
        plt.legend()
        #
        # plt.subplot(3, 1, 2)
        # plt.plot(base_df.index, base_df['SMA_12'], label='Original SMA 12')
        # plt.plot(sample_df.index, sample_df['SMA_12'], label='Generated SMA 12', linestyle='--')
        # plt.plot(base_df.index, base_df['EMA_12'], label='Original EMA 12')
        # plt.plot(sample_df.index, sample_df['EMA_12'], label='Generated EMA 12', linestyle='--')
        # plt.xlabel('Time')
        # plt.ylabel('Price')
        # plt.title('SMA and EMA')
        # plt.legend()
        #
        # plt.subplot(3, 1, 3)
        # plt.plot(base_df.index, base_df['Cumulative_Returns'], label='Original Cumulative Returns')
        # plt.plot(sample_df.index, sample_df['Cumulative_Returns'], label='Generated Cumulative Returns',
        #          linestyle='--')
        # plt.xlabel('Time')
        # plt.ylabel('Cumulative Returns')
        # plt.title('Cumulative Returns Comparison')
        # plt.legend()
        #
        # plt.tight_layout()
        # plt.show()
        #
        # # Report returns for the first sample
        # base_return = base_df['Cumulative_Returns'].iloc[-1] * 100
        # new_return = sample_df['Cumulative_Returns'].iloc[-1] * 100
        #
        # print(f"Base Cumulative Return: {base_return:.2f}%")
        # print(f"Generated Cumulative Return: {new_return:.2f}%")

    @property
    def plot_styles(self):
        return ['classic', 'charles', 'mike', 'yahoo', 'nightclouds', 'sas',
                'checkers', 'brasil', 'blueskies', 'ibd', 'mexcel', 'default']
