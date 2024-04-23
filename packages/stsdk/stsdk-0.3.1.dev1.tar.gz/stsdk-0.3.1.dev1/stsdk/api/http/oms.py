from stsdk.utils.config import config
from stsdk.utils.http import request


class OMSApi:

    def __init__(self, params=None):
        self.OMS_BASE_HTTP_URL = config.OMS_BASE_HTTP_URL

    def place_order(self, data=None):
        if data is None:
            return
        resp = request.post(self.OMS_BASE_HTTP_URL + "/order/new", data=data)
        return resp

    def cancel_order(self, data=None):
        if data is None:
            return
        order_id = data.get("order_id")
        if order_id is None:
            return
        resp = request.patch(self.OMS_BASE_HTTP_URL + "/order/" + order_id, data=data)
        return resp

    def close_order(self, data=None):
        if data is None:
            return
        resp = request.delete(self.OMS_BASE_HTTP_URL + "/order/new", data=data)
        return resp

    def cancel_all_orders(self, data=None):
        pass

    def cancel_orders(self, data=None):
        pass

    def get_order(self, params=None):
        if params is None:
            return
        order_id = params.get("order_id")
        resp = request.get(self.OMS_BASE_HTTP_URL + "/order/" + order_id, params=params)
        return resp

    def get_all_outstanding_orders(self, params=None):
        if params is None:
            return
        resp = request.get(self.OMS_BASE_HTTP_URL + "/all/outstanding/orders", params=params)
        return resp

    def cancel_all_outstanding_orders(self, data=None):
        if data is None:
            return
        resp = request.patch(self.OMS_BASE_HTTP_URL + "/cancel/all/order", data=data)
        return resp

    def close_all_positions(self, data=None):
        if data is None:
            return
        resp = request.post(self.OMS_BASE_HTTP_URL + "/position/closeAll", data=data)
        return resp

    def change_leverage(self, data=None):
        if data is None:
            return
        resp = request.post(self.OMS_BASE_HTTP_URL + "/leverage", data=data)
        return resp

    def get_all_positions(self, params=None):
        resp = request.get(self.OMS_BASE_HTTP_URL + "/position/all", params=params)
        return resp

    def get_position_mode(self, params=None):
        resp = request.get(self.OMS_BASE_HTTP_URL + "/account/positionMode", params=params)
        return resp

    def change_position_mode(self, data=None):
        if data is None:
            return
        resp = request.post(self.OMS_BASE_HTTP_URL + "/account/positionMode", data=data)
        return resp
