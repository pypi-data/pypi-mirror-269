import traceback

import websocket

from stsdk.utils.log import log


class Websocket:
    def __init__(self, url):
        self.ws = None
        self.url = url
        self.sub_keys = set()

    def registerEvent(self, sub_key):
        log.info(sub_key)
        self.sub_keys.add(sub_key)

    def run(self, consumer):
        log.info("Websocket connecting...")

        def handle_message(ws, message):
            consumer(message)

        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=handle_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

        self.ws.run_forever(reconnect=5)

    def on_open(self, ws):
        log.info("Websocket connection opened")
        for payload in self.sub_keys:
            self.ws.send(payload)

    def on_close(self, ws, close_status_code, close_msg):
        log.info("Websocket connection closed")
        ws.close()

    def on_error(self, ws, error):
        log.error(f"Websocket error received: {error}, ws url: {self.url}")
        log.error("Detailed error information:")
        log.error(traceback.format_exc())
