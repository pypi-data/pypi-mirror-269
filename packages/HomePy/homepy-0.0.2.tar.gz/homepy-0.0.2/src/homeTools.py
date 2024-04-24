#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-12-22 16:55
# @Author  : Jack
# @File    : homeTools.py

"""
homeTools
"""
import random
import string
from shapely.geometry import Polygon


def getRandomId(length=10):
    """
    生成指定长度的随机字符串

    Args:
        length (int, optional): 字符串长度，默认为10.

    Returns:
        str: 生成的随机字符串.

    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def getBounds(coords):
    """
    计算多边形坐标点的最小边界框。

    Args:
        coords (list[tuple[float, float]]): 多边形坐标点列表，每个坐标点为(x, y)。

    Returns:
        tuple[float, float, float, float]: 最小边界框的左上角和右下角坐标点坐标，
            格式为(left, bottom, right, top)。

    """
    polygon = Polygon(coords)
    return polygon.bounds
