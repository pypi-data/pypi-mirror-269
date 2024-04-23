import time
import sys


from stsdk.utils.ali_sls import sls_data

log_store = "st-sdk-log-pre"
topic = "trade-log"
source = "tianjian-pre"


def test_sls():
    start = time.time()
    sls_data.set_project(project="st-sdk-log")  # 设置一次就可以
    log_store = "st-sdk-log-pre"
    topic = "trade-log"
    source = "tianjian-pre"
    contents = [
        ("timestamp", "1709029762.279965"),
        ("order_id", "15qeny11000czf666xda7ha9vlv0g706"),
        ("instrument_id", "EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"),
        ("order_status", "ORDER_STATUS_PARTIALLY_FILLED"),
        ("origin_quantity", "0.15"),
        ("last_filled_quantity", "0.02"),
        ("average_filled_price", "53000"),
        ("mark_price", "53010"),
        ("commission", "0.0018")
    ]
    sls_data.save_sls(log_store, topic, source, contents)
    print(time.time() - start)


def test_sls_read():
    start = time.time()
    sls_data.set_project(project="st-sdk-log")  # 设置一次就可以
    log_store = "st-sdk-log-pre"
    topic = "trade-log"
    from_time = int(time.time()) - 36000000
    to_time = int(time.time())
    res = sls_data.read_sls(log_store, from_time, to_time, topic,
                            '"order_id" = "15qeny11000czf666xda7ha9vlv0g706"', line=1000, offset=0, reverse=True)
    print(len(res))
    for i in res:
        print(i["timestamp"])
        print(i["order_id"])
    print(time.time() - start)



def test_sls_batch():
    start = time.time()
    sls_data.set_project(project="st-sdk-log")  # 设置一次就可以
    log_store = "st-sdk-log-pre"
    topic = "trade-log"
    source = "tianjian-pre"
    batch_list = []
    for i in range(5):
        contents = [
            ("timestamp", "1709029762.279965"),
            ("order_id", "15qeny11000czf666xda7ha9vlv0g706"),
            ("instrument_id", "EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"),
            ("order_status", "ORDER_STATUS_PARTIALLY_FILLED"),
            ("origin_quantity", "0.15"),
            ("last_filled_quantity", "0.02"),
            ("average_filled_price", "53000"),
            ("mark_price", "53010"),
            ("commission", "0.0018")
        ]
        batch_list.append(contents)
    sls_data.save_sls_batch(log_store, topic, source, batch_list)
    end = time.time()
    print("time: ", end - start)


if __name__ == "__main__":
    test_sls()