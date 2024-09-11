from sklearn.impute import SimpleImputer


class Impute:
    def __init__(self):
        self.__impute_strategy = 'mean'

    def fill_missing(self, data):
        # Impute missing values
        impute = SimpleImputer(strategy=self.__impute_strategy)
        imputed_ta_features = impute.fit_transform(data)
        return imputed_ta_features
