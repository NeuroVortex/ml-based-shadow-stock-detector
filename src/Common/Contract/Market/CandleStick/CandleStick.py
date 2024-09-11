from typing import NamedTuple
from decimal import Decimal


class CandleStick(NamedTuple):
    Open: Decimal
    Low: Decimal
    High: Decimal
    Close: Decimal
    Volume: Decimal
    OpeningTime: str
