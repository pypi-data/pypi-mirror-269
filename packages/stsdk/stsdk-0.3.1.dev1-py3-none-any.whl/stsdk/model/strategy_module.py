import threading
from typing import Dict, List
from copy import deepcopy
from stsdk.model.instrument import CONTRACT_TYPE
from stsdk.utils.config import config
from stsdk.common.exception import (OrderPlaceExceedLimit, TradingException, OperationException,
                                    SelfCrossOrderEncountered, CancelOrderNotFound, OrderQtyInValid)
from stsdk.common.key import (
    ORDER_DIRECTION_BUY,
    ORDER_DIRECTION_SELL,
    ORDER_STATUS_CANCELED,
    ORDER_STATUS_EXPIRED,
    ORDER_STATUS_FILLED,
    ORDER_STATUS_OMS_CREATED,
    ORDER_STATUS_OMS_PLACE_ORDER_FAILED,
    ORDER_STATUS_PARTIALLY_FILLED,
    ORDER_STATUS_REJECTED,
    POSITION_SIDE_LONG,
    POSITION_SIDE_NOTBOTH,
    POSITION_SIDE_SHORT,
    POSITION_SIDE_MAP,
    ORDER_DIRECTION_MAP,
    HEDGING_MODE_UNSPECIFIED,
    HEDGING_MODE_DOWN,
    HEDGING_MODE_ON
)
from stsdk.common.signal_key import CANCEL_ORDER_SIGNAL, PLACE_ORDER_SIGNAL
from stsdk.model.order_manager import OrderManager
from stsdk.model.position_manager import PositionManager
from stsdk.model.strategy_base import StrategyBaseModule
from stsdk.utils.log import log
import stsdk.utils.precision as prec


class StrategyModule(StrategyBaseModule):
    def __init__(self, strategy_id, account_id):
        self._hedging_mode = HEDGING_MODE_UNSPECIFIED
        self._positionManager = PositionManager(strategy_id, account_id)
        self._orderManager = OrderManager(strategy_id, account_id)
        super().__init__(strategy_id, account_id)
        self.sync_position_mode()
        self.init_order_thread()
        log.info("StrategyModule init")
        self.exec_start_trading_session()

    def init_order_thread(self):
        threading.Thread(target=self.consumer_with_signal).start()

    # 需要手动初始化对应的instrument_id，以及对应的开仓限额
    def register_instrument(
            self, instrument_id, long_open_quota: float, short_open_quota: float
    ):
        self._positionManager.register_instrument(
            instrumentId=instrument_id,
            long_opening_quota=long_open_quota,
            short_opening_quota=short_open_quota,
        )
        self._orderManager.register_instrument(instrumentId=instrument_id)

    def register(self, event, func, **kwargs):
        if "instrument_id" in kwargs:
            if kwargs["instrument_id"] not in self._positionManager.instruments:
                raise OperationException(f"{kwargs['instrument_id']} not registered")
        super().register(event, func, **kwargs)

    def get_instrument(self, instrument_id):
        return self._positionManager.get_instrument(instrument_id)

    def sync_position_mode(self):
        if self._hedging_mode == HEDGING_MODE_UNSPECIFIED:
            raise OperationException(
                f"hedging mode should be set explicitly in init_params current hedging mode is {self._hedging_mode}")
        is_hedging_mode = self._positionManager.get_position_mode()
        hedging_mode = HEDGING_MODE_ON if is_hedging_mode else HEDGING_MODE_DOWN
        log.info(f"current hedging mode is {hedging_mode}")
        if self._hedging_mode != hedging_mode:
            is_both = (self._hedging_mode == HEDGING_MODE_ON)
            self._positionManager.change_position_mode(is_both)
            log.info(f"change hedging mode to {self._hedging_mode}")

    def check_order_selfcrossing(self, instrument_id, side, price):
        if side == ORDER_DIRECTION_BUY:
            opposite_side = self._orderManager.get_best_price_order(instrument_id=instrument_id,
                                                                    side=ORDER_DIRECTION_SELL)
            if opposite_side is not None:
                if price >= opposite_side[0]:
                    raise SelfCrossOrderEncountered(
                        f"{instrument_id} {side} order ecountered self-crossing at price = {price}")
        elif side == ORDER_DIRECTION_SELL:
            opposite_side = self._orderManager.get_best_price_order(instrument_id=instrument_id,
                                                                    side=ORDER_DIRECTION_BUY)
            if opposite_side is not None:
                if price <= opposite_side[0]:
                    raise SelfCrossOrderEncountered(
                        f"{instrument_id} {side} order ecountered self-crossing at price = {price}")

    def check_order_qty(self, instrument_id, size, price):
        instrument = self.get_instrument(instrument_id)
        if size < instrument.qty_unit:
            raise OrderQtyInValid(
                f"Invalid order qty encountered: instrument_id = {instrument_id} price = {price} size = {size} "
                f"qty_unit = {instrument.qty_unit}")
        if size * price < instrument.min_notional and price > 0 and instrument.contract_type != CONTRACT_TYPE.INVERSE:
            raise OrderQtyInValid(
                f"Invalid order notional amount encountered: instrument_id = {instrument_id} price = {price} "
                f"size = {size} min_notional = {instrument.min_notional}")

    def pre_place_order_check(self, instrument_id, price, side, size, position_side):
        # 是否是双向模式，默认单向模式
        self.check_order_selfcrossing(instrument_id, side, price)
        self.check_order_qty(instrument_id, size, price)
        if self._hedging_mode == HEDGING_MODE_DOWN:
            if position_side != POSITION_SIDE_NOTBOTH:
                raise TradingException(
                    f"position_side must be POSITION_NOT_BOTH_STR when hedging_mode == False, got {position_side}"
                )
            qty = size
            instr_qty_unit = self.get_instrument(instrument_id).qty_unit
            if side == ORDER_DIRECTION_BUY:
                if self._positionManager.get_active_short_close_quota(instrument_id) > 0:
                    _update_size = min(
                        self._positionManager.get_active_short_close_quota(
                            instrument_id
                        ),
                        size,
                    )
                    qty = prec.substract(qty, _update_size, instr_qty_unit)
                if qty > 0:
                    quota = self._positionManager.get_active_long_open_quota(
                        instrument_id
                    )
                    if self.get_position(instrument_id).long_filled + self.get_position(instrument_id).long_outstanding + qty > quota:
                        raise OrderPlaceExceedLimit(
                            f"instrument {instrument_id} order size {size} exceeds long_open_quota: {quota}, "
                            f"in which {qty} used to open long position"
                        )
            elif side == ORDER_DIRECTION_SELL:
                if self._positionManager.get_active_long_close_quota(instrument_id) > 0:
                    _update_size = min(
                        self._positionManager.get_active_long_close_quota(instrument_id),
                        size,
                    )
                    qty = prec.substract(qty, _update_size, instr_qty_unit)
                if qty > 0:
                    quota = self._positionManager.get_active_short_open_quota(
                        instrument_id
                    )
                    if self.get_position(instrument_id).short_filled + self.get_position(instrument_id).short_outstanding > quota:
                        raise OrderPlaceExceedLimit(
                            f"instrument {instrument_id} order size {size} exceeds short_open_quota: {quota}, "
                            f"in which {qty} used to open short position"
                        )
            else:
                raise TradingException(f"order side not recognized, got {side}")
        elif self._hedging_mode == HEDGING_MODE_ON:
            if position_side == POSITION_SIDE_LONG:
                if side == ORDER_DIRECTION_BUY:
                    quota = self._positionManager.get_active_long_open_quota(
                        instrument_id
                    )
                    if size > quota:
                        raise OrderPlaceExceedLimit(
                            f"instrument {instrument_id} order size {size} exceeds long_open_quota: {quota}"
                        )
                elif side == ORDER_DIRECTION_SELL:
                    quota = self._positionManager.get_active_long_close_quota(
                        instrument_id
                    )
                    if size > quota:
                        raise OrderPlaceExceedLimit(
                            f"instrument {instrument_id} order size {size} exceeds long_close_quota {quota}"
                        )
                else:
                    raise TradingException(f"order side not recognized, got {side}")
            elif position_side == POSITION_SIDE_SHORT:
                if side == ORDER_DIRECTION_BUY:
                    quota = self._positionManager.get_active_short_close_quota(
                        instrument_id
                    )
                    if size > quota:
                        raise OrderPlaceExceedLimit(
                            f"instrument {instrument_id} order size {size} exceeds short_close_quota {quota}"
                        )
                elif side == ORDER_DIRECTION_SELL:
                    quota = self._positionManager.get_active_short_open_quota(
                        instrument_id
                    )
                    if size > quota:
                        raise OrderPlaceExceedLimit(
                            f"instrument {instrument_id} order size {size} exceeds short_open_quota {quota}"
                        )
                else:
                    raise TradingException(f"order side not recognized, got {side}")
            else:
                raise TradingException(
                    f"position_side must be either POSITION_SIDE_LONG_STR or POSITION_SIDE_SHORT_STR when "
                    f"hedging_mode == True, got {position_side}"
                )

    # 使用信号下单，本质上是通过blinker发送一个信号，然后通过信号处理函数来下单，这样无需等待接口返回，可以提高下单速度
    def place_order_signal(
            self,
            instrument_id,
            price,
            size,
            side,
            position_side=POSITION_SIDE_NOTBOTH,
            ref_id="",
            **kwargs,
    ):
        op_info = {
            "origin_quantity": size,
            "position_side": POSITION_SIDE_MAP[position_side],
            "order_direction": ORDER_DIRECTION_MAP[side]
        }
        self.pre_place_order_check(instrument_id, price, side, size, position_side)
        self._positionManager.update_place_order(instrument_id, op_info)
        message = {
            "instrument_id": instrument_id,
            "price": price,
            "size": size,
            "side": side,
            "position_side": position_side,
            "ref_id": ref_id,
            **kwargs,
        }
        PLACE_ORDER_SIGNAL.send(message)

    # 使用信号撤单，本质上是通过blinker发送一个信号，然后通过信号处理函数来撤单，这样无需等待接口返回，可以提高撤单速度
    def cancel_order_signal(self, instrument_id, order_id):
        self._orderManager.pre_cancel_order_check(instrument_id, order_id)
        message = {
            "instrument_id": instrument_id,
            "order_id": order_id,
        }
        CANCEL_ORDER_SIGNAL.send(message)

    def cancel_batch_orders_signal(self, instrument_id, order_ids: List[str], ignore_error: bool = False):
        for order_id in order_ids:
            try:
                self.cancel_order_signal(instrument_id, order_id)
            except CancelOrderNotFound as e:
                if ignore_error:
                    log.error(
                        f"error encountered when canceling order: instrument_id = {instrument_id} "
                        f"order_id = {order_id} error = {e}")
                else:
                    raise e

    def cancel_orders_at_side_signal(self, instrument_id, side, ignore_error: bool = False):
        orders = deepcopy(self.get_order_by_side(instrument_id, side))
        self.cancel_batch_orders_signal(instrument_id, list(orders.keys()), ignore_error=ignore_error)

    def cancel_orders_at_price_signal(self, instrument_id, side, price, ignore_error: bool = False):
        orders = deepcopy(self.get_order_by_price(instrument_id, side, price))
        self.cancel_batch_orders_signal(instrument_id, orders.keys(), ignore_error=ignore_error)

    def cancel_instrument_orders_signal(self, instrument_id, ignore_error: bool = False):
        orders = deepcopy(self.get_open_orders(instrument_id))
        self.cancel_batch_orders_signal(instrument_id, orders.keys(), ignore_error=ignore_error)

    def cancel_all_orders_signal(self, instrument_id, ignore_error: bool = False):
        orders = self.get_all_open_orders()
        tmp_orders = deepcopy(orders)
        for instrument_id in tmp_orders.keys():
            self.cancel_instrument_orders_signal(instrument_id, ignore_error=ignore_error)

    # TODO: multi-threading cancel_order_at_price ...

    def place_order_handle(self, message):
        instrument_id, price, size, side, position_side, ref_id = message.values()
        self.place_order(instrument_id, price, size, side, position_side, ref_id)

    def cancel_order_handle(self, message):
        instrument_id, order_id = message.values()
        self.cancel_order(instrument_id, order_id)

    def consumer_with_signal(self):
        PLACE_ORDER_SIGNAL.connect(self.place_order_handle)
        CANCEL_ORDER_SIGNAL.connect(self.cancel_order_handle)

    # 下单基础函数，封装了对应下单接口的调用，以及下单后的持仓更新
    def place_order(
            self,
            instrument_id,
            price,
            size,
            side,
            position_side=POSITION_SIDE_NOTBOTH,
            ref_id="",
            **kwargs,
    ):
        # self.pre_place_order_check(instrument_id, price, side, size, position_side)
        # QUESTION: reponse format? add in docs
        resp = self._orderManager.place_order(
            instrument_id=instrument_id,
            price=price,
            size=size,
            side=side,
            position_side=position_side,
            ref_id=ref_id,
            **kwargs
        )
        if "err" in resp:
            log.error("place_order error: %s" % resp)
        return resp

    # 永续合约开空单
    def open_short_for_perp(self, instrument_id, size, price, **kwargs):
        resp = self._orderManager.open_short_for_perp(
            instrument_id, size, price, **kwargs
        )
        log.info("open_short_for_perp resp: %s" % resp)
        if "order_id" in resp:
            self._positionManager.update_position(
                resp["instrument_id"], resp
            )
        else:
            log.error("open_short_for_perp error: %s" % resp)
        return resp

    # 永续合约开多单
    def open_long_for_perp(self, instrument_id, size, price, **kwargs):
        resp = self._orderManager.open_long_for_perp(
            instrument_id, size, price, **kwargs
        )
        log.info("open_long_for_perp resp: %s" % resp)
        if "order_id" in resp:
            self._positionManager.update_position(
                resp["instrument_id"], resp
            )
        else:
            log.error("open_long_for_perp error: %s" % resp)
        return resp

    # 永续合约平多单
    def close_long_for_perp(self, instrument_id, size, price, **kwargs):
        resp = self._orderManager.close_long_for_perp(
            instrument_id, size, price, **kwargs
        )
        log.info("close_long_for_perp resp: %s" % resp)
        if "order_id" in resp:
            self._positionManager.update_position(
                resp["instrument_id"], resp
            )
        else:
            log.error("close_long_for_perp error: %s" % resp)
        return resp

    # 永续合约平空单
    def close_short_for_perp(self, instrument_id, size, price, **kwargs):
        resp = self._orderManager.close_short_for_perp(
            instrument_id, size, price, **kwargs
        )
        log.info("close_short_for_perp resp: %s" % resp)
        if "order_id" in resp:
            self._positionManager.update_position(
                resp["instrument_id"], resp
            )
        else:
            log.error("close_short_for_perp error: %s" % resp)
        return resp

    # 批量下单基础函数，封装了对应下单接口的调用，以及下单后的持仓更新
    def place_batch_orders(self, orders: List[Dict]):
        resp = []
        for o in orders:
            resp.append(self.place_order(**o))
        return resp

    # 撤单基础函数，封装了对应撤单接口的调用，以及撤单后的持仓更新

    def cancel_order(self, instrument_id, order_id):
        self._orderManager.pre_cancel_order_check(instrument_id, order_id)
        return self._orderManager.cancel_order(instrument_id, order_id)

    # 批量撤单基础函数，封装了对应撤单接口的调用，以及撤单后的持仓更新
    def cancel_batch_orders(self, instrument_id, order_ids, ignore_error: bool = False):
        return self._orderManager.cancel_batch_orders(instrument_id, order_ids, ignore_error=ignore_error)

    def cancel_best_price_order(self, instrument_id, side, ignore_error: bool = False):
        return self._orderManager.cancel_best_price_order(instrument_id, side, ignore_error=ignore_error)

    def cancel_worst_price_order(self, instrument_id, side, ignore_error: bool = False):
        return self._orderManager.cancel_worst_price_order(instrument_id, side, ignore_error=ignore_error)

    def cancel_order_at_price(self, instrument_id, side, price: float, ignore_error: bool = False):
        return self._orderManager.cancel_order_at_price(
            instrument_id=instrument_id, side=side, price=price, ignore_error=ignore_error
        )

    def cancel_instrument_orders(self, instrument_id, ignore_error: bool = False):
        return self._orderManager.cancel_instrument_orders(instrument_id, ignore_error=ignore_error)

    def cancel_orders_at_side(self, instrument_id, side, ignore_error: bool = False):
        return self._orderManager.cancel_order_at_side(
            instrument_id=instrument_id, side=side, ignore_error=ignore_error
        )

    def cancel_all_orders(self):
        # if an account to only one strategy
        return self._orderManager.cancel_all_outstanding_orders()

    # 获取持仓基础函数，封装了对应持仓接口的调用
    def get_position(self, instrument_id):
        return self._positionManager.get_position(instrument_id)

    # 获取目前还在挂的订单基础函数
    def get_open_orders(self, instrument_id) -> Dict:
        return self._orderManager.get_open_orders(instrument_id)

    # 获取目前还在挂所有的持仓基础函数
    def get_all_open_orders(self):
        return self._orderManager.get_all_open_orders()

    # 获取目前所有的持仓基础函数
    def get_all_positions(self):
        return self._positionManager.get_all_positions()

    # 通过订单id获取某个订单基础函数
    def get_order_by_id(self, instrument_id, order_id):
        return self._orderManager.get_order_by_id(instrument_id, order_id)

    def get_order_by_price(self, instrument_id, side, price):
        return self._orderManager.get_order_by_price(instrument_id, price, side)

    def get_order_by_side(self, instrument_id, side):
        return self._orderManager.get_order_by_side(instrument_id, side)

    def handle_order_update(self, message):
        if "body" in message:
            order_id = message["body"]["order_id"]
            order_status = message["body"]["order_status"]
            instrument_id = message["body"]["instrument_id"]
            log.info(
                "receive order update: order_id: %s, order_status: %s"
                % (order_id, order_status)
            )
            if instrument_id not in self._positionManager.instruments:
                log.warning(f"receive unregistered instrumemt order update: {instrument_id}")
                return

            # QUESION: Will partially filled be pushed earler than new?
            if order_status == ORDER_STATUS_OMS_CREATED:
                # self._positionManager.update_position(instrument_id, message["body"])
                self._orderManager.append_order(instrument_id, message["body"])
            if order_status in [ORDER_STATUS_FILLED, ORDER_STATUS_PARTIALLY_FILLED]:
                # if self._orderManager.remove_order(
                #     message["body"]["instrument_id"], message["body"]["order_id"]
                # ):
                if order_status == ORDER_STATUS_FILLED:
                    self._orderManager.remove_order(instrument_id, order_id)
                else:
                    # 更新已有订单
                    self._orderManager.append_order(instrument_id, message["body"])
                self._positionManager.update_position(
                    instrument_id,
                    message["body"],
                )
            if order_status in [
                ORDER_STATUS_CANCELED,
                ORDER_STATUS_REJECTED,
                ORDER_STATUS_EXPIRED,
                ORDER_STATUS_OMS_PLACE_ORDER_FAILED,
            ]:
                self._orderManager.remove_order(instrument_id, order_id)
                self._positionManager.update_position(
                    instrument_id,
                    message["body"],
                )
        else:
            log.error("message: %s" % message)
