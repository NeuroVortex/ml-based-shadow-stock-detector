from multiprocessing import Pool

import pandas as pd
import numpy as np


class SimilarCandlestickGenerator:
    def __init__(self):
        self.__base_df: pd.DataFrame | None = None
        self.__daily_summary = None
        self.__counter = 0

    @staticmethod
    def generate_multiprocessing_candlestick(args):
        self, fluctuation_range, volatility_range, return_adjustment = args
        return self.generate_sample(fluctuation_range, volatility_range, return_adjustment)

    @classmethod
    def __calculate_indicators(cls, candle_df):
        candle_df['EMA_12'] = candle_df['Close'].ewm(span=12, adjust=False).mean()
        candle_df['EMA_26'] = candle_df['Close'].ewm(span=26, adjust=False).mean()
        candle_df['SMA_12'] = candle_df['Close'].rolling(window=12).mean()
        candle_df['SMA_26'] = candle_df['Close'].rolling(window=26).mean()
        candle_df['Returns'] = candle_df['Close'].pct_change()
        candle_df['Cumulative_Returns'] = (1 + candle_df['Returns']).cumprod() - 1

    def __calculate_daily_summary(self):
        daily_summary = self.__base_df.groupby('Date').agg({
            'Open': 'first',
            'Close': 'last'
        }).reset_index()
        daily_summary['Daily_Percentage_Change'] = ((daily_summary['Close'] - daily_summary['Open']) / daily_summary[
            'Open']) * 100
        daily_summary['Direction'] = daily_summary['Daily_Percentage_Change'].apply(
            lambda x: 'Rising' if x > 0 else 'Falling' if x < 0 else 'No Change'
        )
        return daily_summary

    def __generate_candlesticks(self, return_adjustment, fluctuation_range=(-0.05, 0.05),
                                volatility_range=(-0.02, 0.02)):
        new_data = []
        previous_close = self.__base_df['Close'].iloc[0]

        for idx, row in self.__daily_summary.iterrows():
            date = row['Date']
            direction = row['Direction']

            for timestamp in self.__base_df[self.__base_df['Date'] == date].index:
                if timestamp == self.__base_df[self.__base_df['Date'] == date].index[0]:
                    open_price = previous_close
                else:
                    open_price = close_price

                sma_value = self.__base_df.loc[timestamp, 'SMA_12']
                ema_value = self.__base_df.loc[timestamp, 'EMA_12']

                fluctuation = np.random.uniform(*fluctuation_range)  # Random fluctuation between -5% and +5%
                volatility = np.random.uniform(*volatility_range)  # Random volatility between -2% and +2%

                if direction == 'Rising':
                    close_price = ema_value * (1 + abs(fluctuation)) * (1 + abs(volatility))
                elif direction == 'Falling':
                    close_price = ema_value * (1 - abs(fluctuation)) * (1 - abs(volatility))
                else:
                    close_price = ema_value * (1 + fluctuation) * (1 + volatility)

                high_price = max(open_price, close_price) * (1 + abs(np.random.uniform(*fluctuation_range)))
                low_price = min(open_price, close_price) * (1 - abs(np.random.uniform(*fluctuation_range)))

                volume = self.__base_df['Volume'].mean() * np.random.uniform(0.9, 1.1)

                new_data.append({
                    'OpeningTime': timestamp,
                    'Open': open_price,
                    'High': high_price,
                    'Low': low_price,
                    'Close': close_price,
                    'Volume': volume
                })

                previous_close = close_price

        new_df = pd.DataFrame(new_data)
        new_df.set_index('OpeningTime', inplace=True)
        self.__calculate_indicators(new_df)
        new_df = self.__adjust_returns(new_df, return_adjustment)
        return new_df

    def __adjust_returns(self, new_df, return_adjustment: float = 0.02):
        base_cumulative_return = self.__base_df['Cumulative_Returns'].iloc[-1]
        new_df['Returns'] = new_df['Close'].pct_change()
        new_df['Cumulative_Returns'] = (1 + new_df['Returns']).cumprod() - 1

        new_cumulative_return = new_df['Cumulative_Returns'].iloc[-1]
        adjustment_factor = base_cumulative_return / new_cumulative_return

        random_adjustment = np.random.uniform(-return_adjustment, return_adjustment)
        adjusted_factor = adjustment_factor * (1 + random_adjustment)
        new_df['Close'] = new_df['Close'] * adjusted_factor
        new_df['Open'] = new_df['Open'] * adjusted_factor
        new_df['High'] = new_df['High'] * adjusted_factor
        new_df['Low'] = new_df['Low'] * adjusted_factor

        new_df['Returns'] = new_df['Close'].pct_change()
        new_df['Cumulative_Returns'] = (1 + new_df['Returns']).cumprod() - 1

        return new_df

    def __generate_sample(self, fluctuation_range=(0.0001, 0.001), volatility_range=(0.0001, 0.001),
                          return_adjustment=0.02):
        sample_df = self.__generate_candlesticks(return_adjustment, fluctuation_range, volatility_range)
        base_cumulative_return = self.__base_df['Cumulative_Returns'].iloc[-1]
        new_cumulative_return = sample_df['Cumulative_Returns'].iloc[-1]

        # Adjust returns to ensure the difference is within 5%
        while abs(new_cumulative_return - base_cumulative_return) > abs(return_adjustment):
            sample_df = self.__generate_candlesticks(return_adjustment, fluctuation_range, volatility_range)
            new_cumulative_return = sample_df['Cumulative_Returns'].iloc[-1]

        return sample_df.drop(columns=['Cumulative_Returns', 'EMA_12', 'EMA_26', 'SMA_12', 'SMA_26', 'Returns'])

    def generate_sample(self, fluctuation_range=(0.0001, 0.001), volatility_range=(0.0001, 0.001),
                        return_adjustment=0.02):
        print(f'Generating sample number {self.__counter}')
        try:
            return self.__generate_sample(fluctuation_range, volatility_range, return_adjustment)

        except Exception as e:
            pass

    def generate_samples(self, goal_candle: pd.DataFrame,
                         sampling_count: int, fluctuation_range=(0.0001, 0.001),
                         volatility_range=(0.0001, 0.001),
                         return_adjustment=0.02):
        self.__base_df = goal_candle.copy()
        self.__calculate_indicators(self.__base_df)
        self.__base_df['Date'] = self.__base_df.index.date
        self.__daily_summary = self.__calculate_daily_summary()
        self.__counter = 0
        print('Similar sample generator start to generate samples')

        with Pool() as pool:
            tasks = [(self, fluctuation_range, volatility_range, return_adjustment) for _ in range(sampling_count)]
            results = pool.map(SimilarCandlestickGenerator.generate_multiprocessing_candlestick, tasks)

        return [candle for candle in results if candle is not None]


