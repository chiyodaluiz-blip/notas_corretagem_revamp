from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:

    asset: str
    side: str
    quantity: float
    price: float


@dataclass
class Taxes:

    liquidacao: float = 0
    registro: float = 0
    emolumentos: float = 0
    operacional: float = 0
    impostos: float = 0
    total: float = 0


@dataclass
class BrokerageNote:

    date: datetime
    trades: list
    taxes: Taxes
    liquido_para: float | None = None
