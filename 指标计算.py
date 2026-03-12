import pandas as pd

# 读取数据
acc_data = pd.read_excel('data/20251223二部客户明细.xlsx')
# 读取csv文件
non_rent_data = pd.read_csv('data/二部业绩核对/其他非利息净收入_20251231.csv', encoding='gb18030', dtype=str)
rent_data = pd.read_csv('data/二部业绩核对/利息净收入（账面）_20251231.csv', encoding='gb18030', dtype=str)
charge_data = pd.read_csv('data/二部业绩核对/手续费净收入_20251231.csv', encoding='gb18030', dtype=str)
credits_data = pd.read_csv('data/二部业绩核对/贷款补贴明细查询_20251231.csv', encoding='gb18030', dtype=str)

# 数据标准化
non_rent_data['客户号'] = non_rent_data['客户号'].str[1:]
rent_data['客户号'] = rent_data['客户号'].str[1:]
charge_data['客户号'] = charge_data['客户号'].str[1:]
credits_data['客户号'] = credits_data['客户号'].str[1:]

# 临时处理后续删除
# 将acc_data的客户编号列转换为字符串
acc_data['客户编号'] = acc_data['客户编号'].astype(str)
# 将acc_data中客户编号列前加00
acc_data['客户编号'] = '00' + acc_data['客户编号']

# 仅保留acc_data中存在的客户编号行
non_rent_data = non_rent_data[non_rent_data['客户号'].isin(acc_data['客户编号'])]
rent_data = rent_data[rent_data['客户号'].isin(acc_data['客户编号'])]
charge_data = charge_data[charge_data['客户号'].isin(acc_data['客户编号'])]
credits_data = credits_data[credits_data['客户号'].isin(acc_data['客户编号'])]

# 加总相关数据
# 计算非息收入, non_rent_data中应当加总 营业净收入列, 需要先将营业净收入列转换为数值型
non_rent_data['营业净收入'] = non_rent_data['营业净收入'].str.replace(',', '')
non_rent_data['营业净收入'] = non_rent_data['营业净收入'].astype(float)
non_rent_sum = non_rent_data['营业净收入'].sum()
# 计算利息收入, rent_data中应当加总 营业净收入列, 需要先将营业净收入列转换为数值型
rent_data['营业净收入'] = rent_data['营业净收入'].str.replace(',', '')
rent_data['营业净收入'] = rent_data['营业净收入'].astype(float)
rent_sum = rent_data['营业净收入'].sum()
# 计算手续费收入, charge_data中应当加总 营业净收入列, 需要先将营业净收入列转换为数值型
charge_data['营业净收入'] = charge_data['营业净收入'].str.replace(',', '')
charge_data['营业净收入'] = charge_data['营业净收入'].astype(float)
charge_sum = charge_data['营业净收入'].sum()
# 计算总行补贴, credits_data中应当加总 总行利息补贴列, 需要先将营业净收入列转换为数值型
credits_data['总行利息补贴'] = credits_data['总行利息补贴'].str.replace(',', '')
credits_data['总行利息补贴'] = credits_data['总行利息补贴'].astype(float)
credits_sum = credits_data['总行利息补贴'].sum()

# 计算营收数据 营收净收入 = 利息收入 + 总行补贴
revenue = rent_sum + credits_sum

# 创建最后所需输出数据的表格
output_list = [['营业净收入', revenue], ['利息净收入(账面)', rent_sum], ['非利息收入', non_rent_sum], ['手续费收入', charge_sum],
               ['其他收入', 0]]
# 将output_list转化为dataframe, 列名为考核指标 和 数值
