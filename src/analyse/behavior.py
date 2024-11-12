"""
每日用户行为趋势图
数据包含4个字段，分别是
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
"""
import pandas as pd
from matplotlib import pyplot as plt


from src.common.enum.behavior_enum import Behavior
from src.file.read_csv import analyse_csv_pickle

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

__file_path = "../../file/tianchi_mobile_recommend_train_user.csv"
__file_name = "tianchi_mobile_recommend_train_user"

# 读取文件
csv_data = analyse_csv_pickle(__file_path, __file_name)
behavior_data = csv_data.loc[:, [ "behavior_type", "time"]]

# 提取出日期
behavior_data["time"] = pd.to_datetime(behavior_data["time"]).dt.date

# 定义一个count列，用于统计每个行为类型的数量
behavior_data["count"] = 1

# 用户在某个日期的行为类型数量
behavior_data_group_by_data = behavior_data.groupby([ "time", "behavior_type"])["count"].sum().reset_index()
print(behavior_data_group_by_data)

#  创建一个新的figure
plt.rc('figure', figsize=(20, 10))
figure = plt.figure()
# 只需要一个图
i = 0
# behavior_data_group_by_data.groupby("behavior_type")是为了逐个提取不同的 behavior_type 行为类型的子数据集
for behavior_type_name, group in behavior_data_group_by_data.groupby("behavior_type"):
    i = i + 1
    ax = figure.add_subplot(2, 2, i)
    ax.plot(group["time"], group["count"],  marker='o', label=Behavior.get_decs_by_value(behavior_type_name))
    ax.set_title(Behavior.get_decs_by_value(behavior_type_name))
    ax.set_xlabel('日期')
    ax.set_ylabel('数量')
    ax.legend()

plt.tight_layout()
plt.show()