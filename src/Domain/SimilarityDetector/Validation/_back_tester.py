import matplotlib.pyplot as plt


class BackTester:

    def __init__(self, tolerance: float = 0.05):
        self.__tolerance = tolerance

    def back_test(self, candle_1, candle_2):
        # Assuming df1 and df2 are your DataFrames for Stock 1 and Stock 2
        candle_1['Returns'] = candle_1['Close'].pct_change()
        candle_2['Returns'] = candle_2['Close'].pct_change()

        # Calculate Cumulative Returns
        candle_1['Cumulative Returns'] = (1 + candle_1['Returns']).cumprod() - 1
        candle_2['Cumulative Returns'] = (1 + candle_2['Returns']).cumprod() - 1

        # Compare Cumulative Returns
        final_return_stock1 = candle_1['Cumulative Returns'].iloc[-1]
        final_return_stock2 = candle_2['Cumulative Returns'].iloc[-1]

        # Apply a Penalty for Return Discrepancy
        penalty_rate = 0.1  # Define how severe the penalty should be
        penalty = penalty_rate * abs(final_return_stock1 - final_return_stock2)

        adjusted_return_stock1 = final_return_stock1 - penalty
        adjusted_return_stock2 = final_return_stock2 - penalty

        print(f"Adjusted Final Return Stock 1: {adjusted_return_stock1}")
        print(f"Adjusted Final Return Stock 2: {adjusted_return_stock2}")

        # Evaluate the Result
        if abs(adjusted_return_stock1 - adjusted_return_stock2) < self.__tolerance:
            print("Stocks provide similar returns within the specified tolerance.")
            return True

        else:
            print("Stocks do not provide similar returns.")
            return False

    @classmethod
    def visualize(cls, candle_1, candle_2):
        plt.figure(figsize=(14, 7))
        plt.plot(candle_1['Cumulative Returns'], label='Stock 1 Cumulative Returns')
        plt.plot(candle_2['Cumulative Returns'], label='Stock 2 Cumulative Returns')
        plt.title('Comparison of Cumulative Returns')
        plt.legend()
        plt.show()
