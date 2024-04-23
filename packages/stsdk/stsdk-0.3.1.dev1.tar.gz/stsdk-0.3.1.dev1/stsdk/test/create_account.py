import requests

from loguru import logger

create_account_end_points = "http://{host}:6002/account/new".format(host="43.207.106.154")
get_account_end_points = "http://{host}:6002/account/account_id".format(host="43.207.106.154")

post_strategy_end_points = "http://{host}:6002/strategy/new".format(host="43.207.106.154")
get_strategy_end_points = "http://{host}:6002/strategy/strategy_id".format(host="43.207.106.154")

if __name__ == "__main__":
    account_info = {
        "account_id": "",
        "exchange": 1,
        "security_type": [],
        "contract_type": [],
        "balance": "0",
        "multi_asset_margin": False,
        "api_key": "",
        "api_secret": "",
        "ip_white_list": []
    }

    r = requests.post(url=create_account_end_points, data=account_info)
    logger.info(r.text)
