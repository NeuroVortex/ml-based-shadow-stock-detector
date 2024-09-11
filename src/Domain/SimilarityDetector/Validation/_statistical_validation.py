import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from statsmodels.tsa.stattools import coint
from sklearn.metrics import mean_squared_error


class StatisticalValidator:
    def __init__(self):
        self.__pearson_coefficient = 0.95
        self.__co_integration_coefficient = 0.05
        self.__RSME_threshold = 5

    def validate(self, candle_1, candle_2):
        candle_1['Returns'] = candle_1['Close'].pct_change()
        candle_2['Returns'] = candle_2['Close'].pct_change()

        result = [self.pearson(candle_1, candle_2),
                  self.co_integration(candle_1, candle_2),
                  self.root_mean_squared_error(candle_1, candle_2)]
        return result

    def pearson(self, df_1, df_2):

        corr, p_value = pearsonr(df_1['Returns'].dropna(), df_2['Returns'].dropna())
        if corr > self.__pearson_coefficient and p_value < 0.05:
            print("The returns are highly correlated.")
            return True

        else:
            print("The returns are not sufficiently correlated.")
            return False

    def co_integration(self, df_1, df_2):

        score, p_value, _ = coint(df_1['Close'], df_2['Close'])
        if p_value < self.__co_integration_coefficient:
            print("The series are co-integrated.")
            return True
        else:
            print("No co-integration found.")
            return False

    def root_mean_squared_error(self, df_1, df_2):
        rmse = np.sqrt(np.mean((df_1['Returns'] - df_2['Returns']) ** 2))

        # Calculate mean and range of returns
        mean_returns = np.mean(df_1['Returns'])
        range_returns = np.max(df_1['Returns']) - np.min(df_1['Returns'])

        # Calculate RMSE as a percentage of the mean of returns
        rmse_percentage_mean = (rmse / mean_returns) * 100

        # Calculate RMSE as a percentage of the range of returns
        rmse_percentage_range = (rmse / range_returns) * 100

        rmse = np.sqrt(mean_squared_error(df_1['Returns'].dropna(), df_2['Returns'].dropna()))
        print(f'RMSE: {rmse}')
        print(f'Mean of Returns: {mean_returns}')
        print(f'Range of Returns: {range_returns}')
        print(f'RMSE as Percentage of Mean: {rmse_percentage_mean:.2f}%')
        print(f'RMSE as Percentage of Range: {rmse_percentage_range:.2f}%')

        # Define an RMSE threshold that makes sense for your context
        if rmse < self.__RSME_threshold:
            print("The returns are close enough to be considered nearly identical.")
            return True

        else:
            print("The returns differ more than the acceptable threshold.")
            return False
