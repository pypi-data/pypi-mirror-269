import pytest

from stsdk.test.ordertest.GetOrderFormPositionId import GetOrderFromPositionId
from stsdk.test.ordertest.logs import logger
from stsdk.test.ordertest.placeOrder import placeOrder
from stsdk.test.ordertest.pmsinit import pmsinit

'''
下单一个市价单，然后操作平仓，平常之后查看仓位不存在。查看仓位是否存在的接口需要知道。

'''
# 一键平仓执行
def test_close_all_positions_return():
    # 操作下单，定义入参参数并进行校验
    orderinfo = {
        "strategy_id": "1", 
        "symbol": "BTC-USDT", 
        "quantity": "0.009",
        "price": "20000",  #价格不填写的情况下会是市价单
        # "settle_ccy": "USDT", 
        # "expiry_date": "",  #过期时间
        # "security_type": 1,  #SECURITY_TYPE_SPOT正确 2:SECURITY_TYPE_PERP
        "position_side": 3,  #POSITION_SIDE_NOTBOTH
        "order_type": 1,  #ORDER_TYPE_LIMIT 1:ORDER_TYPE_MARKET
        # "exchange": 1,   #返回EXCHANGE_BINANCE正确
        "order_direction": 1,  #ORDER_DIRECTION_BUY
        "time_in_force": 1,  #TIME_IN_FORCE_GTC
        "leverage": 0,  #杠杆倍数
        # "contract_type": 0, #CONTRACT_TYPE_LINEAR
        "account_id": "aris_test",
        # "instrument_id": "EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_SPOT.UNSPECIFIED.UNSPECIFIED.UNSPECIFIED"
        "instrument_id": "EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    }
    #下单操作
    try:
        request_result = placeOrder.get_placeOrder(orderinfo).json()
        logger.info(f"下单返回结果: {request_result}")
        assert request_result["strategy_id"] == orderinfo["strategy_id"]
        assert request_result["account_id"] == orderinfo["account_id"]
        assert request_result["instrument_id"] == orderinfo["instrument_id"]
        assert request_result["symbol"] == orderinfo["symbol"]
        assert request_result["exchange"] == "EXCHANGE_BINANCE"
        assert request_result["security_type"] == "SECURITY_TYPE_PERP"
        assert request_result["order_type"] == "ORDER_TYPE_MARKET"
        # assert request_result["origin_price"] == "0" 
        assert request_result["origin_quantity"] == orderinfo["quantity"]
        assert request_result["order_direction"] == "ORDER_DIRECTION_BUY"
        assert request_result["position_side"] == "POSITION_SIDE_NOTBOTH"
        # assert request_result["order_status"] == "ORDER_STATUS_FILLED" "ORDER_DIRECTION_BUY"
        assert request_result["time_in_force"] == "TIME_IN_FORCE_GTC"
    except Exception as excinfo:
        logger.info("exception验证下单: %s" % excinfo.args)
    # print(type(request_result))
    # 断言下单应该要返回的结果是预期设计的结果
    # 下单之后操作平仓
    st=pmsinit("1", "aris_test")
    try:
        close_position=st.close_all_positions()
        logger.info(f"平仓结果: {close_position}")
    except Exception as excinfo:
        logger.info("exception平仓结果: %s" % excinfo.args)
        assert False
    # 断言，平常结果与下单结果订单一致
    #查询订单不存在了
    try:
        request_gopid=GetOrderFromPositionId.get_PositionId("1", "aris_test", "EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    # 断言，订单返回结果filled_position应该为0
        assert request_gopid["long_position"]["filled_position"] == "0"
    # logger.info(f"查询订单情况: {request_gopid}")
    except Exception as excinfo:
        logger.info("exception查询订单情况: %s" % excinfo.args)
        assert False