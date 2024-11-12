import matplotlib.pyplot as plt
import pandas as pd

from src.file.read_csv import analyse_csv_hdf5, analyse_csv_pickle, replace_none_to_zero

"""
每日pv统计、每日uv统计
uv 用户每天访问多次只算为一次
pv 用户每天访问多次累计
"""


def count_uv(data, user_id="user_id", time="time"):
    """
    数据转换
    :param time: 日期
    :param user_id: 用户ID
    :param data: 需要统计的数据
    :return: 行为用户 列为日期 元素内容为pv的数量
    """
    # 新建一列 每个用户的一次访问网站的记录为1次
    data.loc[:, "count"] = 1
    data[time] = pd.to_datetime(data[time]).dt.date
    # 分组
    return data.groupby(data[time])["count"].sum().reset_index()

def count_pv(data, user_id="user_id", time="time"):
    """
    数据转换
    :param data: 数据
    :param user_id: 用户ID
    :param time: 日期
    :return: None
    """
    # 提取出日期部分
    data[time] = pd.to_datetime(data[time]).dt.date
    # 去重
    drop_duplicates_data = data.drop_duplicates(subset=[user_id, time])
    # 对user_id根据日期去重
    drop_duplicates_data.loc[:, "count"] = 1
    return drop_duplicates_data.groupby(drop_duplicates_data[time])["count"].sum().reset_index()


__file_path = "../../file/tianchi_mobile_recommend_train_user.csv"
__file_name = "tianchi_mobile_recommend_train_user"

# 读取文件
csv_data = analyse_csv_pickle(__file_path, __file_name)
user_id_and_time = csv_data.loc[:,["user_id", "time"]]

# 统计pv
grouped_by_time_pv = count_uv(user_id_and_time)

# 统计uv
grouped_by_time_uv = count_pv(user_id_and_time)

# 创建画布，指定子图的布局
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # 1 行 2 列的子图

# 绘制 UV 图
ax1.plot(grouped_by_time_uv['time'], grouped_by_time_uv['count'], linestyle='--', color='g')
ax1.set_title("每日 UV 统计")
ax1.set_xlabel("日期")
ax1.set_ylabel("UV 数量")

# 绘制 PV 图
ax2.plot(grouped_by_time_pv['time'], grouped_by_time_pv['count'], linestyle='--', color='b')
ax2.set_title("每日 PV 统计")
ax2.set_xlabel("日期")
ax2.set_ylabel("PV 数量")

# 自动调整子图间距
plt.tight_layout()

# 显示图形
plt.show()