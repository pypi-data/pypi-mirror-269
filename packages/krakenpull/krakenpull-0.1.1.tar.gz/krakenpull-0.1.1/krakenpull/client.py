import abc
import base64
import hashlib
import hmac
import requests
import time
import urllib.parse
from requests import Response

from krakenpull.models import (
    CurrencyPair,
    ClosedTransaction,
    Currency,
    TickerInfo,
    JSON,
)

BASE_URL = "https://api.kraken.com/0"


class AbstractKraken(abc.ABC):
    @abc.abstractmethod
    def __init__(self, key: str, private_key: str):
        self.private_url = f"{BASE_URL}/private"
        self.public_url = f"{BASE_URL}/public"
        self.private_endpoint = "/0/private"
        self.public_endpoint = "/0/public"

    def get_order_book(self, currency_pair: CurrencyPair) -> JSON:
        url, _ = self._return_url_endpoint(endpoint="Depth")
        res = requests.post(f"{url}?pair={''.join(c.value for c in currency_pair)}")
        self._get_result(res, op="get order book")
        return list(res.json()["result"].values())[0]

    @abc.abstractmethod
    def get_account_balance(self) -> dict[Currency, float]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_closed_orders(self, trades: bool = False) -> list[ClosedTransaction]:
        raise NotImplementedError

    def get_ticker_info(
        self, currency_pairs: list[CurrencyPair] | CurrencyPair
    ) -> list[TickerInfo]:
        url, _ = self._return_url_endpoint(endpoint="Ticker")
        pairs = currency_pairs if isinstance(currency_pairs, list) else [currency_pairs]
        stringed_pairs = ["".join(c.value for c in pair) for pair in pairs]
        res = requests.post(f"{url}?pair={','.join(stringed_pairs)}")
        result = self._get_result(res, op="get ticker info")
        return [
            TickerInfo.model_validate(
                {
                    "pair": pair_id,
                    "price": data["a"][0],
                    "low": data["l"][0],
                    "high": data["h"][0],
                },
            )
            for pair_id, data in result.items()
        ]

    def _return_url_endpoint(
        self, endpoint: str, private: bool = False
    ) -> tuple[str, str]:
        if private:
            return (
                f"{self.private_url}/{endpoint}",
                f"{self.private_endpoint}/{endpoint}",
            )
        else:
            return f"{self.public_url}/{endpoint}", f"{self.public_endpoint}/{endpoint}"

    def _get_server_time_unix(self) -> int:
        res = requests.get(f"{BASE_URL}/public/Time")
        result = self._get_result(res, op="get server time")
        return result["unixtime"]

    def _get_result(self, res: Response, op: str | None = None) -> JSON:
        json_res = res.json()
        error = json_res.get("error") or None
        if res.status_code != 200 or error:
            raise Exception(
                "Kraken api call failed"
                + (f" ({op})" if op else "")
                + f": {error[0] if isinstance(error, list) else error}"
            )
        return json_res["result"]


class FakeKraken(AbstractKraken):
    def __init__(self, transactions: list[ClosedTransaction] | None):
        super().__init__("key", "private_key")
        self._transactions = transactions or []

    def get_order_book(self, currency_pair: CurrencyPair) -> JSON:
        return {
            "asks": [
                ["69854.10000", "17.384", 1711832989],
                ["69854.20000", "0.189", 1711832983],
                ["69863.60000", "0.118", 1711832989],
                ["69863.70000", "0.042", 1711832983],
                ["69866.90000", "17.247", 1711832988],
            ],
            "bids": [
                ["69854.00000", "0.015", 1711832988],
                ["69850.00000", "0.005", 1711832881],
                ["69844.60000", "0.001", 1711832857],
                ["69838.00000", "0.010", 1711832884],
                ["69836.50000", "0.003", 1711832881],
            ],
        }

    def get_account_balance(self) -> dict[Currency, float]:
        return {
            Currency.FLR: 1062.2314,
            Currency.SGB: 1062.2666259600,
            Currency.USDT: 10474.11937100,
            Currency.BTC: 4.2375553847,
            Currency.XMR: 1.600,
        }

    def get_closed_orders(self, trades: bool = False) -> list[ClosedTransaction]:
        return self._transactions

    def _get_server_time_unix(self) -> int:
        return int(time.time() * 1000)


# FIXME
# get_env_variables().KRAKEN_API_KEY


class Kraken(AbstractKraken):
    def __init__(self, key: str, private_key: str):
        super().__init__(key, private_key)
        self.api_key = key
        self.private_key = private_key

    def get_order_book(self, currency_pair: CurrencyPair) -> JSON:
        url, _ = self._return_url_endpoint(endpoint="Depth")
        res = requests.post(f"{url}?pair={''.join(c.value for c in currency_pair)}")
        result = self._get_result(res, op="get order book")
        return list(result.values())[0]

    def get_account_balance(self) -> dict[Currency, float]:
        url, endpoint = self._return_url_endpoint(endpoint="Balance", private=True)
        nonce = self._get_server_time_unix()
        headers = self._headers(endpoint, nonce)
        res = requests.post(
            url,
            headers=headers,
            data={"nonce": nonce},
        )
        result = self._get_result(res, op="get account balance")
        return {
            Currency(k.replace("XX", "X")): float(v)
            for k, v in result.items()
            if float(v) > 1e-5
        }

    def get_closed_orders(self, trades: bool = False) -> list[ClosedTransaction]:
        url, endpoint = self._return_url_endpoint(endpoint="ClosedOrders", private=True)
        nonce = self._get_server_time_unix()
        data = {
            "nonce": nonce,
            "trades": trades,
        }
        headers = self._headers(endpoint, nonce, data)
        res = requests.post(url, headers=headers, data=data)
        result = self._get_result(res, op="get closed orders")

        closed_positions = result["closed"]

        return [
            ClosedTransaction.model_validate(
                v
                | v["descr"]
                | {
                    "id": k,
                    "price": v["price"],
                    "open_datetime": v["opentm"],
                    "close_datetime": v["closetm"],
                }
            )
            for k, v in closed_positions.items()
            if v["status"] == "closed"
        ]

    def _headers(self, urlpath: str, nonce: int, data: JSON | None = None) -> JSON:
        data = data if data else {}
        postdata = urllib.parse.urlencode({"nonce": nonce, **data})
        encoded = (str(nonce) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.private_key), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return {"API-Key": self.api_key, "API-Sign": sigdigest.decode()}


def get_kraken_client(
    key: str | None,
    private_key: str | None,
    emulator: bool = False,
    transactions: list[ClosedTransaction] | None = None,
) -> AbstractKraken:
    return (
        Kraken(key, private_key)
        if not emulator and key and private_key
        else FakeKraken(transactions)
    )
