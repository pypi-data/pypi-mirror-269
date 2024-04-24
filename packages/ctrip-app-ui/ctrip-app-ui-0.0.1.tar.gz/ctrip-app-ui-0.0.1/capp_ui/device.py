# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-app-ui
# FileName:     device.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from airtest.core.android.constant import TOUCH_METHOD, CAP_METHOD

default_andriod_device = {
    # "device_id": "LMG710N248c5b73", # LG G7
    "device_id": "66J5T19312004724",  # 华为 mate 20
    "device_conn": "android://127.0.0.1:5037/66J5T19312004724?cap_method={}&touch_method={}".format(
        CAP_METHOD.JAVACAP, TOUCH_METHOD.ADBTOUCH
    ),
    "platform": "Android",
    "enable_debug": True
}

default_minicap_device = {
    "device_id": "66J5T19312004724",  # 华为 mate 20
    "device_conn": "android://127.0.0.1:5037/66J5T19312004724?cap_method={}&touch_method={}".format(
        CAP_METHOD.MINICAP, TOUCH_METHOD.ADBTOUCH
    ),
    "platform": "Android",
    "enable_debug": True
}
