import pandas as pd

from ._back_tester import BackTester
from ._statistical_validation import StatisticalValidator


class Validator:
    def __init__(self):
        self.__statistical_validator = StatisticalValidator()
        self.__back_tester = BackTester()

    def validate(self, candlesticks_1: pd.DataFrame, candlesticks_2: pd.DataFrame) -> bool:

        if (self.__statistical_validator.validate(candlesticks_1, candlesticks_2) and
                self.__back_tester.back_test(candlesticks_1, candlesticks_2)):
            return True

        else:
            return False
