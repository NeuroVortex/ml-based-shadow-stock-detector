import random
from multiprocessing import Pool

import pandas as pd
import numpy as np


class DissimilarCandleGeneratorOld:
    def __init__(self, base_df):
        self.__base_df: pd.DataFrame = base_df
        self.__calculate_indicators(self.__base_df)
        self.__base_df['Date'] = self.__base_df.index.date
        self.__counter = 0

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

    def __generate_sample(self, price_range, volatility_range=(0.001, 0.99), fluctuation_range=(0.001, 0.99),
                          volume_range=(1000, 10000), return_window=0.05):

        candlesticks = []

        def is_similar_to_base_or_previous(base_row, generated, previous):
            # Check trend similarity with base candle
            base_trend = np.sign(base_row['Close'] - base_row['Open'])
            generated_trend = np.sign(generated['Close'] - generated['Open'])
            if random.choice([False, False, True, False, True]) and base_trend == generated_trend:
                return True

            # Check similarity with the previous candle
            if previous is not None:
                previous_trend = np.sign(previous['Close'] - previous['Open'])
                if random.choice([False, False, True, False, True]) and previous_trend == generated_trend:
                    return True

                # Check return similarity with previous candle
                previous_return = (previous['Close'] - previous['Open']) / previous['Open']
                generated_return = (generated['Close'] - generated['Open']) / generated['Open']
                if abs(previous_return - generated_return) < return_window:
                    return True

            return False

        # Initialize the open price for the first candle
        open_price = np.random.uniform(*price_range)
        previous_candle = None

        for dt, row in self.__base_df.iterrows():
            attempts = 0
            while True:
                # Avoid infinite loop
                if attempts > 1000:
                    raise ValueError("Unable to generate a sufficiently different candlestick")
                attempts += 1

                volatility_ratio = np.random.uniform(*volatility_range)
                fluctuation_ratio = np.random.uniform(*fluctuation_range)
                # Apply volatility and fluctuation to price changes
                price_change = np.random.uniform(0, volatility_ratio * abs(open_price))
                fluctuation = fluctuation_ratio * open_price

                high_price = open_price + abs(np.random.uniform(0, fluctuation))
                low_price = max(price_range[0], open_price - abs(np.random.uniform(0, fluctuation)))
                close_price = max(price_range[0], open_price + price_change)

                # Ensure high is the highest and low is the lowest
                high_price = max(high_price, close_price, open_price)
                low_price = min(low_price, close_price, open_price)

                # Generate random volume within the specified range
                volume = np.random.randint(*volume_range)

                generated_candle = {
                    'OpeningTime': dt,
                    'Open': open_price,
                    'High': high_price,
                    'Low': low_price,
                    'Close': close_price,
                    'Volume': volume,
                }

                # Check if the generated candle is similar to the base candle or the previous candle
                if not is_similar_to_base_or_previous(row, generated_candle, previous_candle):
                    break

            candlesticks.append(generated_candle)
            previous_candle = generated_candle

            # Set the close price of this candle as the open price for the next candle
            open_price = close_price

        new_df = pd.DataFrame(candlesticks)
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
        print(f'Generating dissimilar sample number {self.__counter}')
        try:
            return self.__generate_sample(price_range,
                                          volatility_range=volatility_range,
                                          fluctuation_range=fluctuation_range,
                                          volume_range=volume_range,
                                          return_window=return_window)

        except Exception as e:
            pass

    def generate_samples(self, price_range,
                         sampling_count: int = 100,
                         volatility_range=(0.001, 0.5),
                         fluctuation_range=(0.001, 0.5),
                         volume_range=(1000, 10000), return_window=0.05):
        self.__counter = 0
        print('Dissimilar sample generator start to generate samples')
        with Pool() as pool:
            tasks = [(self, price_range, volatility_range, fluctuation_range, volume_range, return_window)
                     for _ in range(sampling_count)]
            generated_candles = pool.map(DissimilarCandleGeneratorOld.generate_multiprocessing_candlestick, tasks)

        return [candle for candle in generated_candles if candle is not None]
