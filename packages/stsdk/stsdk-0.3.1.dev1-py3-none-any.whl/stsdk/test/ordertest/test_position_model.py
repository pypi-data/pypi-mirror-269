import os

import requests

# 环境配置
ENV = "TEST"  # 或者 "PRODUCTION" 根据需要设置
IP = {"TEST": "43.207.106.154", "PRODUCTION": "43.207.236.155"}[ENV]

# API端点配置
BASE_URL = f"http://{IP}:4000"

def query_position_mode(exchange, contract_type, account_id):
    """查询持仓模式"""
    url = f"{BASE_URL}/account/positionMode"
    params = {
        "exchange": exchange,
        "contract_type": contract_type,
        "account_id": account_id,
    }
    response = requests.get(url, params=params)
    print("查询持仓模式"+response.text)
    return response.json()

def change_position_mode(exchange, contract_type, account_id, is_both):
    """更改持仓模式"""
    url = f"{BASE_URL}/account/positionMode"
    data = {
        "exchange": exchange,
        "contract_type": contract_type,
        "account_id": account_id,
        "is_both": is_both,
    }
    response = requests.post(url, json=data)
    print("更改持仓模式"+response.text)
    return response.json()

# 测试脚本
def test_position_mode():
    exchange = 1
    contract_type = 2
    account_id = "test-future7"

    # 查询当前持仓模式
    current_mode = query_position_mode(exchange, contract_type, account_id)
    print("当前持仓模式:", current_mode)

    # 更改持仓模式
    new_mode = not current_mode['is_both']
    change_result = change_position_mode(exchange, contract_type, account_id, new_mode)
    print("更改持仓模式结果:", change_result)

    # 验证更改后的持仓模式
    verify_mode = query_position_mode(exchange, contract_type, account_id)
    assert verify_mode['is_both'] == new_mode, "持仓模式更改失败"
    print("持仓模式更改验证成功，当前持仓模式:", verify_mode)

if __name__ == "__main__":
    test_position_mode()
