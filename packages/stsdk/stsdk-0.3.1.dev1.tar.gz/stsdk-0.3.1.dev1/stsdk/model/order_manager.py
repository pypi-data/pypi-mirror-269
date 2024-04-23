from typing import Dict, List, Set

from sortedcontainers import SortedDict
from copy import deepcopy
from stsdk.api.http.oms import OMSApi
from stsdk.common.exception import *
from stsdk.common.key import (
    CONTRACT_TYPE_LINEAR,
    ORDER_DIRECTION_BUY,
    ORDER_DIRECTION_SELL,
    ORDER_DIRECTION_BUY_STR,
    ORDER_DIRECTION_SELL_STR,
    ORDER_TYPE_LIMIT,
    ORDER_TYPE_MARKET,
    POSITION_SIDE_LONG,
    POSITION_SIDE_NOTBOTH,
    POSITION_SIDE_SHORT,
    TIME_IN_FORCE_GTC,
    HEDGING_MODE_DOWN,
    HEDGING_MODE_ON
)
from stsdk.utils.log import log


class OrderManager:
    def __init__(self, strategy_id, account_id):
        self.omsApi = OMSApi()
        # TODO: use a sorted dict
        self.openOrders: Dict[str, Dict] = {}
        self.canceling_orders: Set = set()
        self.bid_price_order_map: Dict[str, SortedDict] = {}
        self.ask_price_order_map: Dict[str, SortedDict] = {}
        self.strategy_id = strategy_id
        self.account_id = account_id

    def register_instrument(self, instrumentId):
        self.openOrders[instrumentId] = {}
        self.bid_price_order_map[instrumentId] = SortedDict()
        self.ask_price_order_map[instrumentId] = SortedDict()

    def place_order(
        self,
        instrument_id,
        price,
        size,
        side=ORDER_DIRECTION_BUY,
        position_side=POSITION_SIDE_NOTBOTH,
        contract_type=CONTRACT_TYPE_LINEAR,
        time_in_force=TIME_IN_FORCE_GTC,
        ref_id="",
    ):
        """
        下单:只提供最简单的下单方式，open_order_list更新依赖oms_order_update,在handle_order_update中更新
        :param ref_id: ref_id
        :param instrument_id:instrument_id
        :param size:下单数量
        :param price:下单价格
        :param position_side:仓位方向
        :param contract_type:合约类型
        :param side:下单方向
        :param time_in_force:time_in_force
        :return: order
        """
        data = {
            "ref_id": ref_id,
            "strategy_id": self.strategy_id,
            "account_id": self.account_id,
            "quantity": size,
            "price": price,
            "instrument_id": instrument_id,
            "position_side": position_side,
            "contract_type": contract_type,
            "order_type": ORDER_TYPE_LIMIT if price != "0" else ORDER_TYPE_MARKET,
            "order_direction": side,
            "time_in_force": time_in_force,
        }
        log.info("place order data: ", data)
        try:
            resp = self.omsApi.place_order(data)
            return resp
        except Exception as e:
            log.error(f"place order error: {e}")
            return {"err": e}

    def open_short_for_perp(
        self,
        instrument_id,
        size,
        price="0",
        contract_type=CONTRACT_TYPE_LINEAR,
        time_in_force=TIME_IN_FORCE_GTC,
    ):
        """
        永续合约开空仓
        :param instrument_id:instrument_id
        :param size:下单数量
        :param price:下单价格
        :param contract_type:合约类型
        :param time_in_force:time_in_force
        :return: order
        """
        data = {
            "instrument_id": instrument_id,
            "size": size,
            "price": price,
            "position_side": POSITION_SIDE_SHORT,
            "contract_type": contract_type,
            "side": ORDER_DIRECTION_SELL,
            "time_in_force": time_in_force,
        }
        return self.place_order(**data)

    def open_long_for_perp(
        self,
        instrument_id,
        size,
        price="0",
        contract_type=CONTRACT_TYPE_LINEAR,
        time_in_force=TIME_IN_FORCE_GTC,
    ):
        """
        永续合约开多仓
        :param instrument_id: instrument_id
        :param size: 下单数量
        :param price: 下单价格
        :param contract_type: 合约类型
        :param time_in_force: time_in_force
        :return: order
        """
        data = {
            "instrument_id": instrument_id,
            "size": size,
            "price": price,
            "position_side": POSITION_SIDE_LONG,
            "contract_type": contract_type,
            "side": ORDER_DIRECTION_BUY,
            "time_in_force": time_in_force,
        }
        return self.place_order(**data)

    def close_long_for_perp(
        self,
        instrument_id,
        size,
        price="0",
        contract_type=CONTRACT_TYPE_LINEAR,
        time_in_force=TIME_IN_FORCE_GTC,
    ):
        """
        永续合约平多仓
        :param instrument_id: instrument_id
        :param size: 下单数量
        :param price: 下单价格
        :param contract_type: 合约类型
        :param time_in_force: time_in_force
        :return: order
        """
        data = {
            "instrument_id": instrument_id,
            "size": size,
            "price": price,
            "position_side": POSITION_SIDE_LONG,
            "contract_type": contract_type,
            "side": ORDER_DIRECTION_SELL,
            "time_in_force": time_in_force,
        }
        return self.place_order(**data)

    def close_short_for_perp(
        self,
        instrument_id,
        size,
        price="0",
        contract_type=CONTRACT_TYPE_LINEAR,
        time_in_force=TIME_IN_FORCE_GTC,
    ):
        """
        永续合约平空仓
        :param instrument_id: instrument_id
        :param size: 下单数量
        :param price: 下单价格
        :param contract_type: 合约类型
        :param time_in_force: time_in_force
        :return: order
        """
        data = {
            "instrument_id": instrument_id,
            "size": size,
            "price": price,
            "position_side": POSITION_SIDE_SHORT,
            "contract_type": contract_type,
            "side": ORDER_DIRECTION_BUY,
            "time_in_force": time_in_force,
        }
        return self.place_order(**data)

    def pre_cancel_order_check(self, instrument_id, order_id):
        order_stack = self.openOrders[instrument_id]
        if order_id not in order_stack:
            raise CancelOrderNotFound(
                f"instrument {instrument_id} order {order_id} not found when attempting to cancel"
            )
        if order_id in self.canceling_orders:
            raise CancelOrderNotFound(
                f"instrument {instrument_id} order {order_id} is canceling"
            )

    def cancel_order(self, instrument_id, orderId):
        self.pre_cancel_order_check(instrument_id, orderId)
        data = {
            "order_id": orderId,
        }
        resp = self.omsApi.cancel_order(data)
        self.canceling_orders.add(orderId)
        return resp

    def cancel_order_at_price(self, instrument_id, side, price, ignore_error:bool = False):
        orders = deepcopy(self.get_order_by_price(instrument_id, price, side))
        if len(orders) > 0:
            self.cancel_batch_orders(instrument_id, orders.keys(), ignore_error=ignore_error)

    def cancel_best_price_order(self, instrument_id, side, ignore_error:bool = False):
        best_price_order = deepcopy(self.get_best_price_order(instrument_id, side))
        if best_price_order:
            return self.cancel_batch_orders(instrument_id, best_price_order[1].keys(), ignore_error=ignore_error)
        else:
            return None

    def cancel_worst_price_order(self, instrument_id, side, ignore_error:bool = False):
        worst_price_order = deepcopy(self.get_worst_price_order(instrument_id, side))
        if worst_price_order:
            return self.cancel_batch_orders(instrument_id, worst_price_order[1].keys(), ignore_error=ignore_error)
        else:
            return None

    def cancel_instrument_orders(self, instrument_id, ignore_error:bool = False):
        instrument_orders = deepcopy(self.openOrders[instrument_id])
        return self.cancel_batch_orders(instrument_id, instrument_orders.keys(), ignore_error=ignore_error)

    def cancel_batch_orders(self, instrument_id, order_ids: List[str], ignore_error:bool = False):
        resp = []
        for order_id in order_ids:
            try:
                resp.append(self.cancel_order(instrument_id, order_id))
            except CancelOrderNotFound as e:
                if ignore_error:
                    log.error(f"error encountered when canceling order instrument_id = {instrument_id} order_id = {order_id}:\n{e}")
                else:
                    raise e
        return resp

    def cancel_order_at_side(self, instrument_id: str, side: str, ignore_error:bool = False):
        orders = deepcopy(self.get_order_by_side(instrument_id, side))
        return self.cancel_batch_orders(instrument_id, orders.keys(), ignore_error=ignore_error)

    # QUESTION: if an account with only one strategy
    def cancel_all_orders(self, ignore_error:bool = False):
        # await self.omsApi.cancel_all_orders()
        resp = []
        tmp_open_orders = deepcopy(self.openOrders)
        for instrument_id, orders in tmp_open_orders.items():
            self.cancel_batch_orders(instrument_id, orders.keys(), ignore_error=ignore_error)
        return resp

    def append_order(self, instrument_id, data):
        order_id = data["order_id"]
        self.openOrders[instrument_id][order_id] = data
        # 原始下单价格
        price = float(data["origin_price"])
        if data["order_direction"] == ORDER_DIRECTION_BUY_STR:
            if price in self.bid_price_order_map[instrument_id]:
                self.bid_price_order_map[instrument_id][price][order_id] = data
            else:
                self.bid_price_order_map[instrument_id][price] = {order_id: data}
        elif data["order_direction"] == ORDER_DIRECTION_SELL_STR:
            if price in self.ask_price_order_map[instrument_id]:
                self.ask_price_order_map[instrument_id][price][order_id] = data
            else:
                self.ask_price_order_map[instrument_id][price] = {order_id: data}

    def remove_order(self, instrument_id, orderId):
        # if (
        #     instrument_id in self.openOrders
        #     and orderId in self.openOrders[instrument_id]
        # ):
        #     del self.openOrders[instrument_id][orderId]
        #     if len(self.openOrders[instrument_id]) == 0:
        #         # TODO: Why delete, will be used when return len(self.openOrders[instrument_id])
        #         del self.openOrders[instrument_id]
        #     return True

        # TODO: not use if, raise exception is needed here
        order_data = self.openOrders[instrument_id][orderId]
        price = float(order_data["origin_price"])
        if order_data["order_direction"] == ORDER_DIRECTION_BUY_STR:
            del self.bid_price_order_map[instrument_id][price][orderId]
            if len(self.bid_price_order_map[instrument_id][price]) == 0:
                del self.bid_price_order_map[instrument_id][price]
        elif order_data["order_direction"] == ORDER_DIRECTION_SELL_STR:
            del self.ask_price_order_map[instrument_id][price][orderId]
            if len(self.ask_price_order_map[instrument_id][price]) == 0:
                del self.ask_price_order_map[instrument_id][price]
        del self.openOrders[instrument_id][orderId]

        if orderId in self.canceling_orders:
            self.canceling_orders.remove(orderId)

    def remove_instrument_id(self, instrument_id):
        if instrument_id in self.openOrders:
            self.openOrders[instrument_id] = {}
            self.ask_price_order_map[instrument_id] = SortedDict()
            self.bid_price_order_map[instrument_id] = SortedDict()

    def reset(self):
        for instrument_id in self.openOrders:
            self.remove_instrument_id(instrument_id)

    def get_open_orders(self, instrument_id) -> Dict:
        return self.openOrders.get(instrument_id, {})

    def get_all_open_orders(self):
        return self.openOrders

    def get_order_by_id(self, instrument_id, orderId):
        return self.openOrders.get(instrument_id, {}).get(orderId, None)

    def get_best_price_order(self, instrument_id, side):
        best_price_order = None
        if (
            side == ORDER_DIRECTION_BUY
            and len(self.bid_price_order_map[instrument_id]) > 0
        ):
            best_price_order = self.bid_price_order_map[instrument_id].peekitem(0)
        elif (
            side == ORDER_DIRECTION_SELL
            and len(self.ask_price_order_map[instrument_id]) < 0
        ):
            best_price_order = self.ask_price_order_map[instrument_id].peekitem(-1)
        return best_price_order


    def get_worst_price_order(self, instrument_id, side):
        worst_price_order = None
        if (
            side == ORDER_DIRECTION_BUY
            and len(self.bid_price_order_map[instrument_id]) > 0
        ):
            worst_price_order = self.bid_price_order_map[instrument_id].peekitem(-1)
        elif (
            side == ORDER_DIRECTION_SELL
            and len(self.ask_price_order_map[instrument_id]) > 0
        ):
            worst_price_order = self.ask_price_order_map[instrument_id].peekitem(0)
        return worst_price_order

    def get_order_by_side(self, instrument_id, side):
        resp = {}
        if side == ORDER_DIRECTION_BUY:
            order_map = self.bid_price_order_map[instrument_id]
            for price, orders in order_map.items():
                resp.update(orders)
        elif side == ORDER_DIRECTION_SELL:
            order_map = self.ask_price_order_map[instrument_id]
            for price, orders in order_map.items():
                resp.update(orders)
        return resp

    def get_order_by_price(self, instrumentId, price, side) -> Dict:
        if side == ORDER_DIRECTION_BUY:
            return self.bid_price_order_map.get(instrumentId, {}).get(price, {})
        elif side == ORDER_DIRECTION_SELL:
            return self.ask_price_order_map.get(instrumentId, {}).get(price, {})

    def get_all_outstanding_orders(self, instrument_id):
        """
        获取所有outstanding订单
        :param instrument_id:
        :return: order list
        """
        data = {
            "strategy_id": self.strategy_id,
            "account_id": self.account_id,
            "instrument_id": instrument_id,
        }
        self.remove_instrument_id(instrument_id)
        return self.omsApi.get_all_outstanding_orders(data)

    def cancel_all_outstanding_orders(self):
        """
        取消所有outstanding订单
        :return: order list
        """
        data = {
            "strategy_id": self.strategy_id,
            "account_id": self.account_id,
        }
        orders = self.omsApi.cancel_all_outstanding_orders(data)
        # self.reset()
        return orders

    def change_leverage(self, position_id, leverage):
        """
        更改仓位杠杆倍率
        :param position_id: 仓位id
        :param leverage: 杠杆倍率
        :return position_id: 仓位id
        :return leverage: 杠杆倍率
        """
        data = {"position_id": position_id, "leverage": leverage}
        return self.omsApi.change_leverage(data)
