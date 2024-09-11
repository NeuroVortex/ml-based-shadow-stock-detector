import mplfinance as mpf
import pandas as pd


class CandlePlotter:

    @classmethod
    def plot(cls, candle: pd.DataFrame):
        mc = mpf.make_marketcolors(up='g', down='r', wick='inherit', edge='inherit', volume='in')
        s = mpf.make_mpf_style(marketcolors=mc)

        mpf.plot(candle, type='candle', volume=True, style=s, title='Candlestick Chart', ylabel='Price',
                 ylabel_lower='Volume')
