
# ML-Based Stock Matcher

## Overview

**Ml-StockMatcher** is a project that leverages machine learning techniques to identify and analyze similar stocks based on their historical price patterns. This repository implements a solution using the Fast Dynamic Time Warping (Fast DTW) algorithm and Random Forest classifier, combined with data augmentation, to generate and discover similar stock patterns.

## Features

- **Fast DTW**: Efficiently measures the similarity between stock time series, enabling the comparison of different stocks' historical price movements.
- **Random Forest**: Utilized for classification and pattern recognition, helping to identify which stocks exhibit similar behaviors.
- **Data Augmentation**: Enhances the model's robustness by generating synthetic data to improve pattern recognition accuracy.

## Installation

Clone the repository:

```bash
git clone https://github.com/NeuroVortex/ml-stock-matcher.git
```

Navigate to the project directory:

```bash
cd MlBasedStockMatcher
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. **Data Preparation**: Ensure your stock data is formatted correctly. The model expects time-series data with consistent timestamps across all stocks.
  
2. **Run the Model**:
   
   - To find similar stocks, run the main script:
   
     ```bash
     python find_similar_stocks.py
     ```

3. **Results**:
   - The output will include a list of stocks that are most similar to the target stock based on historical price patterns.

## Data Augmentation

Data augmentation is used to create additional synthetic stock patterns. This improves the generalization of the Random Forest model by exposing it to a wider variety of stock behaviors.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find a bug or have a feature request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
