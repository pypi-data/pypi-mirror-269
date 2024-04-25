# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-app-ui
# FileName:     date_extend.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import typing as t
from datetime import datetime, timedelta

standard_date_format = "%Y-%m-%d %H:%M:%S"

public_holiday_2024 = [
    "2024-04-04",
    "2024-04-05",
    "2024-04-06",
    "2024-05-01",
    "2024-05-02",
    "2024-05-03",
    "2024-05-04",
    "2024-05-05",
    "2024-06-08",
    "2024-06-09",
    "2024-06-10",
    "2024-09-15",
    "2024-09-16",
    "2024-09-17",
    "2024-10-01",
    "2024-10-02",
    "2024-10-03",
    "2024-10-04",
    "2024-10-05",
    "2024-10-06",
    "2024-10-07",
]


def get_trip_year_month_day(date_str: str) -> t.Tuple:
    """携程日历界面头部上的选择区域"""
    trip_dt = datetime.strptime(date_str, standard_date_format)
    current_dt = datetime.now()
    if trip_dt >= current_dt + timedelta(minutes=60):
        year = "{}年".format(trip_dt.year)
        month = "{}月".format(trip_dt.month)
        day = "{}".format(trip_dt.day)
        return year, month, day
    else:
        raise ValueError("航班时间: {} 已失效或接近当前时间: {}".format(
            date_str, current_dt.strftime(standard_date_format)))


def get_datetime_area(date_str: str) -> str:
    dt = datetime.strptime(date_str, standard_date_format)
    # 获取当天的0点时间
    first_time = datetime(dt.year, dt.month, dt.day, 0, 0, 0)
    six_time = datetime(dt.year, dt.month, dt.day, 6, 0, 0)
    twelve_time = datetime(dt.year, dt.month, dt.day, 12, 0, 0)
    eighteen_time = datetime(dt.year, dt.month, dt.day, 18, 0, 0)
    # end_time = datetime(dt.year, dt.month, dt.day, 23, 59, 59)
    if first_time <= dt < six_time:
        return "00:00 - 06:00"
    elif six_time <= dt < twelve_time:
        return "06:00 - 12:00"
    elif twelve_time <= dt < eighteen_time:
        return "12:00 - 18:00"
    else:
        return "18:00 - 24:00"


def is_public_holiday(date_str: str) -> bool:
    """判断是不是中国的法定节假日"""
    if date_str.split(" ")[0] in public_holiday_2024:
        return True
    else:
        return False


def iso_to_standard_datestr(datestr: str, time_zone_step: int) -> str:
    """iso(2024-04-21T04:20:00Z)格式转 标准的时间格式(2024-01-01 00:00:00)"""
    dt_str = "{} {}".format(datestr[:10], datestr[11:-1])
    dt = datetime.strptime(dt_str, standard_date_format)
    dt_step = dt + timedelta(hours=time_zone_step)
    return dt_step.strftime(standard_date_format)


def current_datetime_str() -> str:
    return datetime.now().strftime(standard_date_format)
