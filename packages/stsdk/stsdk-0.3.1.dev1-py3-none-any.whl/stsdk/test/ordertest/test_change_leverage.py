import pytest

from stsdk.test.ordertest.initialization import initialization
from stsdk.test.ordertest.logs import logger

# from stsdk.utils.log import log


@pytest.fixture
def init_ST():
    st = initialization("1", "aris_test")
    logger.info(st)
    return st
# 获取positeionid值
def generate_position_id(strategy_id, account_id, inst_id):
    return "{}.{}.{}".format(strategy_id, account_id, inst_id)

# 不存在的position_id~
def test_change_leverage_not_found_positionid(init_ST):
    position_id = 123
    leverage = 10
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("不存在的position_id: %s" % result)
    except Exception as excinfo:
        logger.info("不存在的position_id: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='position not found 123'


# 验证正确的返回
def test_change_leverage_return(init_ST):
    position_id=generate_position_id(1,"aris_test","EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    leverage = 10
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("正确的返回值: %s" % result)
        assert result['position_id']=='1.aris_test.EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED'
        assert result['leverage']==10
    except Exception as excinfo:
        logger.info("如果错误: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500

#验证leverage为0时返回异常  
def test_change_leverage_leverage_zero(init_ST):
    position_id=generate_position_id(1,"aris_test","EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    leverage = 0
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("leverage为0时异常: %s" % result)
    except Exception as excinfo:
        logger.info("leverage为0时异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='leverage 0 invalid, target leverage must in [125 , 1]'

# 验证leverage为负数时返回异常
def test_change_leverage_leverage_negative(init_ST):
    position_id=generate_position_id(1,"aris_test","EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    leverage = -1
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("leverage为负数时异常: %s" % result)
    except Exception as excinfo:
        logger.info("leverage为负数时异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='leverage -1 invalid, target leverage must in [125 , 1]'
    

# 验证leverage为超过最大值时返回异常
def test_change_leverage_leverage_Exceed(init_ST):
    position_id=generate_position_id(1,"aris_test","EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    leverage = 250
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("leverage为超过最大值时异常: %s" % result)
    except Exception as excinfo:
        logger.info("leverage为超过最大值时异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='leverage 250 invalid, target leverage must in [125 , 1]'

# 验证leverage为非数字时返回异常
def test_change_leverage_leverage_notnumer(init_ST):
    position_id=generate_position_id(1,"aris_test","EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    leverage = "test"
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("leverage为非数字时异常: %s" % result)
    except Exception as excinfo:
        logger.info("leverage为非数字时异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==400
        assert excinfo.args[0]['reason'] == 'CODEC'
        assert excinfo.args[0]['message'] == 'body unmarshal parsing field "leverage": strconv.ParseInt: parsing "test": invalid syntax'
    

# 验证leverage为None时返回异常
def test_change_leverage_leverage_none(init_ST):
    position_id=generate_position_id(1,"aris_test","EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    leverage = None
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("leverage为None时异常: %s" % result)
    except Exception as excinfo:
        logger.info("leverage为None时异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='leverage 0 invalid, target leverage must in [125 , 1]'

# 验证leverage为空时返回异常
def test_change_leverage_leverage_null(init_ST):
    position_id=generate_position_id(1,"aris_test","EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    leverage = ""
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("leverage为空时异常: %s" % result)
    except Exception as excinfo:
        logger.info("leverage为空时异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='leverage 0 invalid, target leverage must in [125 , 1]'

# 验证position_id为空时返回异常
def test_change_leverage_positionid_null(init_ST):
    position_id=""
    leverage = "10"
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("验证position_id为空时异常: %s" % result)
    except Exception as excinfo:
        logger.info("验证position_id为空时异常: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='instrument not found for '

# 验证position_id为strategy_id不正确
def test_change_leverage_positionid_wrong(init_ST):
    position_id=generate_position_id(100,"aris_test","EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    leverage = "10"
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("验证position_id为strategy_id不正确: %s" % result)
    except Exception as excinfo:
        logger.info("验证position_id为strategy_id不正确: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='position not found 100.aris_test.EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED'

# 验证position_id为account_id不正确
def test_change_leverage_positionid_acid_wrong(init_ST):
    position_id=generate_position_id(1,"aris_test1111","EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    leverage = "10"
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("验证position_id为account_id不正确: %s" % result)
    except Exception as excinfo:
        logger.info("验证position_id为account_id不正确: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='position not found 1.aris_test1111.EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED'
    
# 验证position_id为account_id不正确为空
def test_change_leverage_positionid_acid_null(init_ST):
    position_id=generate_position_id(1,"","EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    leverage = "10"
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("验证position_id为account_id不正确为空: %s" % result)
    except Exception as excinfo:
        logger.info("验证position_id为account_id不正确为空: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='position not found 1..EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED'

# 验证position_id为inst_id为空
def test_change_leverage_positionid_instid_null(init_ST):
    position_id=generate_position_id(1,"aris_test","")
    leverage = "10"
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("验证position_id为inst_id为空: %s" % result)
    except Exception as excinfo:
        logger.info("验证position_id为inst_id为空: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='position not found 1.aris_test.'

# 验证position_id为inst_id为空
def test_change_leverage_positionid_instid_allnull(init_ST):
    position_id=""
    leverage = "10"
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("验证position_id为inst_id为空: %s" % result)
    except Exception as excinfo:
        logger.info("验证position_id为inst_id为空: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='instrument not found for '

# 验证position_id和leverage都为空
def test_change_leverage_positionid_instid_isnull(init_ST):
    position_id=""
    leverage = ""
    try:
        result = init_ST.change_leverage(position_id, leverage)
        logger.info("验证position_id和leverage都为空: %s" % result)
    except Exception as excinfo:
        logger.info("验证position_id和leverage都为空: %s" % excinfo.args)
        assert excinfo.args[0]['code']==500
        assert excinfo.args[0]['message']=='leverage 0 invalid, target leverage must in [125 , 1]'