from enum import Enum

class Behavior(Enum):
    """
    行为枚举
    behavior_type：用户行为
    1:点击
    2:收藏
    3:添加购物车
    4:购买
    """

    def __new__(cls, value, description):
        obj = object.__new__(cls)  # 创建实例
        obj._value_ = value        # 设置唯一值
        obj.description = description  # 设置描述
        return obj


    def __str__(self):
        return self.description

    @staticmethod
    def get_decs_by_value(behavior_value):
        for behavior in Behavior:
            if behavior.value == behavior_value:
                return behavior.description
        return None

    CLICK = (1,"点击量")
    COLLECT = (2,"收藏量")
    ADD_CART = (3,"添加购物车次数")
    PURCHASE = (4,"购买量")