

class OperationException(Exception):
    """
    Exceptions raised by incorrect settings
    which must be handled before the start of the trading session
    """
    pass


class TradingException(Exception):
    """
    Exceptions raised by trading events
    """
    pass

class InstrumentNotRegisteredException(OperationException):
    pass


class OrderPlaceExceedLimit(TradingException):
    pass


class OrderQtyInValid(TradingException):
    pass


class CancelOrderNotFound(TradingException):
    pass


class SelfCrossOrderEncountered(TradingException):
    pass


class DataException(TradingException):
    pass