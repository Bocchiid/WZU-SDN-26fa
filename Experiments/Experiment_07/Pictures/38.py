import requests
import json

# 1. 配置基础信息
ODL_IP = "192.168.72.135"  # 如果你虚拟机的IP变了，记得改这里
BASE_URL = f"http://{ODL_IP}:8181/restconf"
AUTH = ('admin', 'admin')
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}
NODE_ID = "openflow:1"

def block_traffic():
    """下发阻断 h1 到 h3 的流表"""
    print(">>> 正在下发阻断流表...")
    url = f"{BASE_URL}/config/opendaylight-inventory:nodes/node/{NODE_ID}/table/0/flow/2"
    body = {
        "flow": [{
            "id": "2",
            "match": {
                "in-port": "1",
                "ethernet-match": {"ethernet-type": {"type": "0x0800"}},
                "ipv4-destination": "10.0.0.3/32"
            },
            "instructions": {
                "instruction": [{
                    "order": 0,
                    "apply-actions": {"action": [{"order": 0, "drop-action": {}}]}
                }]
            },
            "priority": 65535,
            "table_id": "0"
        }]
    }
    response = requests.put(url, json=body, auth=AUTH, headers=HEADERS)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print("阻断流表下发成功！请去 Mininet 里测试 h1 ping h3。")

def restore_traffic():
    """删除流表，恢复通讯"""
    print(">>> 正在删除流表恢复通讯...")
    url = f"{BASE_URL}/config/opendaylight-inventory:nodes/node/{NODE_ID}/table/0"
    response = requests.delete(url, auth=AUTH, headers=HEADERS)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print("流表已删除，通讯已恢复！请去 Mininet 里测试 h1 ping h3。")

def show_flows():
    """查看当前交换机的流表"""
    print(">>> 正在获取当前流表...")
    url = f"{BASE_URL}/operational/opendaylight-inventory:nodes/node/{NODE_ID}/table/0"
    response = requests.get(url, auth=AUTH, headers=HEADERS)
    if response.status_code == 200:
        print("获取成功，当前流表数据如下：")
        # 打印部分 JSON 数据，避免刷屏
        print(json.dumps(response.json(), indent=2, ensure_ascii=False)[:800] + "\n...")
    else:
        print(f"获取失败，状态码: {response.status_code}")

if __name__ == "__main__":
    # 简易操作菜单
    print("请选择操作：")
    print("1. 阻断 h1 到 h3")
    print("2. 恢复通讯（删除流表）")
    print("3. 显示当前流表")
    choice = input("请输入 1/2/3: ")
    
    if choice == '1':
        block_traffic()
    elif choice == '2':
        restore_traffic()
    elif choice == '3':
        show_flows()