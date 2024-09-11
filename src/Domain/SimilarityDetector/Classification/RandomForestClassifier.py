import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, classification_report,
                             confusion_matrix)
import joblib

from src.Common.File.FileChecking import file_exists


class Classifier:
    def __init__(self, model_name: str):
        self.__model_name = model_name
        self.__estimator = None
        self.__data_sets = {
            'X_train': None,
            'Y_train': None,
            'X_test': None,
            'Y_test': None
        }

    def train(self, data_sets: pd.DataFrame):
        x_series = data_sets[['series_distance', 'ta_distance', 'return_distance']]
        y_series = data_sets['result']

        x_train_series, x_test_series, y_train_series, y_test_series = train_test_split(x_series, y_series,
                                                                                        test_size=0.3,
                                                                                        random_state=42)
        self.__data_sets.update({
            'X_train': x_train_series,
            'Y_train': y_train_series,
            'X_test': x_test_series,
            'Y_test': y_test_series
        })
        self.__estimator = RandomForestClassifier(n_estimators=100, random_state=42)
        # self.__estimator = self.__cross_validation(x_train_series, y_train_series)
        self.__estimator.fit(x_train_series, y_train_series)

    def validate(self):
        x_test_series, y_test_series = self.__data_sets.get('X_test'), self.__data_sets.get('Y_test')
        y_pred = self.__estimator.predict(x_test_series)

        # Evaluate the model
        accuracy = accuracy_score(y_test_series, y_pred)
        precision = precision_score(y_test_series, y_pred)
        recall = recall_score(y_test_series, y_pred)
        f1 = f1_score(y_test_series, y_pred)
        conf_matrix = confusion_matrix(y_test_series, y_pred)
        class_report = classification_report(y_test_series, y_pred)

        # Print the results
        print(f'Accuracy: {accuracy}')
        print(f'Precision: {precision}')
        print(f'Recall: {recall}')
        print(f'F1 Score: {f1}')
        print('Confusion Matrix:')
        print(conf_matrix)
        print('Classification Report:')
        print(class_report)

    def is_similar(self, feature: pd.DataFrame):
        y_pred = self.__estimator.predict(feature)
        return bool(y_pred)

    def save_model(self, path):
        joblib_file = path + f"{self.__model_name}.pkl"
        joblib.dump(self.__estimator, joblib_file)
        print(f"Model saved to {joblib_file}")
        return self.__estimator

    def load_model(self, file_path):
        joblib_file = f"{self.__model_name}.pkl"
        if file_exists(file_path, joblib_file):
            self.__estimator = joblib.load(file_path+joblib_file)
            return True

        else:
            return False

    @classmethod
    def __cross_validation(cls, x_train_series, y_train_series):
        # Define the parameter grid for GridSearchCV
        param_grid = {
            'n_estimators': [100, 200, 500, 1000],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }

        # Initialize the Random Forest Classifier
        classifier = RandomForestClassifier(random_state=42)

        # Initialize GridSearchCV
        grid_search = GridSearchCV(estimator=classifier, param_grid=param_grid,
                                   cv=5, n_jobs=-1, verbose=2, scoring='accuracy')

        # Fit GridSearchCV
        grid_search.fit(x_train_series, y_train_series)

        # Print the best parameters and the best score
        print(f'Best Parameters: {grid_search.best_params_}')
        print(f'Best Cross-Validation Accuracy: {grid_search.best_score_}')

        return grid_search.best_estimator_

    @property
    def model(self):
        return self.__estimator

