"""
漏斗模型：用户行为转化分析
behavior_type：用户行为
    1:点击
    2:收藏
    3:添加购物车
    4:购买
"""

from plotly import graph_objects as go
import plotly.express as px

from src.common.enum.behavior_enum import Behavior
from src.file.read_csv import analyse_csv_pickle

__file_path = "../../file/tianchi_mobile_recommend_train_user.csv"
__file_name = "tianchi_mobile_recommend_train_user"

# 读取文件
data = analyse_csv_pickle(__file_path, __file_name)

behavior_type_data = data.loc[:, ["behavior_type"]]
behavior_type_data["count"] = 1

# 分组
behavior_type_data_group = behavior_type_data.groupby(behavior_type_data["behavior_type"])["count"].sum()

# 循环绘制字典类型
behavior_data_dict = {}
for name, group in behavior_type_data_group.items():
    behavior_data_dict[Behavior.get_decs_by_value(name)]= group


# 绘制漏斗图
fig = px.funnel_area(
    names=list(behavior_data_dict.keys()),
    values=list(behavior_data_dict.values())
)
fig.show()