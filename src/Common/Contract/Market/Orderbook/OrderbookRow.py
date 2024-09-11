from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OrderbookRow:
    price: Decimal
    qty: Decimal

    def to_dict(self):
        return {
            "price": str(self.price),
            "qty": str(self.qty)
        }
