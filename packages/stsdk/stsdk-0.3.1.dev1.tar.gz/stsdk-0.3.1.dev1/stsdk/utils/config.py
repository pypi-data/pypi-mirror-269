import json
import os

from stsdk.common.env import ENV_PRE, ENV_PROD, ENV_TEST, ENV_STAGE
from stsdk.utils.consul import ConsulClient


class Config:
    env = ENV_PRE
    config = {}

    def __init__(self):
        self._load_config()
        address, token = self.consul_addr
        self.consul_client = ConsulClient(address, token)
        self._get_config_from_consul()

    # 内部方法，加载配置文件
    def _load_config(self):
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../config/config.json")
        )
        try:
            with open(config_path, "r") as file:
                data = json.load(file)
                self.consul = data.get("consul", {})
                self.log = data.get("log", {})
                self.metric = data.get("metric", {})
                self.aliyun_sls = data.get("aliyun_sls", {})
            env_config_path = self.get_config_env_path()
            with open(env_config_path, "r") as file:
                data = json.load(file)
                self.api_endpoint = data.get("api_endpoint", {})
                self.redis = data.get("redis", {})
        except Exception as e:
            raise Exception(f"init config Error: {e}")

    def _get_config_from_consul(self):
        if self.env == ENV_PROD:
            self.api_endpoint = self.consul_client.get_api_endpoint()

    def __str__(self):
        return (
            f"API Endpoint: {self.api_endpoint}\n"
            f"Environment: {self.env}\n"
            f"Log Path: {self.log}\n"
            f"Strategy Module: {self.strategy_module}\n"
        )

    # 执行策略前，需要初始化一些策略本身的配置
    def init_config(self, path):
        try:
            with open(path, mode="r", encoding="utf-8") as f:
                self.config = json.load(f)
        except Exception as e:
            raise Exception(f"Error loading config file: {e}")

    # 从配置中心获取配置,仅支持读取
    def get_config(self, key):
        value = self.config.get(key, "")
        return value

    # 不同的env会带来不同的配置，需要在执行策略前设置env
    def set_env(self, env):
        self.env = env
        self._load_config()
        address, token = self.consul_addr
        self.consul_client = ConsulClient(address, token)
        self._get_config_from_consul()

    def get_config_env_path(self):
        default_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../config/test.config.json")
        )
        if self.env == ENV_TEST:
            return default_path
        if self.env == ENV_PRE:
            return os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../config/pre.config.json")
            )
        if self.env == ENV_STAGE:
            return os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../config/stage.config.json")
            )
        if self.env == ENV_PROD:
            return os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../config/prod.config.json")
            )
        return default_path

    @property
    def redis_addr(self):
        return self.redis.get("addr", "")

    @property
    def redis_port(self):
        return self.redis.get("port", 6379)

    @property
    def redis_password(self):
        return self.redis.get("password", None)

    @property
    def redis_read_timeout(self):
        return self.redis.get("read_timeout", 0.2)

    @property
    def redis_write_timeout(self):
        return self.redis.get("write_timeout", 0.2)

    @property
    def DMS_BASE_HTTP_URL(self):
        return self.api_endpoint.get("http", {}).get("dms_base_url", "")

    @property
    def DMS_BASE_WS_URL(self):
        return self.api_endpoint.get("ws", {}).get("dms_base_ws", "")

    @property
    def OMS_BASE_HTTP_URL(self):
        return self.api_endpoint.get("http", {}).get("oms_base_url", "")

    @property
    def OMS_BASE_WS_URL(self):
        return self.api_endpoint.get("ws", {}).get("oms_base_ws", "")

    @property
    def ENV(self):
        return self.env

    @property
    def LOG_PATH(self):
        return self.log.get("path", "")

    @property
    def consul_test_addr(self):
        return self.consul.get("test_addr", "")

    @property
    def consul_pre_addr(self):
        return self.consul.get("pre_addr", "")
    
    @property
    def consul_stage_addr(self):
        return self.consul.get("stage_addr", "")

    @property
    def consul_prod_addr(self):
        return self.consul.get("prod_addr", "")

    @property
    def consul_prod_token(self):
        return self.consul.get("prod_token", "")

    @property
    def metric_port(self):
        return self.metric.get("port", 8000)

    @property
    def aliyun_sls_endpoint(self):
        return self.aliyun_sls.get("endpoint", "")

    @property
    def aliyun_sls_access_key_id(self):
        return self.aliyun_sls.get("access_key_id", "")

    @property
    def aliyun_sls_access_key(self):
        return self.aliyun_sls.get("access_key", "")

    @property
    def aliyun_sls_project(self):
        return self.aliyun_sls.get("project", "")

    @property
    def aliyun_sls_log_store(self):
        return self.aliyun_sls.get("log_store", "")

    @property
    def aliyun_sls_topic(self):
        return self.aliyun_sls.get("topic", "")

    @property
    def aliyun_sls_source(self):
        return self.aliyun_sls.get("source", "")

    @property
    def aliyun_sls_time_interval(self):
        return self.aliyun_sls.get("time_interval", 1)

    @property
    def consul_addr(self):
        if self.env == ENV_TEST:
            return self.consul_test_addr, ""
        elif self.env == ENV_PRE:
            return self.consul_pre_addr, ""
        elif self.env == ENV_STAGE:
            return self.consul_stage_addr, ""
        elif self.env == ENV_PROD:
            return self.consul_prod_addr, self.consul_prod_token
        else:
            raise Exception("Error ENV")


config = Config()
