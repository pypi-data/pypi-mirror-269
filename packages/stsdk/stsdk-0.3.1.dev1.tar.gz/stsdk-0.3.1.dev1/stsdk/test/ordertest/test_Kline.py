import json
import time
from datetime import datetime

import pandas as pd  # 引入pandas进行数据处理和保存
import requests


def get_data(url, params):
    request_time = time.time()
    response = requests.get(url=url, params=params)
    response_time = time.time()
    latency = round((response_time - request_time) * 1000, 2)
    data = json.loads(response.text)
    return data, request_time, response_time, latency


def verify_data(data, request_time, response_time):
    if not all(len(kline) == 13 for kline in data):
        return False, "数据结构不匹配", None
    if not data[-2][-1]:
        return False, "倒数第二根k线应该是关闭状态", {"isclosed": data[-2][-1]}
    last_kline_closed = data[-1][-1]
    last_update_close_time = data[-1][7] / 1000
    close_time = data[-1][6] / 1000
    if last_kline_closed and (last_update_close_time != close_time):
        return False, "最后一根k线的关闭状态不匹配", {"last_kline_closed": last_kline_closed,
                                                      "last_update_close_time": last_update_close_time,
                                                      "close_time": close_time}
    for i in range(len(data) - 1):
        if data[i + 1][0] != data[i][6] + 1:
            return False, "k线时间不连续", {"current_open_time": data[i + 1][0], "previous_close_time": data[i][6]}

    if not (request_time - 60 <= last_update_close_time <= response_time + 60):
        time_diff_request = request_time - last_update_close_time  # 与请求时间的差异
        time_diff_response = last_update_close_time - response_time  # 与响应时间的差异

        return False, "最后一根k线的最后更新关闭时间不在预期范围内", {
            "last_update_close_time": datetime.fromtimestamp(last_update_close_time).strftime('%Y-%m-%d %H:%M:%S'),
            "request_time": datetime.fromtimestamp(request_time).strftime('%Y-%m-%d %H:%M:%S'),
            "time_diff_request_sec": time_diff_request,
            "time_diff_response_sec": time_diff_response,
            "request_time_range": (
                request_time - 60, response_time + 60)}
    return True, "数据验证通过", {
        "last_update_close_time": datetime.fromtimestamp(last_update_close_time).strftime('%Y-%m-%d %H:%M:%S'),
        "request_time": datetime.fromtimestamp(request_time).strftime('%Y-%m-%d %H:%M:%S')}


def test_continuity_and_repeated_requests(instrument_ls, kline_intervals, window_size):
    results = []
    pre_url = "http://13.115.30.37:5001/v1/klines/instrument"
    test_url = "http://43.207.106.154:5001/v1/klines/instrument"
    for interval in kline_intervals:
        for instrument in instrument_ls:
            params = {
                "instrument_id": f"EXCHANGE_BINANCE.{instrument.upper()}-USDT.SECURITY_TYPE_SPOT.UNSPECIFIED.UNSPECIFIED.UNSPECIFIED",
                "interval": interval,
                "limit": window_size
            }
            first_data, first_request_time, first_response_time, latency = get_data(test_url, params)
            success, message, failed_values = verify_data(first_data, first_request_time, first_response_time)
            result = {
                "Instrument": instrument,
                "Interval": interval,
                "Success": success,
                "Message": message,
                "Latency(ms)": latency,
                "Values": failed_values if failed_values else "N/A"
            }
            print(result)
            results.append(result)
            # time.sleep(1)  # 避免过快的请求速度

    return results


def save_results_to_excel(results, filename_prefix="test_results"):
    # 获取当前时间并格式化为简短时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.xlsx"

    # 使用pandas创建DataFrame
    df = pd.DataFrame(results)

    # 保存到Excel文件
    df.to_excel(filename, index=False)
    print(f"Results saved to {filename}")


def main():
    instrument_ls = [
        "BTC", "ETH", "XRP", "BNB", "SOL", "DOGE", "MATIC", "ADA", "SHIB",
        "ETC", "LTC", "AVAX", "OP", "FTM", "LINK", "FIL", "GALA", "CHZ",
        "TRX", "DOT", "APE", "NEAR", "ATOM", "GMT", "EUR", "CFX", "SAND",
        "LUNA", "LDO", "DYDX"
    ]
    kline_intervals = ["1m", "3m", "5m", "15m", "30m", "6h", "12h", "1d"]
    window_size = 25

    results = test_continuity_and_repeated_requests(instrument_ls, kline_intervals, window_size)
    save_results_to_excel(results)


if __name__ == "__main__":
    main()
