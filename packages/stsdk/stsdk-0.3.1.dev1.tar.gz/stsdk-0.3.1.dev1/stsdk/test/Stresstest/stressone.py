import random

from locust import HttpUser, between, task


class APITestUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://43.207.236.155:5001"

    @task
    def load_test(self):
        instruments = "BTC"        
        intervals = '30m'
        limits = 100

        # instrument = random.choice(instruments)
        # interval = random.choice(intervals)
        # limit = random.choice(limits)

        params = {
            "instrument_id": f"EXCHANGE_BINANCE.{instruments}-USDT.SECURITY_TYPE_SPOT.UNSPECIFIED.UNSPECIFIED.UNSPECIFIED",
            "interval": intervals,
            "limit": limits
        }
        self.client.get("/v1/klines/instrument", params=params)
