from stsdk.common.env import ENV_TEST
from stsdk.model.position_manager import PositionManager
from stsdk.utils.config import config
from stsdk.utils.log import log


class pmsinit(PositionManager):
    name = "ST"

    def init_params(self):
        log.info(f"init_params {self.name}")
        config.set_env(ENV_TEST)

    def start_trading_session(self):
        pass

    def run_on_data_feed(self, *args):
        pass

    