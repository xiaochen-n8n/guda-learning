#! /usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
import os
import shutil
import platform
import json
import requests
import psutil

#hostname
def get_hostname():
    hostname = platform.node()
    return hostname

#ip
def get_ip():
    """获取本机IP地址"""
    try:
        # 获取本机IP地址
        hostname = socket.gethostname()
        ipaddr = socket.gethostbyname(hostname)
        return ipaddr
    except Exception as e:
        # 如果上述方法失败，尝试连接外部地址来获取本机IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ipaddr = s.getsockname()[0]
            s.close()
            return ipaddr
        except:
            return "127.0.0.1"

#cpu
def get_cpu():
    """获取CPU信息"""
    try:
        # 获取CPU物理核心数
        cpu_count = psutil.cpu_count(logical=False)
        # 获取CPU逻辑核心数
        cpu_count_logical = psutil.cpu_count(logical=True)
        # 获取CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        
        cpu_info = {
            'physical_cores': cpu_count,
            'logical_cores': cpu_count_logical,
            'usage_percent': cpu_percent
        }
        return cpu_info
    except Exception as e:
        return {'error': str(e)}

#mem
def get_mem():
    """获取内存信息"""
    try:
        # 获取内存信息
        memory = psutil.virtual_memory()
        
        mem_info = {
            'total_gb': round(memory.total / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2),
            'used_gb': round(memory.used / (1024**3), 2),
            'usage_percent': memory.percent
        }
        return mem_info
    except Exception as e:
        return {'error': str(e)}

#disk
def get_disk():
    try:
        drive = os.environ.get('SystemDrive')
        if not drive:
            system_root = os.environ.get('SystemRoot')
            if system_root:
                drive = os.path.splitdrive(system_root)[0]
        if not drive:
            drive = os.path.splitdrive(sys.executable)[0]
        if not drive:
            drive = os.path.splitdrive(os.getcwd())[0]
        root = drive + '\\'
        usage = shutil.disk_usage(root)
        return {
            'drive': drive,
            'total_gb': round(usage.total / (1024**3), 2),
            'used_gb': round(usage.used / (1024**3), 2),
            'free_gb': round(usage.free / (1024**3), 2),
            'usage_percent': round((usage.used / usage.total) * 100, 2)
        }
    except Exception as e:
        return {'error': str(e)}

def all_data():
    """收集所有系统信息"""
    asset_info = dict()
    asset_info['hostname'] = get_hostname()
    asset_info['ip'] = get_ip()
    asset_info['cpu'] = get_cpu()
    asset_info['mem'] = get_mem()
    asset_info['disk'] = get_disk()
    asset_info['desc'] = f"Windows 11 Agent - {platform.system()} {platform.release()}"
    return json.dumps(asset_info, ensure_ascii=False)

def post_data(url, data):
    """发送数据到服务器"""
    try:
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=data, headers=headers, timeout=30)
        print(f"状态码: {r.status_code}")
        if r.status_code == 200:
            print("数据发送成功!")
        else:
            print(f"发送失败: {r.text}")
        return r.status_code
    except requests.exceptions.RequestException as e:
        print(f"网络错误: {e}")
        return None

if __name__ == "__main__":
    print("Windows 11 系统监控Agent启动...")
    print("正在收集系统信息...")
    
    # 收集数据
    data = all_data()
    print("系统信息收集完成!")
    print(f"数据内容: {data}")
    
    # 发送数据
    print("正在发送数据到服务器...")
    result = post_data("http://localhost:8000/collect/", data)
    
    if result == 200:
        print("监控数据上报成功!")
    else:
        print("监控数据上报失败!")