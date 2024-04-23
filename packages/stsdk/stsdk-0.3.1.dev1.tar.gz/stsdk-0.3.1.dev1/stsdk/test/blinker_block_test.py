import time

from blinker import Signal

sleep_signal = Signal("sleep")
started_signal = Signal("test-started")


def sleep_connect(message):
    print("sleep", message)
    time.sleep(10)


def started_connect(message):
    print("started", message)


sleep_signal.connect(sleep_connect)
started_signal.connect(started_connect)

sleep_signal.send("sleep")

while True:
    time.sleep(1)
    started_signal.send("started")
