import requests

from stsdk.test.ordertest.logs import logger


class placeOrder():
    def get_placeOrder(payload):
        url = "http://47.91.17.20:4000/order/new"
        # payload = {
        #     "strategy_id": "1", 
        #     "symbol": "BTC-USDT", 
        #     "quantity": "0.0005",
        #     "price": "20000",  #价格不填写的情况下会是市价单
        #     "settle_ccy": "USDT", 
        #     "expiry_date": "",  #过期时间
        #     "security_type": 1,  #SECURITY_TYPE_SPOT正确 2:SECURITY_TYPE_PERP
        #     "position_side": 3,  #POSITION_SIDE_NOTBOTH
        #     "order_type": 2,  #ORDER_TYPE_LIMIT
        #     "exchange": 1,   #返回EXCHANGE_BINANCE正确
        #     "order_direction": 1,  #ORDER_DIRECTION_BUY
        #     "time_in_force": 1,  #TIME_IN_FORCE_GTC
        #     "leverage": 0,  #杠杆倍数
        #     "contract_type": 0, #CONTRACT_TYPE_LINEAR
        #     "account_id": "aris_test",
        #     "instrument_id": "EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_SPOT.UNSPECIFIED.UNSPECIFIED.UNSPECIFIED"
        # }
        response = requests.post(url, json=payload)
        # print(response.text)
        # logger.info("创建订单返回结果：%s"% response.text)
        if response is not None:
            return response

# if __name__ == '__main__':
#     placeOrder()