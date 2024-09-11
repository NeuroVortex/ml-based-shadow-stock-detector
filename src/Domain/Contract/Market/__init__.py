from typing import NamedTuple


class Market(NamedTuple):
    base_asset: str
    quote_asset: str = 'EUR'
