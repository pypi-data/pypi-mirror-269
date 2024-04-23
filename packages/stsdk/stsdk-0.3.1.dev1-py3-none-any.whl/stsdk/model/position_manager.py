from typing import Dict
from loguru import logger
import stsdk.utils.precision as prec
from stsdk.api.http.oms import OMSApi
from stsdk.common.exception import InstrumentNotRegisteredException
from stsdk.common.key import (
    ORDER_DIRECTION_BUY_STR,
    ORDER_DIRECTION_SELL_STR,
    ORDER_STATUS_CANCELED,
    ORDER_STATUS_EXPIRED,
    ORDER_STATUS_FILLED,
    ORDER_STATUS_OMS_CREATED,
    ORDER_STATUS_OMS_PLACE_ORDER_FAILED,
    ORDER_STATUS_PARTIALLY_FILLED,
    ORDER_STATUS_REJECTED,
    POSITION_SIDE_LONG_STR,
    POSITION_SIDE_NOTBOTH_STR,
    POSITION_SIDE_SHORT_STR, EXCHANGE_BINANCE, CONTRACT_TYPE_LINEAR,
)
from stsdk.model.instrument import Instrument
import stsdk.utils.precision as prec

class PositionModule(object):
    def __init__(
            self,
            qty_unit:float, 
            long_filled=0.0,
            long_outstanding=0.0,
            short_filled=0.0,
            short_outstanding=0.0,
    ):
        self.qty_unit = qty_unit
        self.long_filled = long_filled
        self.long_outstanding = long_outstanding
        self.short_filled = short_filled
        self.short_outstanding = short_outstanding

    def __str__(self):
        return (
            f"long_filled: {self.long_filled}, "
            f"long_outstanding: {self.long_outstanding}, "
            f"short_filled: {self.short_filled}, "
            f"short_outstanding: {self.short_outstanding}"
        )
        
    @property
    def net_position(self):
        return prec.substract(self.long_filled, self.short_filled, self.qty_unit)

    @property
    def net_outstanding_qty(self):
        return prec.substract(self.long_outstanding, self.short_outstanding, self.qty_unit)
    
    @property
    def tot_net_position(self):
        return prec.substract(prec.add(self.long_filled, self.long_outstanding, self.qty_unit), prec.add(self.short_filled, self.short_outstanding, self.qty_unit), self.qty_unit)

    def clear(self):
        self.long_filled = 0.0
        self.long_outstanding = 0.0
        self.short_filled = 0.0
        self.short_outstanding = 0.0

    def record_position(self, position_info):
        """
        position management in PositionModule
        :param position_info, a dictionary with keys as position_record_header
        :return:
        """
        pass


class InverseContractPositionModule(PositionModule):
    def __init__(
            self, qty_unit, long_filled=0, long_outstanding=0, short_filled=0, short_outstanding=0
    ):
        self._coin_long_filled = 0.0
        self._coin_short_filled = 0.0
        super().__init__(qty_unit, long_filled, long_outstanding, short_filled, short_outstanding)

    def __str__(self):
        return (
            f"long_filled: {self.long_filled}, "
            f"long_outstanding: {self.long_outstanding}, "
            f"short_filled: {self.short_filled}, "
            f"short_outstanding: {self.short_outstanding}, "
            f"long_coin_filled: {self._coin_long_filled}, "
            f"short_coin_filled: {self._coin_short_filled}"
        )

    @property
    def coin_net_position(self):
        return prec.substract(self._coin_long_filled, self._coin_short_filled, self.qty_unit)

    def clear(self):
        self._coin_long_filled = 0.0
        self._coin_short_filled = 0.0
        return super().clear()


class PositionManager(object):
    def __init__(self, strategy_id, account_id):
        self.positions: Dict[str, PositionModule] = dict()
        self.omsApi = OMSApi()
        self.instruments: Dict[str, Instrument] = dict()
        self.strategy_id = strategy_id
        self.account_id = account_id
        self.active_long_closing_quota: Dict[str, float] = dict()
        self.active_short_closing_quota: Dict[str, float] = dict()
        self.active_long_opening_quota: Dict[str, float] = dict()
        self.active_short_opening_quota: Dict[str, float] = dict()

    def register_instrument(
            self, instrumentId, long_opening_quota: float, short_opening_quota: float, 
            long_closing_quota:float = 0.0, short_closing_quota:float = 0.0
    ):
        instrument = Instrument.gen_by_instrumentId(instrumentId)
        instrument.build()
        self.instruments[instrumentId] = instrument
        self.positions[instrumentId] = PositionModule(instrument.qty_unit)
        self.active_long_opening_quota[instrumentId] = long_opening_quota
        self.active_short_opening_quota[instrumentId] = short_opening_quota
        self.active_long_closing_quota[instrumentId] = long_closing_quota
        self.active_short_closing_quota[instrumentId] = short_closing_quota

    def get_instrument(self, instrument_id):
        return self.instruments[instrument_id]

    def update_place_order(self, instrument_id: str, op_info: Dict):
        position = self.positions[instrument_id]
        instrument = self.instruments[instrument_id]
        orig_qty = float(op_info["origin_quantity"])
        position_side = op_info["position_side"]
        if op_info["order_direction"] == ORDER_DIRECTION_BUY_STR:
            position.long_outstanding = prec.add(
                position.long_outstanding, orig_qty, instrument.qty_unit
            )
            if position_side == POSITION_SIDE_NOTBOTH_STR:
                self.active_long_closing_quota[instrument_id] = position.long_filled + position.long_outstanding
                # size = orig_qty
                # if self.active_short_closing_quota[instrument_id] > 0:
                #     _update_size = min(
                #         self.active_short_closing_quota[instrument_id], size
                #     )
                #     self.active_short_closing_quota[instrument_id] = prec.substract(
                #         self.active_short_closing_quota[instrument_id],
                #         _update_size,
                #         instrument.qty_unit,
                #     )
                #     self.active_short_opening_quota[instrument_id] = prec.add(
                #         self.active_short_opening_quota[instrument_id],
                #         _update_size,
                #         instrument.qty_unit,
                #     )
                #     size = prec.substract(size, _update_size, instrument.qty_unit)
                # if size > 0:
                #     self.active_long_opening_quota[instrument_id] = prec.substract(
                #         self.active_long_opening_quota[instrument_id],
                #         size,
                #         instrument.qty_unit,
                #     )
                #     self.active_long_closing_quota[instrument_id] = prec.add(
                #         self.active_long_closing_quota[instrument_id],
                #         size,
                #         instrument.qty_unit,
                #     )
            elif position_side == POSITION_SIDE_LONG_STR:
                self.active_long_opening_quota[instrument_id] = prec.substract(
                    self.active_long_opening_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
                self.active_long_closing_quota[instrument_id] = prec.add(
                    self.active_long_closing_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
            elif position_side == POSITION_SIDE_SHORT_STR:
                self.active_short_opening_quota[instrument_id] = prec.add(
                    self.active_short_opening_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
                self.active_short_closing_quota[instrument_id] = prec.substract(
                    self.active_short_closing_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
        elif op_info["order_direction"] == ORDER_DIRECTION_SELL_STR:
            position.short_outstanding = prec.add(
                position.short_outstanding, orig_qty, instrument.qty_unit
            )
            size = orig_qty
            if position_side == POSITION_SIDE_NOTBOTH_STR:
                if self.active_long_closing_quota[instrument_id] > 0:
                    _update_size = min(
                        self.active_long_closing_quota[instrument_id], size
                    )
                    self.active_long_closing_quota[instrument_id] = prec.substract(
                        self.active_long_closing_quota[instrument_id],
                        _update_size,
                        instrument.qty_unit,
                    )
                    self.active_long_opening_quota[instrument_id] = prec.add(
                        self.active_long_opening_quota[instrument_id],
                        _update_size,
                        instrument.qty_unit,
                    )
                    size = prec.substract(size, _update_size, instrument.qty_unit)
                if size > 0:
                    self.active_short_opening_quota[instrument_id] = prec.substract(
                        self.active_short_opening_quota[instrument_id],
                        size,
                        instrument.qty_unit,
                    )
                    self.active_short_closing_quota[instrument_id] = prec.add(
                        self.active_short_closing_quota[instrument_id],
                        size,
                        instrument.qty_unit,
                    )
            elif position_side == POSITION_SIDE_LONG_STR:
                self.active_long_closing_quota[instrument_id] = prec.substract(
                    self.active_long_closing_quota[instrument_id],
                    size,
                    instrument.qty_unit,
                )
                self.active_long_opening_quota[instrument_id] = prec.add(
                    self.active_long_opening_quota[instrument_id],
                    size,
                    instrument.qty_unit,
                )
            elif position_side == POSITION_SIDE_SHORT_STR:
                self.active_short_closing_quota[instrument_id] = prec.add(
                    self.active_short_closing_quota[instrument_id],
                    size,
                    instrument.qty_unit,
                )
                self.active_short_opening_quota[instrument_id] = prec.substract(
                    self.active_short_opening_quota[instrument_id],
                    size,
                    instrument.qty_unit,
                )
    
    def update_rejected_order(self, instrument_id: str, op_info:Dict):
        instrument = self.instruments[instrument_id]
        orig_qty = float(op_info["origin_quantity"])
        position_side = op_info["position_side"]
        direction = op_info["order_direction"]
        position = self.positions[instrument_id]
        if direction == ORDER_DIRECTION_BUY_STR:
            position.long_outstanding = prec.substract(
                position.long_outstanding, orig_qty, instrument.qty_unit
            )
            if position_side == POSITION_SIDE_NOTBOTH_STR:
                self.active_long_closing_quota = prec.add(position.long_filled, position.long_outstanding, instrument.qty_unit)
            elif position_side == POSITION_SIDE_LONG_STR:
                self.active_long_closing_quota[instrument_id] = prec.substract(
                    self.active_long_closing_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
                self.active_long_opening_quota[instrument_id] = prec.add(
                    self.active_long_opening_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
            elif position_side == POSITION_SIDE_SHORT_STR:
                self.active_short_closing_quota[instrument_id] = prec.add(
                    self.active_short_closing_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
                self.active_short_opening_quota[instrument_id] = prec.substract(
                    self.active_short_opening_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
        elif direction == ORDER_DIRECTION_SELL_STR:
            position.short_outstanding = prec.substract(
                position.short_outstanding, orig_qty, instrument.qty_unit
            )
            if position_side == POSITION_SIDE_NOTBOTH_STR:
                self.active_short_closing_quota[instrument_id] = prec.add(position.short_filled, position.short_outstanding, instrument.qty_unit)
            elif position_side == POSITION_SIDE_LONG_STR:
                self.active_long_closing_quota[instrument_id] = prec.add(
                    self.active_long_closing_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
                self.active_long_opening_quota[instrument_id] = prec.substract(
                    self.active_long_opening_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
            elif position_side == POSITION_SIDE_SHORT_STR:
                self.active_short_closing_quota[instrument_id] = prec.substract(
                    self.active_short_closing_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )
                self.active_short_opening_quota[instrument_id] = prec.add(
                    self.active_short_opening_quota[instrument_id],
                    orig_qty,
                    instrument.qty_unit,
                )

    def update_canceled_position(self, instrument_id: str, op_info: Dict):
        position = self.positions[instrument_id]
        instrument = self.instruments[instrument_id]
        org_qty = float(op_info["origin_quantity"])
        filled_qty = float(op_info["filled_quantity"])
        position_side = op_info["position_side"]
        unfilled_qty = prec.substract(org_qty, filled_qty, instrument.qty_unit)
        if op_info["order_direction"] == ORDER_DIRECTION_BUY_STR:
            position.long_outstanding = prec.substract(
                position.long_outstanding, unfilled_qty, instrument.qty_unit
            )
            if position_side == POSITION_SIDE_NOTBOTH_STR:
                self.active_long_closing_quota = prec.add(position.long_filled, position.long_outstanding)
                # size = unfilled_qty
                # if self.active_short_closing_quota[instrument_id] > 0:
                #     _update_qty = min(
                #         self.active_short_closing_quota[instrument_id], size
                #     )
                #     self.active_short_closing_quota[instrument_id] = prec.add(
                #         self.active_short_closing_quota[instrument_id],
                #         _update_qty,
                #         instrument.qty_unit,
                #     )
                #     self.active_short_opening_quota[instrument_id] = prec.substract(
                #         self.active_short_opening_quota[instrument_id],
                #         _update_qty,
                #         instrument.qty_unit,
                #     )
                #     size = prec.substract(size, _update_qty, instrument.qty_unit)
                # if size > 0:
                #     self.active_long_closing_quota[instrument_id] = prec.substract(
                #         self.active_long_closing_quota[instrument_id],
                #         size,
                #         instrument.qty_unit,
                #     )
                #     self.active_long_opening_quota[instrument_id] = prec.add(
                #         self.active_long_opening_quota[instrument_id],
                #         size,
                #         instrument.qty_unit,
                #     )
            elif position_side == POSITION_SIDE_LONG_STR:
                self.active_long_closing_quota[instrument_id] = prec.substract(
                    self.active_long_closing_quota[instrument_id],
                    unfilled_qty,
                    instrument.qty_unit,
                )
                self.active_long_opening_quota[instrument_id] = prec.add(
                    self.active_long_opening_quota[instrument_id],
                    unfilled_qty,
                    instrument.qty_unit,
                )
            elif position_side == POSITION_SIDE_SHORT_STR:
                self.active_short_closing_quota[instrument_id] = prec.add(
                    self.active_short_closing_quota[instrument_id],
                    unfilled_qty,
                    instrument.qty_unit,
                )
                self.active_short_opening_quota[instrument_id] = prec.substract(
                    self.active_short_opening_quota[instrument_id],
                    unfilled_qty,
                    instrument.qty_unit,
                )
        elif op_info["order_direction"] == ORDER_DIRECTION_SELL_STR:
            position.short_outstanding = prec.substract(
                position.short_outstanding, unfilled_qty, instrument.qty_unit
            )
            if position_side == POSITION_SIDE_NOTBOTH_STR:
                self.active_short_closing_quota = prec.add(position.short_filled, position.short_outstanding, instrument.qty_unit)
                # size = unfilled_qty
                # if self.active_long_closing_quota[instrument_id] > 0:
                #     _update_qty = min(
                #         self.active_long_closing_quota[instrument_id], size
                #     )
                #     self.active_long_closing_quota[instrument_id] = prec.add(
                #         self.active_long_closing_quota[instrument_id],
                #         _update_qty,
                #         instrument.qty_unit,
                #     )
                #     self.active_long_opening_quota[instrument_id] = prec.substract(
                #         self.active_long_opening_quota[instrument_id],
                #         _update_qty,
                #         instrument.qty_unit,
                #     )
                #     size = prec.substract(size, _update_qty, instrument.qty_unit)
                # if size > 0:
                #     self.active_short_closing_quota[instrument_id] = prec.substract(
                #         self.active_short_closing_quota[instrument_id],
                #         size,
                #         instrument.qty_unit,
                #     )
                #     self.active_short_opening_quota[instrument_id] = prec.substract(
                #         self.active_short_opening_quota[instrument_id],
                #         size,
                #         instrument.qty_unit,
                #     )
            elif position_side == POSITION_SIDE_LONG_STR:
                self.active_long_closing_quota[instrument_id] = prec.add(
                    self.active_long_closing_quota[instrument_id],
                    unfilled_qty,
                    instrument.qty_unit,
                )
                self.active_long_opening_quota[instrument_id] = prec.substract(
                    self.active_long_opening_quota[instrument_id],
                    unfilled_qty,
                    instrument.qty_unit,
                )
            elif position_side == POSITION_SIDE_SHORT_STR:
                self.active_short_closing_quota[instrument_id] = prec.substract(
                    self.active_short_closing_quota[instrument_id],
                    unfilled_qty,
                    instrument.qty_unit,
                )
                self.active_short_opening_quota[instrument_id] = prec.add(
                    self.active_short_opening_quota[instrument_id],
                    unfilled_qty,
                    instrument.qty_unit,
                )

    def update_filled_position(self, instrument_id: str, op_info: Dict):
        if instrument_id not in self.positions:
            self.positions[instrument_id] = PositionModule()
        position = self.positions[instrument_id]
        instrument = self.instruments[instrument_id]
        if "status_log" in op_info:
            size = float(op_info["status_log"][-1]["last_filled_qty"])
        else:
            # 当订单被下出后立马成交，不会有status_log
            size = float(op_info["filled_quantity"])
        if op_info["position_side"] == POSITION_SIDE_NOTBOTH_STR:
            if op_info["order_direction"] == ORDER_DIRECTION_BUY_STR:
                position.long_outstanding = prec.substract(
                    position.long_outstanding, size, instrument.qty_unit
                )
                if position.short_filled > 0:
                    _filled_qty = min(size, position.short_filled)
                    position.short_filled = prec.substract(
                        position.short_filled, _filled_qty, instrument.qty_unit
                    )
                    size = prec.substract(size, _filled_qty, instrument.qty_unit)
                if size > 0:
                    position.long_filled = prec.add(
                        position.long_filled, size, instrument.qty_unit
                    )
            elif op_info["order_direction"] == ORDER_DIRECTION_SELL_STR:
                position.short_outstanding = prec.substract(
                    position.short_outstanding, size, instrument.qty_unit
                )
                if position.long_filled > 0:
                    _filled_qty = min(size, position.long_filled)
                    position.long_filled = prec.substract(
                        position.long_filled, _filled_qty, instrument.qty_unit
                    )
                    size = prec.substract(size, _filled_qty, instrument.qty_unit)
                if size > 0:
                    position.short_filled = prec.add(
                        position.short_filled, size, instrument.qty_unit
                    )
        elif op_info["position_side"] == POSITION_SIDE_LONG_STR:
            if op_info["order_direction"] == ORDER_DIRECTION_BUY_STR:
                position.long_filled = prec.add(
                    position.long_filled, size, instrument.qty_unit
                )
                position.long_outstanding = prec.substract(
                    position.long_outstanding, size, instrument.qty_unit
                )
            elif op_info["order_direction"] == ORDER_DIRECTION_SELL_STR:
                position.long_filled = prec.substract(
                    position.long_filled, size, instrument.qty_unit
                )
                position.short_outstanding = prec.substract(
                    position.short_outstanding, size, instrument.qty_unit
                )
        elif op_info["position_side"] == POSITION_SIDE_SHORT_STR:
            if op_info["order_direction"] == ORDER_DIRECTION_BUY_STR:
                position.short_filled = prec.substract(
                    position.short_filled, size, instrument.qty_unit
                )
                position.long_outstanding = prec.substract(
                    position.long_outstanding, size, instrument.qty_unit
                )
            elif op_info["order_direction"] == ORDER_DIRECTION_SELL_STR:
                position.short_filled = prec.add(
                    position.short_filled, size, instrument.qty_unit
                )
                position.short_outstanding = prec.substract(
                    position.short_outstanding, size, instrument.qty_unit
                )

    def update_position(self, instrument_id, op_info: Dict):
        if instrument_id not in self.instruments:
            raise InstrumentNotRegisteredException(
                f"instrument {instrument_id} not registered."
            )
        order_status = op_info["order_status"]
        # QUESTION: OMS_CREATED arrive earlier than OMS_NEW?
        if order_status == ORDER_STATUS_OMS_CREATED:
            self.update_place_order(instrument_id, op_info)
        elif order_status in [ORDER_STATUS_PARTIALLY_FILLED, ORDER_STATUS_FILLED]:
            self.update_filled_position(instrument_id, op_info)
        elif order_status in [
            ORDER_STATUS_EXPIRED,
            ORDER_STATUS_CANCELED,
            ORDER_STATUS_REJECTED,
            ORDER_STATUS_OMS_PLACE_ORDER_FAILED,
        ]:
            self.update_canceled_position(instrument_id, op_info)

    def clear_position(self, instrument_id):
        self.positions[instrument_id].clear()

    def get_position(self, instrument_id) -> PositionModule:
        return self.positions.get(instrument_id, PositionModule(self.get_instrument(instrument_id).qty_unit))

    def get_active_long_open_quota(self, instrument_id):
        return self.active_long_opening_quota.get(instrument_id, 0.0)

    def get_active_short_open_quota(self, instrument_id):
        return self.active_short_opening_quota.get(instrument_id, 0.0)

    def get_active_long_close_quota(self, instrument_id):
        return self.active_long_closing_quota.get(instrument_id, 0.0)

    def get_active_short_close_quota(self, instrument_id):
        return self.active_short_closing_quota.get(instrument_id, 0.0)

    def get_all_positions(self):
        return self.positions

    def close_all_positions(self):
        """
        一键平仓
        :return: order list
        """
        data = {
            "strategy_id": self.strategy_id,
            "account_id": self.account_id,
        }
        orders = self.omsApi.close_all_positions(data)
        del self.positions
        return orders

    def sync_position(self):
        """
        同步仓位
        :return: position list
        """
        positions = self.omsApi.get_all_positions()
        for position in positions["positions"]:
            instrument_id = position["instrument_id"]
            if instrument_id not in self.positions:
                self.positions[instrument_id] = PositionModule(self.get_instrument(instrument_id).qty_unit)
            self.positions[instrument_id].long_filled = float(
                position["long_position"]["filled_position"]
            )
            self.positions[instrument_id].long_outstanding = float(
                position["long_position"]["outstanding_position"]
            )
            self.positions[instrument_id].short_filled = float(
                position["short_position"]["filled_position"]
            )
            self.positions[instrument_id].short_outstanding = float(
                position["short_position"]["outstanding_position"]
            )
        return positions

    def get_position_mode(self, contract_type=CONTRACT_TYPE_LINEAR, exchange=EXCHANGE_BINANCE):
        """
        获取仓位模式
        :return: position mode
        """
        params = {
            "exchange": exchange,
            "contract_type": contract_type,
            "account_id": self.account_id,
        }
        position_mode = self.omsApi.get_position_mode(params)
        return position_mode.get("is_both", False)

    def change_position_mode(self, is_both, contract_type=CONTRACT_TYPE_LINEAR, exchange=EXCHANGE_BINANCE):
        """
        修改仓位模式
        :return: position mode
        """
        data = {
            "is_both": is_both,
            "exchange": exchange,
            "contract_type": contract_type,
            "account_id": self.account_id,
        }
        position_mode = self.omsApi.change_position_mode(data)
        return position_mode.get("is_both", False)
