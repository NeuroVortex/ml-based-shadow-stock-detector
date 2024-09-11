from typing import NamedTuple, Tuple


class SamplingConf(NamedTuple):
    sim_fluctuation_range: Tuple[float, float] = (0.001, 0.01)
    sim_volatility_range: Tuple[float, float] = (-0.005, -0.01)
    sim_return_adjustment: float = 0.03
    dis_sim_volatility_range: Tuple[float, float] = (0.001, 0.5)
    dis_sim_volume_range: Tuple[float, float] = (1000, 10000)
    dis_sim_fluctuation_range: Tuple[float, float] = (0.001, 0.5)
    dis_sim_price_range: Tuple[float, float] = (200, 1000000)
    return_window: float = 0.1
