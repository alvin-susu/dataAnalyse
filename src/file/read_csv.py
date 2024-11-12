import os
import pandas as pd
import matplotlib.pyplot as plt
import logging
import numpy as np

# 解析文件
'''
user_id: 用户id
item_id：商品id
behavior_type：用户行为
    1:点击
    2:收藏
    3:添加购物车
    4:购买	
user_geohash: 用户地理位置hash值
item_category：商品类别
time：时间戳
'''

store = pd.HDFStore('../../file/tianchi.h5')
def analyse_csv_hdf5(file_path, file_name):
    """
    使用hdf5存储解析内容（速度比较慢？）
    :param file_name: 文件名
    :param file_path: 文件路径
    :return: 文件内容
    """

    # 解析文件路径
    if file_path is None:
        raise ValueError("文件路径不能传空！请重试！")

    # 判断缓存是否为空
    try:
        if store[file_name] is not None:
            return store[file_name]
    except KeyError:
        logging.warning("hdfs文件中不存在该file_name的数据")

    csv_data = pd.read_csv(file_path, sep=',')
    if not csv_data.empty:
        # 保存到HDFS文件
        store[file_name] = csv_data
        return csv_data
    return None

def analyse_csv_pickle(file_path, file_name):
    """
    使用二进制存储解析内容
    :param file_path:
    :param file_name:
    :return:
    """
    __file_cache_path = f"../../file/{file_name}"
    # 解析文件路径
    if file_path is None:
        raise ValueError("文件路径不能传空！请重试！")

    # 已经存在缓存则读取缓存
    if os.path.exists(__file_cache_path):
        return pd.read_pickle(__file_cache_path)

    csv_data = pd.read_csv(file_path, sep=',')
    csv_data.to_pickle(__file_cache_path)
    return csv_data

def replace_none_to_zero(data):
    return data.replace({None: np.nan}).fillna(0)