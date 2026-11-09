import tkinter as tk
from tkinter import messagebox
import csv
import requests

# 基础配置
ODL_IP = "192.168.72.135"  
BASE_URL = f"http://{ODL_IP}:8181/restconf"
AUTH = ('admin', 'admin')
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}
NODE = "openflow:1"

def apply_firewall():
    """读取 CSV 规则并下发流表"""
    try:
        with open('firewall-policies.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row: continue
                rule_id, src_mac, dst_mac = row[0].strip(), row[1].strip(), row[2].strip()
                
                # 构造流表 JSON（匹配源和目的 MAC，动作为丢弃）
                body = {
                    "flow": [{
                        "id": str(rule_id),
                        "match": {
                            "ethernet-match": {
                                "ethernet-source": {"address": src_mac},
                                "ethernet-destination": {"address": dst_mac}
                            }
                        },
                        "instructions": {
                            "instruction": [{
                                "order": 0,
                                "apply-actions": {
                                    "action": [{"order": 0, "drop-action": {}}]
                                }
                            }]
                        },
                        "priority": 65535,
                        "table_id": "0"
                    }]
                }
                
                url = f"{BASE_URL}/config/opendaylight-inventory:nodes/node/{NODE}/table/0/flow/{rule_id}"
                requests.put(url, json=body, auth=AUTH, headers=HEADERS)
        messagebox.showinfo("成功", "防火墙规则已成功下发！")
    except Exception as e:
        messagebox.showerror("错误", f"下发失败: {e}")

def clear_rules():
    """清空流表，恢复通讯"""
    try:
        url = f"{BASE_URL}/config/opendaylight-inventory:nodes/node/{NODE}/table/0"
        requests.delete(url, auth=AUTH, headers=HEADERS)
        messagebox.showinfo("成功", "防火墙规则已清除，网络已恢复！")
    except Exception as e:
        messagebox.showerror("错误", f"清除失败: {e}")

# 构建 GUI 界面
root = tk.Tk()
root.title("ODL 防火墙控制台")
root.geometry("320x200")

tk.Label(root, text="OpenDaylight 防火墙", font=("Arial", 14, "bold")).pack(pady=15)

tk.Button(root, text="应用防火墙规则 (阻断)", command=apply_firewall, width=25, bg="lightcoral").pack(pady=5)
tk.Button(root, text="清除规则 (恢复通信)", command=clear_rules, width=25, bg="lightgreen").pack(pady=5)

root.mainloop()