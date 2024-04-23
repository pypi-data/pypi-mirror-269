from blinker import signal

PLACE_ORDER_KEY = "place_order_signal"
CANCEL_ORDER_KEY = "cancel_order_signal"
PLACE_ORDER_SIGNAL = signal(PLACE_ORDER_KEY)
CANCEL_ORDER_SIGNAL = signal(CANCEL_ORDER_KEY)
