"""
周期内用户行为频率。
每天点击、收藏、加购物车、购买的频率
每个用户的行为频率？
总的行为频率？：统计总数 然后 除以 天数？
周期内用户行为频率。统计点击，收藏，加购物车，购买的均值，方差，最小，最大等统计量，并画出购买行为的密度分布图。
统计每天的点击，收藏，加购物车，购买的总和
"""
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from src.common.enum.behavior_enum import Behavior
from src.file.read_csv import analyse_csv_pickle
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False

__file_path = "../../file/tianchi_mobile_recommend_train_user.csv"
__file_name = "tianchi_mobile_recommend_train_user"

# 读取文件
pickle = analyse_csv_pickle(__file_path, __file_name)

# 整合 准备数据
behavior_type_time_data = pickle.loc[:, ["behavior_type", "time","user_id"]]
behavior_type_time_data["time"] = pd.to_datetime(behavior_type_time_data["time"]).dt.date

# 根据日期统计用户数量
behavior_type_time_data_count_user_id = (behavior_type_time_data
                                 .groupby(["time"])["user_id"]
                                 .nunique()
                                 .reset_index())
# 根据日期和行为类型统计数量
behavior_type_time_data["count"] = 1
behavior_type_time_data_count_behavior = (behavior_type_time_data
                                 .groupby(["behavior_type","time"])["count"]
                                 .sum()
                                 .reset_index())

# 合并两个DataFrame
merge = pd.merge(behavior_type_time_data_count_user_id, behavior_type_time_data_count_behavior, on='time', how='inner')
# 重命名列名
merge.rename(columns={'user_id': 'user_nums'}, inplace=True)
# 计算频率
merge["frequency"] = merge["count"] / merge["user_nums"]
# 转为一个列索引为 点击 收藏 加购物车 购买
# 行索引为日期
# 元素为 数量 的DataFrame
# 转换为宽格式
frequency_data = merge.pivot(index="time", columns="behavior_type", values="frequency")
# 绘图：为每个行为类型创建单独的密度图
num_behavior_types = len(frequency_data.columns)
fig, axes = plt.subplots(nrows=num_behavior_types, figsize=(10, 6 * num_behavior_types))

# 如果只有一个子图，axes 会是单一的，改为列表方便统一处理
if num_behavior_types == 1:
    axes = [axes]

for i, behavior_type in enumerate(frequency_data.columns):
    ax = axes[i]
    subset = frequency_data[behavior_type]
    # 归一化数据
    subset_normalized = (subset - subset.min()) / (subset.max() - subset.min())
    sns.kdeplot(subset_normalized, ax=ax, shade=True)
    ax.set_title(f'密度图:{Behavior.get_decs_by_value(behavior_type)}')
    ax.set_xlabel(f'{Behavior.get_decs_by_value(behavior_type)}')
    ax.set_ylabel('密度')

# 自动调整布局，避免子图重叠
plt.tight_layout()

# 显示图形
plt.show()