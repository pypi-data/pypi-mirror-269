#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : utils.py
@Author  : Gyanano
@Time    : 2023/9/22 14:33
"""
import os
import requests
import platform
import socket


# 获取本机IP地址
def get_ip_address():
    if platform.system() == 'Windows':
        # print(socket.gethostbyname(socket.gethostname()))  # 192.168.123.238 = socket.gethostbyname('Gyan')
        return socket.gethostbyname(socket.gethostname())
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        sock_name = sock.getsockname()[0]
        sock.close()
        return sock_name


# 获取设备信息
def get_device_info():
    device_name = socket.gethostname()
    device_ip = get_ip_address()  # 替换成你的网卡名称
    return {
        'name': device_name,
        'ip': device_ip
    }


def pull_json_config(class_path):
    if os.path.exists(os.path.join(class_path, 'emulator_files')):
        # 说明在blockly运行的，创建对应的gti文件夹
        gti_files_path = os.path.join(class_path, 'gti_files')
        if not os.path.exists(gti_files_path):
            os.mkdir(gti_files_path)
        if not os.path.exists(os.path.join(gti_files_path, 'AppFuncMapClient.json')):
            # 从网络链接中下载客户端配置数据并保存
            url = 'https://gitee.com/gyan71/gti-scnu-file/raw/master/AppFuncMapClient.json'
            res = requests.get(url)
            with open(os.path.join(gti_files_path, 'AppFuncMapClient.json'), 'wb') as f:
                f.write(res.content)
        if not os.path.exists(os.path.join(gti_files_path, 'AppFuncMapServer.json')):
            # 从网络链接中下载服务端配置数据并保存
            url = 'https://gitee.com/gyan71/gti-scnu-file/raw/master/AppFuncMapServer.json'
            res = requests.get(url)
            with open(os.path.join(gti_files_path, 'AppFuncMapServer.json'), 'wb') as f:
                f.write(res.content)

