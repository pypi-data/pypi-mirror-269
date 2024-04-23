from stsdk.utils.instrument_id import expand_topic

params = {"name": "1"}

name1 = params.get("name1")
name2 = params.get("name", "2")
print(name1)
print(name2)
print(name1 is None)


topic_type = expand_topic(
    "bbo.EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
)
print(topic_type)
