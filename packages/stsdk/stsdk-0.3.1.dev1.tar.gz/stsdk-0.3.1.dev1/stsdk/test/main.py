import asyncio
import sys

sys.path.append("/root/lingxiao/st-sdk/")
sys.path.append("/root/lingxiao/st-sdk/stsdk")

from stsdk.utils.http import Request

# 使用示例


async def main():
    req = Request()
    json = await req.get(
        "http://47.91.17.20:5001/v1/klines/spot",
        params={
            "exchange": 1,
            "symbol": "BTCUSDT",
            "interval": "1s",
            "start_time": 0,
            "limit": 10,
        },
    )
    print(json)
    await req.close()


asyncio.run(main())
