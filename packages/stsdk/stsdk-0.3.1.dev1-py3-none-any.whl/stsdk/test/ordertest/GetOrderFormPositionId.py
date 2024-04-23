import requests

from stsdk.test.ordertest.logs import logger


class GetOrderFromPositionId:
    def generate_position_id(strategy_id, account_id, inst_id):
        return "{}.{}.{}".format(strategy_id, account_id, inst_id)
    def get_PositionId(strategy_id, account_id, inst_id):
        url = "http://47.91.17.20:6002/position/position_id"
        position_id=GetOrderFromPositionId.generate_position_id(strategy_id, account_id, inst_id)
        params={
            "position_id": position_id
        }
        response = requests.get(url, params=params).json()
        logger.info(f"获取position_id返回结果: {response}")
        if response is not None:
            return response