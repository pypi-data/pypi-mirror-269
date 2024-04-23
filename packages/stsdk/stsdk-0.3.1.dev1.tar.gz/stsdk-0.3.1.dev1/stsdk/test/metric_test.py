import asyncio
import time
import random

import sys


from stsdk.common.env import ENV_PRE, ENV_TEST
from stsdk.common.key import HEDGING_MODE_DOWN, DMS_BBO
from stsdk.model.strategy_module import StrategyModule
from stsdk.utils.config import config
from stsdk.utils.log import log
from stsdk.utils.metric import MetricUtil
from stsdk.utils.ali_sls import sls_data


def simple_test():
    met = MetricUtil()
    met.add_gauge("test_gauge", "test gauge", ["label1", "label2"])
    met.metric_guage("test_gauge", {"signal_BTC": "1", "label2": "2"}, 100)
    while True:
        pass


class ST1(StrategyModule):
    name = "ST1"

    def __init__(self, strategy_id, account_id):
        config.set_env(ENV_TEST)
        self.metric_name = "signal_BTC_CM_240628"
        super().__init__(strategy_id, account_id)

    def init_params(self):
        log.info(f"init_params {self.name}")
        # 注册 DMS_BBO 和 OMS_ORDER_UPDATE 事件，并指定相应的处理函数
        self._hedging_mode = HEDGING_MODE_DOWN
        self.instrument_id = "EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
        # self.instrument_id = "EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_FUTURE.CONTRACT_TYPE_LINEAR.USDT.2024-06-28"
        self.register_instrument(self.instrument_id, 10, 10)
        self.register(
            DMS_BBO,
            self.handle_bbo,
            instrument_id=self.instrument_id,
        )
        # 添加打点
        self._metric.add_gauge("test_gauge", "test gauge", [self.metric_name, "label2"])

    # 开始交易会话的方法
    def start_trading_session(self):
        pass

    # 数据提供方法
    def run_on_data_feed(self, *args):
        pass

    # 错误处理方法
    def handle_error(self, error):
        log.error(f"error: {error}")
        pass

    # 处理 BBO（最佳买卖盘报价）的方法
    def handle_bbo(self, message):
        # self._metric.metric_time("ws_oms_stsdk", message["topic"], message["tt"] / 1000000, time.time())
        # log.info(f"bbo: {message}")
        self._metric.metric_guage("test_gauge", {self.metric_name: "1", "label2": "2"}, random.randint(0, 100))

        # self._metric.metric_guage("test_gauge", {"kind": "signal_BTC_CM_240628", "operation": "siginal"},
        # random.randint(0, 100)) self._metric.metric_guage("test_gauge", {"kind": "signal_BTC_CM_240628",
        # "operation": "ask"}, random.randint(0, 100)) self._metric.metric_guage("test_gauge",
        # {"kind": "positionManager_BTC_CM_240628", "operation": "ask"}, random.randint(0, 100))
        sls_data.set_project(project="st-sdk-log")  # 设置一次就可以
        log_store = "st-sdk-log-pre"
        topic = "trade-log"
        source = "tianjian-pre"
        contents = [
            ("timestamp", str(int(time.time()))),
            ("order_id", "15qeny11000czf666xda7ha9vlv0g706"),
        ]
        sls_data.put_logs(log_store, topic, source, False, contents)

    # 处理订单更新的方法
    def handle_order_update(self, message):
        log.info("order update", message)
        body = message["body"]
        order_id = body["order_id"]
        instrument_id = body["instrument_id"]
        log.info(f"order_id: {order_id}, instrument_id: {instrument_id}")

    def handle_redis_message(self, message):
        log.info(f"handle_redis_message: {message}")


async def main():
    st = ST1("1", "aris_test")


if __name__ == "__main__":
    asyncio.run(main())