from typing import Any

import json

import datetime as dt
from enum import Enum

from pydantic import BaseModel, field_validator


JSON = dict[str, Any]


class NonfiatCurrency(Enum):
    btc = "XBT"
    ltc = "LTC"


class Currency(Enum):
    USD = "USD"
    BTC = "XBT"
    LTC = "LTC"
    AAVE = "AAVE"
    ADA = "ADA"
    ATOM = "ATOM"
    BCH = "BCH"
    BSV = "BSV"
    DOT = "DOT"
    EOS = "EOS"
    ETHW = "ETHW"
    FLR = "FLR"
    LINK = "LINK"
    SGB = "SGB"
    USDT = "USDT"
    ETH = "ETH"
    XLM = "XLM"
    XMR = "XMR"
    XRP = "XRP"
    ZUSD = "ZUSD"


CurrencyPair = tuple[Currency, Currency]


class TransactionType(Enum):
    buy = "buy"
    sell = "sell"


# FIXME
# OrderType = Literal['limit', 'market', 'stop-loss', 'take-profit']


class OrderType(Enum):
    limit = "limit"
    market = "market"
    stop_loss = "stop-loss"
    take_profit = "take-profit"


class BaseTickerInfo(BaseModel):
    pair: CurrencyPair
    price: float

    @field_validator("pair", mode="before")
    @classmethod
    def parse_pair(cls, v: str) -> tuple[Currency, Currency]:
        if v == "USDZUSD" or v == "USDTZUSD":
            return Currency.USDT, Currency.USD

        try:
            currency1 = Currency(v[:3])
        except ValueError:
            try:
                currency1 = Currency(v[:4].replace("XX", "X"))
            except ValueError:
                raise Exception("Currency 1 could not be parsed")

        try:
            currency2 = Currency(v[3:])
        except ValueError:
            try:
                currency2 = Currency(v[4:])
            except ValueError:
                raise Exception("Currency 2 could not be parsed")

        return currency1, currency2

    @property
    def currency1(self) -> Currency:
        return self.pair[0]

    @property
    def currency2(self) -> Currency:
        return self.pair[1]

    @property
    def currency_pair_id(self) -> str:
        return "".join(c.value for c in self.pair)


class ClosedTransaction(BaseTickerInfo):
    id: str
    type: TransactionType
    ordertype: OrderType
    vol: float
    cost: float
    leverage: str
    fee: float
    order: str
    open_datetime: dt.datetime
    close_datetime: dt.datetime


class TickerInfo(BaseTickerInfo):
    low: float
    high: float


class Asset(BaseModel):
    currency: Currency
    value: float
    amount: float

    def jsonable_dict(self) -> JSON:
        return json.loads(self.model_dump_json())
