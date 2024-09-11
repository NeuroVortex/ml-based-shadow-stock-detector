from matplotlib import pyplot as plt
from sklearn.decomposition import PCA


class PCAFeatureReducer:

    @classmethod
    def reduce_feature(cls, data, n_components=3):
        pca = PCA(n_components=n_components)
        reduced_features = pca.fit_transform(data)
        return reduced_features

    @classmethod
    def plot_pca_and_close(cls, data, reduced_features):
        plt.figure(figsize=(14, 10))

        # Plotting the Close Price
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')

        # Plotting the PCA reduced features
        for i in range(reduced_features.shape[1]):
            plt.plot(data.index, reduced_features[:, i], label=f'PCA Component {i + 1}')

        plt.title('Close Price with PCA-Reduced Features')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.show()
