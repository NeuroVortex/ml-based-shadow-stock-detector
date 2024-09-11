import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class MLBasedValidation:

    def __init__(self):
        self.__random_forest_desired_accuracy = 0.5

    def validate(self, candlestick_df_1: pd.DataFrame, candlestick_df_2: pd.DataFrame):
        extracted_features_1 = self.__extract_feature(candlestick_df_1)
        extracted_features_2 = self.__extract_feature(candlestick_df_2)

        labeled_features, labels = self.__labeling(extracted_features_1, extracted_features_2)

        # Assuming features and labels are prepared
        x_train, x_test, y_train, y_test = train_test_split(labeled_features,
                                                            labels,
                                                            test_size=0.2,
                                                            random_state=42)
        self.__random_forest(x_train, y_train, x_test, y_test)

    @classmethod
    def __calculate_ml_indicators(cls, y_test, y_probs):
        precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)
        # Compute F1 scores at each threshold

        f1_scores = 2 * (precisions * recalls) / (precisions + recalls)

        # Find the threshold that maximizes the F1 score
        optimal_idx = np.argmax(f1_scores)
        optimal_threshold = thresholds[optimal_idx]

        # Make predictions using the optimal threshold
        y_pred_optimal = int(y_probs >= optimal_threshold)

        # Evaluate the model with the optimal threshold
        print(f"Optimal Threshold: {optimal_threshold}")
        print(f"Precision at optimal threshold: {precisions(y_test, y_pred_optimal)}")
        print(f"Recall at optimal threshold: {recalls(y_test, y_pred_optimal)}")
        print(f"F1 Score at optimal threshold: {f1_scores[optimal_idx]}")
        print("\nClassification Report:\n", classification_report(y_test, y_pred_optimal))

    @classmethod
    def __extract_feature(cls, candle):
        features = pd.DataFrame()
        features['Open'] = candle['Open']
        features['High'] = candle['High']
        features['Low'] = candle['Low']
        features['Close'] = candle['Close']
        features['Volume'] = candle['Volume']
        features['Ma5'] = candle['Close'].rolling(window=5).mean()
        features['Ma10'] = candle['Close'].rolling(window=10).mean()
        features['Ma20'] = candle['Close'].rolling(window=20).mean()
        features['Std5'] = candle['Close'].rolling(window=5).std()
        features['Std10'] = candle['Close'].rolling(window=10).std()
        features['Std20'] = candle['Close'].rolling(window=20).std()
        features = features.dropna()
        return features

    @classmethod
    def __labeling(cls, features_1: pd.DataFrame, features_2: pd.DataFrame):
        labels = np.array([1, 0])  # Example labels, you need a labeled dataset
        features = np.vstack((features_1.values, features_2.values))
        return features, labels

    def __random_forest(self, x_train, y_train, x_test, y_test):
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(x_train, y_train)

        y_pred = model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        self.__calculate_ml_indicators(y_test, y_pred)
        print(f'Random Forest Validation Accuracy: {accuracy}')
        print('Random Forest Validation Report ', classification_report(y_test, y_pred))

    @classmethod
    def __kmeans_classification(cls, features):
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        kmeans = KMeans(n_clusters=2, random_state=42)
        clusters = kmeans.fit_predict(features_scaled)

        print(f"Cluster labels: {clusters}")
        score = silhouette_score(features_scaled, clusters)
        print(f"Clustering Silhouette Score: {score}")
