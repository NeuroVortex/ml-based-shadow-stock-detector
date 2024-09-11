import pandas as pd
from matplotlib import pyplot as plt
from ta import trend, momentum, volatility, volume, others


class TechnicalFeatures:

    @classmethod
    def add_ta_features(cls, data):
        data['trend_ichimoku_conv'] = trend.ichimoku_a(data['High'], data['Low'])
        data['trend_ema_slow'] = trend.ema_indicator(data['Close'], 50)
        data['momentum_kama'] = momentum.kama(data['Close'])
        data['trend_psar_up'] = trend.psar_up(data['High'], data['Low'], data['Close'])
        data['volume_vwap'] = volume.VolumeWeightedAveragePrice(data['High'], data['Low'], data['Close'], data['Volume']).volume_weighted_average_price()
        data['trend_ichimoku_a'] = trend.ichimoku_a(data['High'], data['Low'])
        data['volatility_kcl'] = volatility.KeltnerChannel(data['High'], data['Low'], data['Close']).keltner_channel_lband()
        data['trend_ichimoku_b'] = trend.ichimoku_b(data['High'], data['Low'])
        data['trend_ichimoku_base'] = trend.ichimoku_base_line(data['High'], data['Low'])
        data['trend_sma_fast'] = trend.sma_indicator(data['Close'], 20)
        data['volatility_dcm'] = volatility.DonchianChannel(data['High'],
                                                            data['Low'],
                                                            data['Close']).donchian_channel_mband()
        data['volatility_bbl'] = volatility.BollingerBands(data['Close']).bollinger_lband()
        data['volatility_bbm'] = volatility.BollingerBands(data['Close']).bollinger_mavg()
        data['volatility_kcc'] = volatility.KeltnerChannel(data['High'],
                                                           data['Low'],
                                                           data['Close']).keltner_channel_mband()
        data['volatility_kch'] = volatility.KeltnerChannel(data['High'],
                                                           data['Low'],
                                                           data['Close']).keltner_channel_hband()
        data['trend_sma_slow'] = trend.sma_indicator(data['Close'],
                                                     200)
        data['trend_ema_fast'] = trend.ema_indicator(data['Close'],
                                                     20)
        data['volatility_dch'] = volatility.DonchianChannel(data['High'],
                                                            data['Low'],
                                                            data['Close']).donchian_channel_hband()
        data['others_cr'] = others.cumulative_return(data['Close'])
        data['Adj Close'] = data['Close']
        return data

    @classmethod
    def get_price_change(cls, candlesticks) -> pd.DataFrame:
        return candlesticks['Close'].pct_change().dropna()

    @classmethod
    def plot_indicators(cls, data):
        # Adding technical indicators
        data = cls.add_ta_features(data)

        # Plotting
        plt.figure(figsize=(14, 10))
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')
        plt.plot(data.index, data['trend_ema_slow'], label='EMA 50', linestyle='--', color='orange')
        plt.plot(data.index, data['trend_sma_fast'], label='SMA 20', linestyle='--', color='green')
        plt.plot(data.index, data['trend_sma_slow'], label='SMA 200', linestyle='--', color='red')
        plt.plot(data.index, data['momentum_kama'], label='KAMA', linestyle='--', color='purple')
        plt.plot(data.index, data['volume_vwap'], label='VWAP', linestyle='--', color='brown')
        plt.plot(data.index, data['volatility_bbm'], label='Bollinger Bands Middle', linestyle='--', color='magenta')
        plt.plot(data.index, data['volatility_bbl'], label='Bollinger Bands Lower', linestyle='--', color='cyan')
        plt.plot(data.index, data['volatility_kcc'], label='Keltner Channel Middle', linestyle='--', color='gray')
        plt.plot(data.index, data['trend_ichimoku_base'], label='Ichimoku Base Line', linestyle='--', color='black')

        plt.title('Close Price with Technical Indicators')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
