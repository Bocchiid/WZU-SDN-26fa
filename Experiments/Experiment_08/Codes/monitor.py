import requests
import time
import json

RYU_URL = "http://192.168.72.135:8080"

def get_switches():
    return requests.get(f"{RYU_URL}/stats/switches").json()

def get_flow(dpid):
    return requests.get(f"{RYU_URL}/stats/flow/{dpid}").json()

def get_port(dpid):
    return requests.get(f"{RYU_URL}/stats/port/{dpid}").json()

if __name__ == "__main__":
    while True:
        try:
            switches = get_switches()
            print(f"\n[{time.strftime('%H:%M:%S')}] 当前交换机列表: {switches}")
            
            for dpid in switches:
                flow_data = get_flow(dpid)
                port_data = get_port(dpid)
                
                print(f"\n--- 交换机 {dpid} ---")
                print(f"[*] 流表总数量: {len(flow_data[str(dpid)])}")
                
                # 打印前 3 条具体的流表信息（防止终端刷屏）
                print(f"[*] 展示部分流表详情:")
                for flow in flow_data[str(dpid)][:3]:
                    match_info = flow.get('match', {})
                    actions = flow.get('actions', [])
                    packet_count = flow.get('packet_count', 0)
                    priority = flow.get('priority', 0)
                    print(f"    - 优先级:{priority} | 匹配条件:{match_info} | 动作:{actions} | 匹配包数:{packet_count}")
                
                if len(flow_data[str(dpid)]) > 3:
                    print(f"    ... 省略其余 {len(flow_data[str(dpid)]) - 3} 条流表")

                # 打印端口信息
                print(f"[*] 端口状态:")
                for p in port_data[str(dpid)]:
                    if p['port_no'] != 'LOCAL':
                        print(f"    - 端口 {p['port_no']}: RX={p['rx_packets']} 包, TX={p['tx_packets']} 包")
                        
        except Exception as e:
            print("获取数据失败，请检查控制器是否开启或IP是否正确:", e)
            
        time.sleep(5) # 每5秒刷新