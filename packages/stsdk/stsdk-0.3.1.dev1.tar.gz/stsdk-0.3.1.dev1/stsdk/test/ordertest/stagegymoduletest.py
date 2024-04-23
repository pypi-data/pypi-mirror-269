import asyncio
import time

from stsdk.common.env import ENV_TEST
from stsdk.common.key import DMS_BBO, HEDGING_MODE_ON, OMS_ORDER_UPDATE
from stsdk.model.strategy_module import StrategyModule
from stsdk.utils.config import config
from stsdk.utils.log import log


class strategy_module_test(StrategyModule):
    name = "ST1"

    def init_params(self):
        log.info(f"init_params {self.name}")
        # 设置测试环境
        config.set_env(ENV_TEST)
        # 注册 DMS_BBO 和 OMS_ORDER_UPDATE 事件，并指定相应的处理函数
        self.hedging_mode = HEDGING_MODE_ON
        self.instrument_id = "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
        self.register_instrument(self.instrument_id, 10, 10)
        self.register(
            DMS_BBO,
            self.handle_bbo,
            instrument_id=self.instrument_id,
        )
        self.register(
            OMS_ORDER_UPDATE,
            self.handle_order_update,
            strategy_id=self.strategy_id,
            account_id=self.account_id,
        )

    # 开始交易会话的方法
    def start_trading_session(self):
        pass

    # 数据提供方法
    def run_on_data_feed(self, *args):
        pass

    # 错误处理方法
    def handle_error(self, error):
        print("error", error)
        pass

    # 处理 BBO（最佳买卖盘报价）的方法
    def handle_bbo(self, message):
        log.info(f"bbo: {message}")
        # self.place_order_signal(
        #     "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        #     "1000",
        #     "0.1",
        #     "buy",
        # )

    # 处理订单更新的方法
    def handle_order_update(self, message):
        log.info("order update", message)
        body = message["body"]
        order_id = body["order_id"]
        instrument_id = body["instrument_id"]
        log.info(f"order_id: {order_id}, instrument_id: {instrument_id}")
        # self.cancel_order_signal(
        #     instrument_id,
        #     order_id,
        # )

    def handle_redis_message(self, message):
        log.info(f"handle_redis_message: {message}")