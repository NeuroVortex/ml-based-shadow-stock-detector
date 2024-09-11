import random
from multiprocessing import Pool

import pandas as pd
import numpy as np


class DissimilarCandleGenerator:
    def __init__(self):
        self.__base_df: pd.DataFrame | None = None

    @staticmethod
    def generate_multiprocessing_candlestick(args):
        self, price_range, volatility_range, fluctuation_range, volume_range, return_window = args
        return self.generate_sample(price_range, volatility_range, fluctuation_range, volume_range, return_window)

    @classmethod
    def __calculate_indicators(cls, candle_df):
        candle_df['EMA_12'] = candle_df['Close'].ewm(span=12, adjust=False).mean().bfill()
        candle_df['EMA_26'] = candle_df['Close'].ewm(span=26, adjust=False).mean().bfill()
        candle_df['SMA_12'] = candle_df['Close'].rolling(window=12).mean().bfill()
        candle_df['SMA_26'] = candle_df['Close'].rolling(window=26).mean().bfill()
        candle_df['Returns'] = candle_df['Close'].ffill().pct_change()
        candle_df['Cumulative_Returns'] = (1 + candle_df['Returns']).cumprod() - 1

    def __generate_hourly_candles(self, open_price, high_constraint, low_constraint, volume_range, date):
        hourly_candles = []
        previous_close = open_price

        for hour in range(24):
            volume = random.randint(*volume_range)

            # Calculate random fluctuation and price change
            fluctuation = np.random.uniform(0.001, 0.01) * previous_close
            price_change = np.random.uniform(-0.05, 0.05) * previous_close

            open_price = previous_close
            low_price = max(low_constraint, open_price - fluctuation)
            high_price = min(high_constraint, open_price + fluctuation)
            close_price = open_price + price_change

            # Ensure close price is within bounds
            close_price = max(low_price, min(close_price, high_price))

            generated_candle = {
                'OpeningTime': f'{date} {hour:02d}:00:00',
                'Open': open_price,
                'High': high_price,
                'Low': low_price,
                'Close': close_price,
                'Volume': volume,
            }

            hourly_candles.append(generated_candle)
            previous_close = close_price

        return hourly_candles

    def __generate_daily_candles(self, previous_close, volume_range):
        all_candlesticks = []

        for date, group in self.__base_df.groupby('Date'):
            daily_open = previous_close
            daily_high_constraint = daily_open * 1.05
            daily_low_constraint = daily_open * 0.95

            daily_candles = self.__generate_hourly_candles(daily_open, daily_high_constraint, daily_low_constraint, volume_range, date)
            all_candlesticks.extend(daily_candles)

            previous_close = np.mean([candle['Close'] for candle in daily_candles])

        return all_candlesticks

    def __generate_sample(self, price_range, volatility_range=(0.001, 0.99), fluctuation_range=(0.001, 0.99),
                          volume_range=(1000, 10000), return_window=0.05):

        initial_close = self.__base_df.iloc[0]['Close']
        all_candlesticks = self.__generate_daily_candles(initial_close, volume_range)

        new_df = pd.DataFrame(all_candlesticks)
        new_df['OpeningTime'] = pd.to_datetime(new_df['OpeningTime'])
        new_df.set_index('OpeningTime', inplace=True)
        return new_df

    def __ensure_non_similarity(self, sample_df):
        base_returns = self.__base_df['Returns'].dropna()
        sample_returns = sample_df['Returns'].dropna()

        # Align the indices of the base and sample returns
        aligned_base_returns, aligned_sample_returns = base_returns.align(sample_returns, join='inner')

        return not np.allclose(aligned_base_returns, aligned_sample_returns, atol=0.05)

    def generate_sample(self, price_range, volatility_range=(0.1, 0.5), fluctuation_range=(0.1, 0.5),
                        volume_range=(1000, 10000), return_window=0.05):

        try:
            return self.__generate_sample(price_range,
                                          volatility_range=volatility_range,
                                          fluctuation_range=fluctuation_range,
                                          volume_range=volume_range,
                                          return_window=return_window)

        except Exception as e:
            pass

    def generate_samples(self, goal_candle: pd.DataFrame,
                         price_range,
                         sampling_count: int = 100,
                         volatility_range=(0.001, 0.5),
                         fluctuation_range=(0.001, 0.5),
                         volume_range=(1000, 10000), return_window=0.05):
        self.__base_df = goal_candle.copy()
        self.__calculate_indicators(self.__base_df)
        self.__base_df['Date'] = self.__base_df.index.date
        print('Dissimilar sample generator start to generate samples')
        with Pool() as pool:
            tasks = [(self, price_range, volatility_range, fluctuation_range, volume_range, return_window)
                     for _ in range(sampling_count)]
            generated_candles = pool.map(DissimilarCandleGenerator.generate_multiprocessing_candlestick, tasks)

        return [candle for candle in generated_candles if candle is not None]
