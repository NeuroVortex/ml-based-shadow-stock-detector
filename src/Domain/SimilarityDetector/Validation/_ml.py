import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


class MLBasedValidation:
    def __init__(self, goal_candle: pd.DataFrame):
        self.__goal_candle = goal_candle

    def train(self):
        data, labels = self.__generate_dataset(num_samples=1000)

        # Extract features and labels
        X, y = self.__extract_features_and_labels(data, labels)

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the Random Forest classifier
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Predict on the test set
        y_pred = model.predict(X_test)

        # Evaluate the model
        print("Classification Report:\n", classification_report(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    @classmethod
    def __generate_similar_series(cls, base_series, variation=0.01):
        similar_series = base_series.copy()
        similar_series['Close'] = similar_series['Close'] + np.random.normal(0, variation, len(similar_series))
        similar_series['Open'] = similar_series['Open'] + np.random.normal(0, variation, len(similar_series))
        similar_series['High'] = similar_series['High'] + np.random.normal(0, variation, len(similar_series))
        similar_series['Low'] = similar_series['Low'] + np.random.normal(0, variation, len(similar_series))
        return similar_series

    @classmethod
    def __generate_non_similar_series(cls, length=100, start_price=200):
        np.random.seed()
        dates = pd.date_range('2021-01-01', periods=length)
        prices = np.cumsum(np.random.normal(0, 5, length)) + start_price  # Different mean and variance
        high = prices + np.random.normal(5, 1, length)
        low = prices - np.random.normal(5, 1, length)
        open = prices + np.random.normal(0, 1, length)
        close = prices + np.random.normal(0, 1, length)
        volume = np.random.randint(100, 1000, length)
        data = pd.DataFrame({'Open': open, 'High': high, 'Low': low, 'Close': close, 'Volume': volume}, index=dates)
        return data

    def __generate_dataset(self, num_samples=1000, length=100, start_price=100):
        data = []
        labels = []
        for _ in range(num_samples):

            # Generate a similar series
            similar_series = self.__generate_similar_series(self.__goal_candle)
            data.append((self.__goal_candle, similar_series))
            labels.append(1)  # Label as similar

            # Generate a non-similar series
            non_similar_series = self.__generate_non_similar_series(length=length, start_price=start_price * 2)
            data.append((self.__goal_candle, non_similar_series))
            labels.append(0)  # Label as non-similar

        return data, labels

    @classmethod
    def __extract_features_and_labels(cls, data, labels):
        features = []
        for base_series, compare_series in data:
            base_returns = base_series['Close'].pct_change().dropna()
            compare_returns = compare_series['Close'].pct_change().dropna()
            distance, _ = fastdtw(base_returns, compare_returns, dist=euclidean)
            features.append([distance])
        return np.array(features), np.array(labels)

