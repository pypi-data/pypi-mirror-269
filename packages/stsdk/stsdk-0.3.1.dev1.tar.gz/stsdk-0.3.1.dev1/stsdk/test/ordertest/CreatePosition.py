import requests

from stsdk.test.ordertest.logs import logger


class CreatePosition():
    def get_CreatePosition():
        url = "http://47.91.17.20:6002/position/new"
        payload = {
            "account_id": "aris_test",
            "strategy_id": "1",
            "instrument_id": "EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_SPOT.UNSPECIFIED.UNSPECIFIED.UNSPECIFIED",
            "is_both": False,
            "long_position": {
                "filled_limit": "9999999",
                "filled_position": "0",
                "outstanding_limit": "999999",
                "outstanding_position": "0"
            },
            "short_position": {
                "filled_limit": "9999999",
                "filled_position": "0",
                "outstanding_limit": "999999",
                "outstanding_position": "0"
            }
        }

        response = requests.post(url, json=payload)
        # print(response.text)
        logger.info("创建策略返回：%s" %response.text)
        if response is not None:
            return response


# if __name__ == '__main__':
#     CreatePosition()