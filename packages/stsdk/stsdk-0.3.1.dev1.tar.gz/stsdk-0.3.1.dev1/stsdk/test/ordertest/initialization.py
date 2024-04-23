import asyncio

from stsdk.common.env import ENV_TEST
from stsdk.model.order_manager import OrderManager
# from stsdk.model.strategy_module import StrategyModule
from stsdk.utils.config import config
from stsdk.utils.log import log


class initialization(OrderManager):
    name = "ST"

    def init_params(self):
        log.info(f"init_params {self.name}")
        config.set_env(ENV_TEST)

    def start_trading_session(self):
        pass

    def run_on_data_feed(self, *args):
        pass

# st = initialization("1", "aris_test")
# log.info(st)


# def test():
#     result=st.change_leverage(123, 10)
#     log.info("change_leverage: %s" % result)

# async def main():
#     test()

# if __name__ == "__main__":
#     asyncio.run(main())