import requests

RYU_URL = "http://192.168.72.135:8080"
DPID = 1

def add_flow():
    url = f"{RYU_URL}/stats/flowentry/add"
    data = {
        "dpid": DPID, "priority": 300,
        "match": {"in_port": 1, "eth_type": 2048, "ipv4_dst": "10.0.0.2/32"},
        "actions": []
    }
    res = requests.post(url, json=data)
    print(f"✅ 1. 添加丢包流表成功，状态码: {res.status_code}")

def modify_flow():
    url = f"{RYU_URL}/stats/flowentry/modify"
    data = {
        "dpid": DPID, "priority": 300,
        "match": {"in_port": 1, "eth_type": 2048, "ipv4_dst": "10.0.0.2/32"},
        "actions": [{"type": "OUTPUT", "port": 2}]
    }
    res = requests.post(url, json=data)
    print(f"✅ 2. 修改流表动作成功，状态码: {res.status_code}")

def delete_flow():
    url = f"{RYU_URL}/stats/flowentry/delete"
    data = {
        "dpid": DPID, "priority": 300,
        "match": {"in_port": 1, "eth_type": 2048, "ipv4_dst": "10.0.0.2/32"}
    }
    res = requests.post(url, json=data)
    print(f"✅ 3. 删除流表成功，状态码: {res.status_code}")

if __name__ == "__main__":
    while True:
        print("\n" + "="*40)
        print("请选择操作: 1.添加阻断  2.修改为转发  3.直接删除")
        print("="*40)
        choice = input("请输入 [1-3, 0退出]: ")
        if choice == '1': add_flow()
        elif choice == '2': modify_flow()
        elif choice == '3': delete_flow()
        elif choice == '0': break