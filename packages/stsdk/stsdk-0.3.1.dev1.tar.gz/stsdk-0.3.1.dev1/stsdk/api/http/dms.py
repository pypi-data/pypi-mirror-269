import datetime
from stsdk.common.key import STRING_SECURITY_TYPE_SPOT
from stsdk.utils.config import config
from stsdk.utils.http import request


class DMSApi:

    def __init__(self):
        self.DMS_BASE_HTTP_URL = config.DMS_BASE_HTTP_URL

    def get_instrument_info(self, params=None):
        if params is None:
            return None
        symbol, exchange, security_type, contract_type, external_symbol = (
            params.get("symbol"),
            params.get("exchange"),
            params.get("security_type"),
            params.get("contract_type", "UNSPECIFIED"),
            params.get("external_symbol", ""),
        )
        if security_type == STRING_SECURITY_TYPE_SPOT:
            contract_type = None
        resp = request.get(
            self.DMS_BASE_HTTP_URL + "/v1/instruments",
            params={
                "symbol": symbol,
                "exchange": exchange,
                "security_type": security_type,
                "contract_type": contract_type,
                "external_symbol": external_symbol,
            },
        )
        return resp

    def get_kline_spot(self, params=None):
        if params is None:
            return None
        symbol, exchange, interval, start_time, end_time, limit = (
            params.get("symbol"),
            params.get("exchange"),
            params.get("interval", "1m"),
            params.get("start_time", 0),
            params.get("end_time", datetime.now().timestamp()),
            params.get("limit", 10),
        )
        if symbol is None or exchange is None:
            return None
        resp = request.get(
            self.DMS_BASE_HTTP_URL + "/v1/klines/spot",
            params={
                "symbol": symbol,
                "exchange": exchange,
                "interval": interval,
                "start_time": start_time,
                "end_time": end_time,
                "limit": limit,
            },
        )
        return resp

    def get_kline_ufuture(self, params=None):
        if params is None:
            return None
        symbol, exchange, interval, start_time, end_time, limit = (
            params.get("symbol"),
            params.get("exchange"),
            params.get("interval", "1m"),
            params.get("start_time", 0),
            params.get("end_time", datetime.now().timestamp()),
            params.get("limit", 10),
        )
        if symbol is None or exchange is None:
            return None
        resp = request.get(
            self.DMS_BASE_HTTP_URL + "/v1/klines/u-future",
            params={
                "symbol": symbol,
                "exchange": exchange,
                "interval": interval,
                "start_time": start_time,
                "end_time": end_time,
                "limit": limit,
            },
        )
        return resp

    def get_kline_cfuture(self, params=None):
        if params is None:
            return None
        symbol, exchange, interval, start_time, end_time, limit = (
            params.get("symbol"),
            params.get("exchange"),
            params.get("interval", "1m"),
            params.get("start_time", 0),
            params.get("end_time", datetime.now().timestamp()),
            params.get("limit", 10),
        )
        if symbol is None or exchange is None:
            return None
        resp = request.get(
            self.DMS_BASE_HTTP_URL + "/v1/klines/c-future",
            params={
                "symbol": symbol,
                "exchange": exchange,
                "interval": interval,
                "start_time": start_time,
                "end_time": end_time,
                "limit": limit,
            },
        )
        return resp

    def get_bbo(self, params=None):
        if params is None:
            return None
        instrument_id, limit = params.get("instrument_id"), params.get("limit")
        if instrument_id is None or limit is None:
            return None
        resp = request.get(
            self.DMS_BASE_HTTP_URL + "/v1/bbo/latest",
            params={
                "instrument_id": instrument_id,
                "limit": limit,
            },
        )
        return resp

    def get_price(self, params=None):
        if params is None:
            return None
        instrument_id = params.get("instrument_id")
        if instrument_id is None:
            return None
        resp = request.get(
            self.DMS_BASE_HTTP_URL + "/v1/price",
            params={
                "instrument_id": instrument_id,
            },
        )
        return resp

    def get_mark_price(self, params=None):
        if params is None:
            return None
        instrument_id = params.get("instrument_id")
        if instrument_id is None:
            return None
        resp = request.get(
            self.DMS_BASE_HTTP_URL + "/v1/mark-price",
            params={
                "instrument_id": instrument_id,
            },
        )
        return resp

    def get_lob(self, params=None):
        if params is None:
            return None
        instrument_id = params.get("instrument_id")
        if instrument_id is None:
            return None
        resp = request.get(
            self.DMS_BASE_HTTP_URL + "/v1/order-book/snapshot",
            params={
                "instrument_id": instrument_id,
            },
        )
        return resp
