def generator_instrument_id(
    exchange, symbol, security_type, contract_type, settle_ccy, expiry_date
):
    instrument_id = f"{exchange}.{symbol}.{security_type}.{contract_type}.{settle_ccy}.{expiry_date}"
    return instrument_id


def expand_instrument_id(instrument_id):
    (
        exchange,
        symbol,
        security_type,
        contract_type,
        settle_ccy,
        expiry_date,
    ) = instrument_id.split(".")
    return {
        "exchange": exchange,
        "symbol": symbol,
        "security_type": security_type,
        "contract_type": contract_type,
        "settle_ccy": settle_ccy,
        "expiry_date": expiry_date,
    }


def expand_topic(topic):
    topic_type = topic.split(".")[0]
    return topic_type
