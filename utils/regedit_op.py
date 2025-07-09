# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : regedit_op.py
# Time       ：2024/8/2 10:43
# Author     ：author name
# version    ：python 3.9
# Description：
"""
import winreg


def modify_registry_key(key_path, value_name, new_value):
    try:
        # 打开注册表键HKEY_LOCAL_MACHINE
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)

        # 修改键值
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, new_value)

        # 关闭键
        winreg.CloseKey(key)
        print(f"成功修改 {key_path}\\{value_name} 的值为 {new_value}")
    except Exception as e:
        print(f"修改注册表失败: {e}")


if __name__ == '__main__':
    language = ['French', 'German', 'Italian', 'Korean', 'Portuguese', 'Japanese', 'ChineseTrad', 'ChineseSimp',
                'Spanish', 'English','Turkish','Arabic','Polish']
    app_name = ['ERE', 'EVE']
    modify_registry_key(r"SOFTWARE\WOW6432Node\EaseUS\\"+app_name[0], "Language", 'English')
    # modify_registry_key(r"SOFTWARE\EaseUS\\"+app_name[1], "Language", language[0])
