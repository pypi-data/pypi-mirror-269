import json

import pytest

from stsdk.test.ordertest.initialization import initialization
from stsdk.test.ordertest.logs import logger
# from stsdk.test.ordertest.pmsinit import pmsinit
from stsdk.test.ordertest.placeOrder import placeOrder

'''
创建订单然后查询订单，再取消订单，取消后查看订单不存在
'''
def test_order_closed_loop():
    # 操作下单，定义入参参数并进行校验
    orderinfo = {
        "strategy_id": "1", 
        "symbol": "BTC-USDT", 
        "quantity": "0.0005",
        "price": "20000",  #价格不填写的情况下会是市价单
        "settle_ccy": "USDT", 
        "expiry_date": "",  #过期时间
        "security_type": 1,  #SECURITY_TYPE_SPOT正确 2:SECURITY_TYPE_PERP
        "position_side": 3,  #POSITION_SIDE_NOTBOTH
        "order_type": 2,  #ORDER_TYPE_LIMIT 1:ORDER_TYPE_MARKET
        "exchange": 1,   #返回EXCHANGE_BINANCE正确
        "order_direction": 1,  #ORDER_DIRECTION_BUY
        "time_in_force": 1,  #TIME_IN_FORCE_GTC
        "leverage": 0,  #杠杆倍数
        "contract_type": 0, #CONTRACT_TYPE_LINEAR
        "account_id": "aris_test",
        "instrument_id": "EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_SPOT.UNSPECIFIED.UNSPECIFIED.UNSPECIFIED"
    }
    #下单操作
    request_result = placeOrder.get_placeOrder(orderinfo).json()
    # print(type(request_result))
    # 断言下单应该要返回的结果是预期设计的结果
    assert request_result["strategy_id"] == orderinfo["strategy_id"]
    assert request_result["account_id"] == orderinfo["account_id"]
    assert request_result["instrument_id"] == orderinfo["instrument_id"]
    assert request_result["symbol"] == orderinfo["symbol"]
    assert request_result["exchange"] == "EXCHANGE_BINANCE"
    assert request_result["security_type"] == "SECURITY_TYPE_SPOT"
    assert request_result["order_type"] == "ORDER_TYPE_LIMIT"
    assert request_result["origin_price"] == orderinfo["price"] 
    assert request_result["origin_quantity"] == orderinfo["quantity"]
    assert request_result["order_direction"] == "ORDER_DIRECTION_BUY"
    assert request_result["position_side"] == "POSITION_SIDE_NOTBOTH"
    assert request_result["order_status"] == "ORDER_STATUS_NEW"
    assert request_result["time_in_force"] == "TIME_IN_FORCE_GTC"
    logger.info("下单返回结果: %s" % request_result)
    # 查看订单详情与下单内容是否一致
    st= initialization("1", "aris_test")
    instrument_id="EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_SPOT.UNSPECIFIED.UNSPECIFIED.UNSPECIFIED"
    order_result = st.get_all_outstanding_orders(instrument_id)
    logger.info("订单详情查看: %s" % order_result)
    #断言，查看订单详情与下单内容是否一致
    assert request_result in order_result["Orders"]
    # 取消订单
    cancle_order=st.cancel_all_outstanding_orders()
    logger.info("取消订单返回结果: %s" % cancle_order)
    # 断言取消的order等于查询到的order
    assert order_result["Orders"] == cancle_order["orders"]
