import pandas as pd

# 读取文件
data = pd.read_excel('data/公司客户明细表20251231.xlsx', header=3)

# 仅保留客户编号 和 客户名称 列
data = data[['客户编号', '客户名称']]

# 增加一列序号
data['序号'] = range(1, len(data) + 1)
# 排序列
data = data[['序号', '客户编号', '客户名称']]

# 将数据带着序号输出为客户明细表
data.to_excel('data/客户明细表.xlsx', index=False)