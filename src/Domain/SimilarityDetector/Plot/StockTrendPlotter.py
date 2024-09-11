import matplotlib.pyplot as plt
import pandas as pd


class StockTrendPlotter:
    def __init__(self, num_columns=2):
        self.__num_columns = num_columns  # Controls how many plots per row
        self.__fix_colour = 0
        self.__colour_num = 1

    def plot(self, candle_series: dict[str, pd.DataFrame], column_name, x_label, y_label, title):
        num_rows = len(candle_series) // self.__num_columns + (len(candle_series) % self.__num_columns > 0)
        fig, axes = plt.subplots(num_rows, self.__num_columns, figsize=(15 * self.__num_columns, 8 * num_rows),
                                 squeeze=False)
        axes = axes.flatten()

        for index, (ticker, series) in enumerate(candle_series.items()):
            self.__add_series(axis=axes[index], y_date=list(series[column_name].values),
                              x_data=list(series[column_name].index),
                              title=title, x_label=x_label, y_label=y_label, label=ticker)

        plt.tight_layout()
        plt.show()

    def __add_series(self, axis, x_data, y_date, label, title, x_label, y_label):
        axis.plot(x_data, y_date, label=label, color=f"C{self.__colour_num}")
        axis.set_title(title)
        axis.set_xlabel(x_label)
        axis.set_ylabel(y_label)
        axis.legend()

        self.__colour_num += 1
