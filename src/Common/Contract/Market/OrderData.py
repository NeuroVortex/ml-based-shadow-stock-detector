from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class OrderData:
    price: Decimal
    qty: Decimal

    def toDict(self):
        return {
            "price": self.price,
            "qty": self.qty
        }
