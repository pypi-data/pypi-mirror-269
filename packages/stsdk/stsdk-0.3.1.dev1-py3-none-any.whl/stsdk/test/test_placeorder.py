import aiohttp
import asyncio

async def make_post_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.json()

async def main():
    url = 'http://47.91.17.20:4000/order/new'
    data = {"strategy_id": "17", "account_id": "test-future", "quantity": "0.03", "price": "1000",
            "instrument_id": "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
            "position_side": 3, "contract_type": 2, "order_type": 2, "order_direction": 1, "time_in_force": 1,
            "leverage": 2}

    response = await make_post_request(url, data)
    print(response)

# 运行异步函数
asyncio.run(main())
