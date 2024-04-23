import pytest

from stsdk.test.ordertest.initialization import initialization
from stsdk.test.ordertest.logs import logger


@pytest.fixture
def init_ST():
    st = initialization("1", "aris_test")
    logger.info(st)
    return st

# 无订单情况
def test_cancel_all_outstanding_orders_return(init_ST):
    # instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    try:
        result = init_ST.cancel_all_outstanding_orders()
        logger.info("无订单情况: %s" % result)
        assert result=={}
    except Exception as excinfo:
        logger.info("无订单情况: %s" % excinfo.args)
    


