import pytest

from stsdk.test.ordertest.logs import logger
from stsdk.test.ordertest.stagegymoduletest import strategy_module_test
from stsdk.utils.config import config

'''
空订单和多订单下单测试
'''

@pytest.fixture
def init_ST():
    st = strategy_module_test("1", "aris_test")
    logger.info(st)
    return st

def test_empty_order(init_ST):
    '''
    当价格为0时下单市价单
    '''
    # instrument_id的含义：交易所币安.以太币-USDT.永续合约.线性合约.USDT.未指定
    # instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    # st=strategy_module_test("1", "aris_test")
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_short_for_perp(instrument_id=instrument_id,size=0.1,price=0)
        logger.info("下订单返回: %s" % response)
        assert response["order_id"] is not None
    except Exception as excinfo:
        logger.info("下订单异常: %s" % excinfo.args)
        assert False
        
'''
    空订单平仓
    平空单，size为0
    平空单，price为0
    平空单，price为负数
    平空单，price为空
    平空单，price为字符串
    平空单，price为None
    平空单，size为负数
    平空单，size为空
    平空单，size为字符串
    平空单，size为None
    '''
def test_empty_order_close(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price=0)
        logger.info("平空单返回: %s" % response)
        assert response["order_id"] is not None
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert False
        
def test_empty_order_close_price_large(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price=99999)
        logger.info("平空单返回: %s" % response)
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        logger.info("arg[0]平空单返回: %s" %excinfo.args[0])
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]["message"] == "invoke gms place order failed: rpc error: code = Unknown desc = <APIError> code=-4016, msg=Limit price can't be higher than 2603.49."

def test_empty_order_close_price_negative(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price="-1")
        logger.info("平空单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]["message"] == "check price and quantity error price too small, min price is 39.86"

def test_empty_order_close_price_null(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price="")
        logger.info("平空单返回: %s" % response)
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]["message"] == "validate place order request failed: validate price error,limit order price not set"

def test_empty_order_close_price_none(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price=None)
        logger.info("平空单返回: %s" % response)
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]["message"] == "validate place order request failed: validate price error,limit order price not set"

def test_empty_order_close_price_string(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price="abc")
        logger.info("平空单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]["message"] == "fail to parse price from order request"

def test_empty_order_price_big(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_short_for_perp(instrument_id=instrument_id,size=0.01,price=99999)
        logger.info("下订单返回: %s" % response)
        assert response["order_id"] is not None
    except Exception as excinfo:
        logger.info("下订单异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_price_null(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_short_for_perp(instrument_id=instrument_id,size=0.01,price="")
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
        assert response["message"]=="validate place order request failed: validate price error,limit order price not set"
    except Exception as excinfo:
        logger.info("下订单异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_price_none(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_short_for_perp(instrument_id=instrument_id,size=0.01,price=None)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
        assert response["message"]=="validate place order request failed: validate price error,limit order price not set"
    except Exception as excinfo:
        logger.info("下订单异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_price_string(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_short_for_perp(instrument_id=instrument_id,size=0.01,price="abc")
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
        assert response["message"]=="fail to parse price from order request"
    except Exception as excinfo:
        logger.info("下订单异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_price_negative(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_short_for_perp(instrument_id=instrument_id,size=0.01,price="-1")
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
        assert response["message"]=="check price and quantity error price too small, min price is 39.86"
    except Exception as excinfo:
        logger.info("下订单异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_size_negative(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_short_for_perp(instrument_id=instrument_id,size=-0.01,price=0)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
        assert response["message"] == "check price and quantity error quantity too small, min quantity is 0.001"
    except Exception as excinfo:
        logger.info("下订单异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_size_null(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_short_for_perp(instrument_id=instrument_id,size="",price=0)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
        assert response["message"] == "validate place order request failed: validate quantity error, quantity not set"
    except Exception as excinfo:
        logger.info("下订单异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_size_none(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_short_for_perp(instrument_id=instrument_id,size=None,price=0)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
        assert response["message"] == "validate place order request failed: validate quantity error, quantity not set"
    except Exception as excinfo:
        logger.info("下订单异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_size_string(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_short_for_perp(instrument_id=instrument_id,size="abc",price=0)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
        assert response["message"] == "fail to parse quantity from order request"
    except Exception as excinfo:
        logger.info("下订单异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

'''
空订单平仓
平空单，size为0
平空单，price为0
平空单，price为负数
平空单，price为空
平空单，price为字符串
平空单，price为None
平空单，size为负数
平空单，size为空
平空单，size为字符串
平空单，size为None
'''

#空订单平仓
def test_empty_order_close(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price=0)
        logger.info("平空单返回: %s" % response)
        assert response["order_id"] is not None
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
def test_empty_order_close_price_large(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price=99999)
        logger.info("平空单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_close_price_negative(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price="-1")
        logger.info("平空单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_close_price_null(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price="")
        logger.info("平空单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_close_price_none(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price=None)
        logger.info("平空单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500


def test_empty_order_close_price_string(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=0.01,price="abc")
        logger.info("平空单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_close_size_negative(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=-0.01,price=0)
        logger.info("平空单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_close_size_null(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size="",price=0)
        logger.info("平空单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_empty_order_close_size_none(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_short_for_perp(instrument_id=instrument_id,size=None,price=0)
        logger.info("平空单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception平空单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_long_order_open(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_long_for_perp(instrument_id=instrument_id,size=0.01,price=0)
        logger.info("下订单返回: %s" % response)
        assert response["order_id"] is not None
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_long_order_open_price_negative(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_long_for_perp(instrument_id=instrument_id,size=0.01,price=-0.01)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_long_order_open_price_null(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_long_for_perp(instrument_id=instrument_id,size=0.01,price=None)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_long_order_open_price_string(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_long_for_perp(instrument_id=instrument_id,size=0.01,price="abc")
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_long_order_open_size_negative(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_long_for_perp(instrument_id=instrument_id,size=-0.01,price=0.01)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_long_order_open_size_null(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_long_for_perp(instrument_id=instrument_id,size="",price=0.01)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_long_order_open_size_string(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_long_for_perp(instrument_id=instrument_id,size="abc",price=0.01)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_long_order_open_normal_small(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_long_for_perp(instrument_id=instrument_id,size=0.01,price=0.01)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_long_order_open_normal_large(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.open_long_for_perp(instrument_id=instrument_id,size=20,price=139.86)
        logger.info("下订单返回: %s" % response)
        assert response["order_id"] is not None
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_close_long_order_price_negative(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_long_for_perp(instrument_id=instrument_id,size=0.01,price=-0.01)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_close_long_order_price_null(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_long_for_perp(instrument_id=instrument_id,size=0.01,price="")
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_close_long_order_price_string(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_long_for_perp(instrument_id=instrument_id,size=0.01,price="abc")
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_close_long_order_size_negative(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_long_for_perp(instrument_id=instrument_id,size=-0.01,price=0.01)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_close_long_order_size_null(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_long_for_perp(instrument_id=instrument_id,size="",price=0.01)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_close_long_order_size_string(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_long_for_perp(instrument_id=instrument_id,size="abc",price=0.01)
        logger.info("下订单返回: %s" % response)
        assert response["code"] == 500
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_close_long_order_normal_large(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_long_for_perp(instrument_id=instrument_id,size=0.01,price=99999)
        logger.info("下订单返回: %s" % response)
        assert response["order_id"] is not None
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

def test_close_long_order_normal_small(init_ST):
    instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        response = init_ST.close_long_for_perp(instrument_id=instrument_id,size=0.01,price=2578.86)
        logger.info("下订单返回: %s" % response)
        assert response["order_id"] is not None
    except Exception as excinfo:
        logger.info("exception下订单返回: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
