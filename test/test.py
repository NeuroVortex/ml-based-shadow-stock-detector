from src.detect import detect_shadow_stocks


if __name__ == "__main__":
    file_path = "./data/sample_datasets.json"
    model_path = "./model/"
    sample_ticker = 'IRTKROBA0001'
    model_name = 'shadow_stocks'

    similar_stocks = detect_shadow_stocks(goal_ticker=sample_ticker,
                                          file_path=file_path,
                                          model_path=model_path,
                                          model_name=model_name)

    print(f"Similar stocks with {sample_ticker} are: {similar_stocks}")
