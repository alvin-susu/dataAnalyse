import pandas as pd

frame = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=['a', 'b', 'c'], index=['x', 'y', 'z'])

# print(frame)
# # 从0开始取n行
# print(frame.head(2))
# # 获取列数
# print(frame.columns)
# print(frame.columns.size)
# # 获取行数
# print(frame.index.size)
# # 求平均值
# print(frame.mean(axis='index')['a'])
# # 求和
# print(frame.sum(axis='index'))
#
# # 列可以使用数组的索引方式直接获取为一个Series
# print(frame['a'])
# # 也可以直接属性获取的方式获取为一个Series
# print(frame.a)
#
# # 取行的话使用loc函数获取
# print(frame.loc['x'])
# print(frame.iloc[0])
#
# print(frame.describe())
#
# frame.drop(['a'], axis=1, inplace=True)
# print(frame)


print(help(frame.tail()))
