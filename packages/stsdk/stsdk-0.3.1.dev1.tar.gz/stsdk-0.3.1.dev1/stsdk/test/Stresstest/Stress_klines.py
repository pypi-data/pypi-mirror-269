import random

from locust import HttpUser, between, task


class APITestUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://43.207.236.155:5001"

    @task
    def load_test(self):
        instruments = [
            "BTC", "ETH", "XRP", "BNB", "SOL", "DOGE", "MATIC", "ADA", "SHIB",
            "ETC", "LTC", "AVAX", "OP", "FTM", "LINK", "FIL", "GALA", "CHZ",
            "TRX", "DOT", "APE", "NEAR", "ATOM", "GMT", "EUR", "CFX", "SAND",
            "LUNA", "LDO", "DYDX"
        ]
        intervals = ['1m', '5m', '15m', '30m', '1h']
        limits = [1, 50, 100, 500, 2000]

        instrument = random.choice(instruments)
        interval = random.choice(intervals)
        limit = random.choice(limits)

        params = {
            "instrument_id": f"EXCHANGE_BINANCE.{instrument}-USDT.SECURITY_TYPE_SPOT.UNSPECIFIED.UNSPECIFIED.UNSPECIFIED",
            "interval": interval,
            "limit": limit
        }
        self.client.get("/v1/klines/instrument", params=params)
