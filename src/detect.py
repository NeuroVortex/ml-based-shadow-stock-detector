from src.Application.Market.CandleDataReader import CandleDataReader
from src.Application.Market.MarketCandleDataRepository import MarketCandleDataRepository
from src.Domain.SimilarityDetector.SimilarityDetector import SimilarityDetector


def detect_shadow_stocks(goal_ticker: str, file_path: str, model_path: str, model_name: str):
    data_repo = MarketCandleDataRepository()
    candle_data_reader = CandleDataReader(data_repo)
    candle_data_reader.read_from_file(file_path)
    similarity_detector = SimilarityDetector(file_path=file_path,
                                             model_name=model_name,
                                             model_path=model_path,
                                             data_repo=data_repo)

    similarity_detector.start()

    goal_candle = data_repo.get_by_ticker(goal_ticker)
    similar_stocks = similarity_detector.calculate(goal_ticker, goal_candle)

    return similar_stocks

