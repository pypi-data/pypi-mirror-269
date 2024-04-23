from typing import Dict, Tuple
from stsdk.api.http.dms import DMSApi


def get_instrument_info(
    symbol: str = None,
    exchange: str = None,
    security_type: str = None,
    contract_type: str = None,
    external_symbol: str = None,
    expiry_date:str = None
) -> Dict:
    params = {
        "symbol": symbol,
        "exchange": exchange,
        "security_type": security_type,
        "contract_type": contract_type,
        "external_symbol": external_symbol,
    }
    resp = DMSApi().get_instrument_info(params)
    configs = resp["instruments"][0]["symbol_infos"]
    if expiry_date:
        for c in configs:
            if c["expiry_date"] == expiry_date:
                return [c]     
    return configs

def instrumentId_decode(instrumentId: str) -> Tuple[str, str, str, str, str]:
    exchange, symbol, sec_type, ct_type, st_ccy, ex_date = instrumentId.split(".")
    return exchange, symbol, sec_type, ct_type, st_ccy, ex_date


class EXCHANGE:
    UNSPECIFIED = "EXCHANGE_UNSPECIFIED"
    BINANCE = "EXCHANGE_BINANCE"
    OKEX = "EXCHANGE_OKEX"
    COINBASE = "EXCHANGE_COINBASE"
    DERIBIT = "EXCHANGE_DERIBIT"


class INSTRUMENT_TYPE:
    UNSPECIFIED = "SECURITY_TYPE_UNSPECIFIED"
    SPOT = "SECURITY_TYPE_SPOT"
    PERP = "SECURITY_TYPE_PERP"
    FUTURE = "SECURITY_TYPE_FUTURE"
    OPTION = "SECURITY_TYPE_OPTION"


class CONTRACT_TYPE:
    UNSPECIFIED = "CONTRACT_TYPE_UNSPECIFIED"
    INVERSE = "CONTRACT_TYPE_INVERSE"
    LINEAR = "CONTRACT_TYPE_LINEAR"


class CURRENCY:
    UNSPECIFIED = "UNSPECIFIED"
    CNY = "CNY"
    # for crypto
    USDT = "USDT"
    BTC = "BTC"
    ETH = "ETH"


class INSTRUMENT_CLASS:
    CRYPTO = "crypto"


class Instrument:
    SUPPORT_INSTRUMENT_TYPE = [
        INSTRUMENT_TYPE.SPOT,
        INSTRUMENT_TYPE.PERP,
        INSTRUMENT_TYPE.FUTURE,
    ]
    """
    This is a priceable object representing a generic security
    Instrument ID is available after initialize, other information will be available after build.
    """
    CM_MAKER_FEE = 0.0
    CM_TAKER_FEE = 0.000192
    UM_MAKER_FEE = -0.00004
    UM_TAKER_FEE = 0.000147

    def __init__(
        self,
        symbol: str,
        exchange: EXCHANGE,
        instrument_type: INSTRUMENT_TYPE,
        contract_type: CONTRACT_TYPE,
        settlement_ccy: CURRENCY,
        expiry_date: str = "UNSPECIFIED",
    ):
        if instrument_type not in self.SUPPORT_INSTRUMENT_TYPE:
            raise Exception(f"{instrument_type} is not supported")
        self._symbol = str(symbol)
        self._exchange = exchange
        self._contract_type = contract_type
        self._instrument_type = instrument_type
        self._expiry_date = expiry_date
        self._settlement_ccy = settlement_ccy
        self._instrument_id = f"{exchange}.{symbol}.{instrument_type}.{contract_type}.{settlement_ccy}.{expiry_date}"
        self._instrument_class = INSTRUMENT_CLASS.CRYPTO

        # below info is set when building security
        self._is_built = False
        self._tick_size = ...
        self._contract_multipl = ...
        self._base_ccy = ...
        self._quote_ccy = ...
        self._qty_unit = ...
        self._min_notional = ...
        self._info = {}  # all information return by dms query api

    def build(self):
        """
        We only build the instrument when we want to access it information which is not contained in instrument in.
        """
        self._info = get_instrument_info(
            symbol=self._symbol,
            exchange=self._exchange,
            security_type=self._instrument_type,
            contract_type=self._contract_type,
            expiry_date = self._expiry_date
        )[0]
        self._instrument_id = self._info["instrument_id"]
        self._tick_size = float(self._info["price_tick_size"])
        self._contract_multipl = float(self._info.get("contract_size", 1))
        self._settlement_ccy = self._info["settle_ccy"]
        self._qty_unit = float(self._info["limit_min_quantity"])
        self._min_notional = float(self._info.get("notional_filter", {}).get("min_notional", 0))
        if self._qty_unit == 0:
            raise ValueError(
                f"got qty_unit == {0} when building instrument fron DMS, the instrument info is: \n {self._info}"
            )
        if self._min_notional == 0 and self._contract_type != CONTRACT_TYPE.INVERSE:
            raise ValueError(
                f"got min_notional == {0} when building instrument fron DMS, the instrument info is: \n {self._info}"
            )
        self._base_ccy = self._info["base_ccy"]
        self._quote_ccy = self._info["quote_ccy"]

    @classmethod
    def gen_by_instrumentId(cls, instrumentId: str):
        ex, sy, sec, ct, st_ccy, ex_dt = instrumentId_decode(instrumentId)
        return cls(sy, ex, sec, ct, st_ccy, ex_dt)

    @property
    def symbol(self):
        return self._symbol

    @property
    def exchange(self):
        return self._exchange

    @property
    def contract_type(self):
        return self._contract_type

    @property
    def instrument_type(self):
        return self._instrument_type

    @property
    def instrument_id(self) -> str:
        return self._instrument_id

    @property
    def contract_multipl(self):
        if self._contract_multipl == 0:
            return 1.0
        return self._contract_multipl

    @property
    def tick_size(self):
        return self._tick_size

    @property
    def underl_instrumentId(self):
        return self._settlement_ccy

    @property
    def qty_unit(self):
        # if self._qty_unit == 0:
        #     return 1.0
        return self._qty_unit

    @property
    def min_notional(self):
        return self._min_notional

    @property
    def contract_type(self):
        return self._contract_type

    @property
    def instrument_class(self):
        return self._instrument_class

    def __eq__(self, other):
        return other.instrument_id == self.instrument_id

    def __neg__(self, other):
        return not self.__eq__(other=other)

    def __str__(self):
        return self.instrument_id

    def __repr__(self) -> str:
        return self.instrument_id

    def calculate_unit_margin(self, price: float, *args, **kwargs):
        if (
            self._contract_type == CONTRACT_TYPE.LINEAR
            or self._instrument_type == INSTRUMENT_TYPE.SPOT
        ):
            return price
        elif self._contract_type == CONTRACT_TYPE.INVERSE:
            return self._contract_multipl / price
        else:
            raise Exception(f"{self._contract_type} is not supported")

    def calc_unit_commission(
        self, price: float, is_maker: bool = True, *args, **kwargs
    ):
        if self._contract_type == CONTRACT_TYPE.INVERSE:
            fee_rate = self.CM_MAKER_FEE if is_maker else self.CM_TAKER_FEE
        else:
            fee_rate = self.UM_MAKER_FEE if is_maker else self.UM_TAKER_FEE
        if (
            self._contract_type == CONTRACT_TYPE.LINEAR
            or self._instrument_type == INSTRUMENT_TYPE.SPOT
        ):
            return price * fee_rate
        elif self._contract_type == CONTRACT_TYPE.INVERSE:
            return fee_rate * self._contract_multipl / price
        else:
            raise Exception(f"{self._contract_type} is not supported")

    def calc_cash_change(self, trade_price: float, qty: float):
        if (
            self._contract_type == CONTRACT_TYPE.LINEAR
            or self.instrument_type == INSTRUMENT_TYPE.SPOT
        ):
            return trade_price * qty
        elif self._contract_type == CONTRACT_TYPE.INVERSE:
            return qty * self.contract_multipl / trade_price
        else:
            raise Exception(f"{self._contract_type} is not supported")


class EuropeanOption(Instrument):
    # TODO: a reminder, instrument object for options is to be finished

    def calc_unit_commission(
        self, price: float, is_maker: bool = True, *args, **kwargs
    ):
        raise NotImplementedError

    def calc_cash_change(self, trade_price: float, qty: float):
        raise NotImplementedError
