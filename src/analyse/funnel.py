"""
漏斗模型：用户行为转化分析
behavior_type：用户行为
    1:点击
    2:收藏
    3:添加购物车
    4:购买
即统计点击，加购物车和购买的频率，并用柱状图表示，呈现漏斗状。
30天内用户每天平均点击多少次，加购物车多少次，购买多少次。
点击数量/用户总数  收藏数量/用户总数  加购物车数量/用户总数  购买数量/用户总数
"""
import pandas as pd
from matplotlib import pyplot as plt

from src.common.enum.behavior_enum import Behavior
from src.file.read_csv import analyse_csv_pickle

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False

__file_path = "../../file/tianchi_mobile_recommend_train_user.csv"
__file_name = "tianchi_mobile_recommend_train_user"

# 读取文件
data = analyse_csv_pickle(__file_path, __file_name)
# 根据用户分组 统计有多少用户
user_id_data = data.loc[:, ["user_id"]]
distinct_user_id_data = user_id_data.drop_duplicates()
user_nums = distinct_user_id_data.shape[0]

# user_id_data["count"] = 1
# user_nums = ["count"].sum()
# 根据行为分类 统计数量
behavior_type_data = data.loc[:, ["behavior_type"]]
behavior_type_data["count"] = 1

# 分组
behavior_type_data_group = behavior_type_data.groupby(behavior_type_data["behavior_type"])["count"].sum()

# 循环绘制字典类型
behavior_data_dict = {}
for name, group in behavior_type_data_group.items():
    behavior_data_dict[Behavior.get_decs_by_value(name)] = group/user_nums

# 字典转为DataFrame便于画图
behavior_data_dict = pd.DataFrame.from_dict(behavior_data_dict, orient='index')

# 创建图表
fig, axes = plt.subplots(1, 1, figsize=(10, 6))

# 绘制水平条形图
behavior_data_dict.plot.barh(ax=axes, color='k', alpha=0.7)

# 设置图表标题和标签
axes.set_title("30天用户行为频率图")
axes.set_xlabel("频率")
axes.set_ylabel("行为描述")

# 显示图表
plt.show()