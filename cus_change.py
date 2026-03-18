# 导入pandas模块
import pandas as pd
import datetime
import io

def main(base_data, cur_data, base_num, eff_num, base_date, current_date, target_date, tar_days, threshold_base_num, threshold_eff_num):
    # 读取公司客户明细表文件, 该表格需要从第四行作为表头开始读取
    base_data = pd.read_excel(base_data, header=3)
    cur_data = pd.read_excel(cur_data, header=3)
    # 管户经理
    manager = ['刘羽佳', '袁若愚', '赵发友', '邸平花', '王任朴', '申思梅', '石家庄维明大街支行公共户', '齐丹']

    # 计算相关参数
    total_period = (target_date - base_date).days + 1
    passed_period = (current_date - base_date).days + 1
    left_period = total_period - passed_period

    # 数据预处理
    # 数据标准化，仅保留有用列
    base_data = standardize_data(base_data)
    cur_data = standardize_data(cur_data)
    # 数据重命名，方便后续表格合并
    base_data = rename_col_old(base_data)
    cur_data = rename_col_new(cur_data)
    # 数据合并
    merged_data = merge_data(base_data, cur_data)

    # 总表整理
    # 获得账户销户情况
    merged_data['账户销户'] = merged_data.apply(lambda x: 1 if pd.isna(x['新时点']) else 0, axis=1)
    # 获取客户降级情况(基于标识：基于标识则年日均和天数双达标）
    merged_data = get_down_acc_status(merged_data)
    # 获取客户降级情况(基于自然年日均：不考虑当年天数达标情况，考虑去年天数达标情况)
    merged_data = get_down_acc_year_ave(merged_data, base_num, eff_num)
    # 获取客户升级情况（基于标识：基于标识则年日均和天数双达标）
    merged_data = get_up_acc_status(merged_data)
    # 获取客户升级情况（基于自然年日均：不考虑当年天数达标情况，考虑去年天数达标情况）
    merged_data = get_up_acc_year_ave(merged_data, base_num, eff_num)
    # 获取预警客户信息
    merged_data = get_warning_acc(merged_data, total_period, passed_period, left_period, base_num, eff_num)
    # 获取临界客户标识
    merged_date = get_critical_acc(merged_data, threshold_base_num, threshold_eff_num, base_num, eff_num)
    # 计算需求来款金额
    merged_data = get_demand_amount(merged_data, base_num, eff_num, total_period, passed_period, tar_days)
    # 获取当前年日均达标情况
    merged_data = get_status_year_ave(merged_data, base_num, eff_num)
    # 获取客户保持当前时点金额预计基础户有效户维持情况
    merged_data = get_keep_acc_status(merged_data, base_num, eff_num)

    # 临时更改管户经理, 此次后可删除
    # qidan_data = pd.read_excel('data/qidan.xlsx')
    # 将qidan_data中的客户号列转为list
    # qidan_list = qidan_data['客户号'].tolist()
    # 将merged_data中纯在与qidan_list中的客户的管户经理改为齐丹
    # merged_data.loc[merged_data['客户号'].isin(qidan_list), '管户经理'] = '齐丹'

    # 获取客户升降级表格
    # 获取基础户基于标识的降级情况表
    down_base_table = get_down_base_table(merged_data)
    # 获取基础户基于自然年日均的降级情况表
    down_base_year_table = get_down_base_year_ave_table(merged_data)
    # 获取基础户基于标识的升级情况表
    up_base_table = get_up_base_table(merged_data)
    # 获取基础户基于年日均的升级情况表
    up_base_year_table = get_up_base_year_ave_table(merged_data)

    base_change_detail = {
        '基础户标识降级情况': down_base_table,
        '基础户年日均降级情况': down_base_year_table,
        '基础户标识升级情况': up_base_table,
        '基础户年日均升级情况': up_base_year_table
    }

    # 获取有效户升降级明细表
    up_eff_table = get_up_eff_table(merged_data)
    up_eff_year_table = get_up_eff_year_ave_table(merged_data)
    down_eff_table = get_down_eff_table(merged_data)
    down_eff_year_table = get_down_eff_year_ave_table(merged_data)

    value_change_detail = {
        '有效户标识降级情况': down_eff_table,
        '有效户年日均降级情况': down_eff_year_table,
        '有效户标识升级情况': up_eff_table,
        '有效户年日均升级情况': up_eff_year_table
    }

    # 获取预警客户以及临界客户信息表
    warning_base_table = get_warning_base_table(merged_data)
    warning_eff_table = get_warning_eff_table(merged_data)
    critical_base_table = get_critical_base_table(merged_data)
    critical_eff_table = get_critical_eff_table(merged_data)

    alarm_and_threshold_detail = {
        '预警基础户信息表': warning_base_table,
        '预警有效户信息表': warning_eff_table,
        '临界基础户信息表': critical_base_table,
        '临界有效户信息表': critical_eff_table
    }

    # 获取基础户有效户数量以及增量情况
    acc_analysis_table = get_acc_status_table(merged_data, manager)
    # 获取基础户有效户数量以及增量情况(基于年日均)
    acc_year_analysis_table = get_acc_year_ave_table(merged_data, manager)
    # 获取基础户有效户数量以及增量情况(基于时点变动预计到目标日期)
    acc_year_predict_analysis_table = get_acc_year_predict_table(merged_data, manager)

    acc_change_summary = {
        '当前标识变动情况': acc_analysis_table,
        '当前年日均变动情况': acc_year_analysis_table,
        '预计变动情况': acc_year_predict_analysis_table
    }


    return merged_data, base_change_detail, value_change_detail, alarm_and_threshold_detail, acc_change_summary


# 标准化数据，仅保留有用列
def standardize_data(data):
    data = data[['客户编号', '数据日期', '客户名称', '绩效归属员工名称', '时点余额', '自然年日均', '基础户', '有效户', '基础户达标天数',
                 '有效户达标天数']]
    return  data

# 重命名基底数据列名
def rename_col_old(data):
    data.rename(columns={'客户编号': '客户号', '数据日期': '旧日期', '客户名称': '旧客户名', '绩效归属员工名称': '旧管户经理',
                         '时点余额': '旧时点', '自然年日均': '去年年日均', '基础户': '旧基础户标识', '有效户': '旧有效户标识',
                         '基础户达标天数': '旧基础户达标天数', '有效户达标天数': '旧有效户达标天数'}, inplace=True)
    return  data

# 重命名当前数据列名
def rename_col_new(data):
    data.rename(columns={'客户编号': '客户号', '数据日期': '新日期', '客户名称': '新客户名', '绩效归属员工名称': '新管户经理',
                         '时点余额': '新时点', '自然年日均': '当前年日均', '基础户': '新基础户标识', '有效户': '新有效户标识',
                         '基础户达标天数': '新基础户达标天数', '有效户达标天数': '新有效户达标天数'}, inplace=True)
    return  data

# 合并两个表格
def merge_data(old_data, new_data):
    data = pd.merge(old_data, new_data, on=['客户号'], how='outer')
    # 客户名以新客户名为准，若新客户名为空，则取旧客户名
    data['客户名'] = data.apply(lambda x: x['新客户名'] if pd.notnull(x['新客户名']) else x['旧客户名'], axis=1)
    # 去除新旧客户名列
    data.drop(columns=['旧客户名', '新客户名'], inplace=True)
    # 管户经理以新管户经理为准，若新管户经理为空，则取旧管户经理
    data['管户经理'] = data.apply(lambda x: x['新管户经理'] if pd.notnull(x['新管户经理']) else x['旧管户经理'], axis=1)
    # 删除新、旧管户经理列
    data.drop(columns=['旧管户经理', '新管户经理'], inplace=True)
    # 重新排列列，相关数据并列，方便数据对比
    data = data[['客户号', '客户名', '管户经理', '旧时点', '新时点', '去年年日均', '当前年日均',
                 '旧基础户标识', '旧有效户标识', '新基础户标识', '新有效户标识', '旧基础户达标天数', '旧有效户达标天数', '新基础户达标天数',
                  '新有效户达标天数']]
    # 若旧标识为空，则标识为0
    data['旧基础户标识'] = data.apply(lambda x: 0 if pd.isnull(x['旧基础户标识']) else x['旧基础户标识'], axis=1)
    data['旧有效户标识'] = data.apply(lambda x: 0 if pd.isnull(x['旧有效户标识']) else x['旧有效户标识'], axis=1)
    # 若旧时点和年日均为空，则设为0
    data['旧时点'] = data.apply(lambda x: 0 if pd.isnull(x['旧时点']) else x['旧时点'], axis=1)
    data['去年年日均'] = data.apply(lambda x: 0 if pd.isnull(x['去年年日均']) else x['去年年日均'], axis=1)
    # 若旧达标日期为空，则设为0
    data['旧基础户达标天数'] = data.apply(lambda x: 0 if pd.isnull(x['旧基础户达标天数']) else x['旧基础户达标天数'], axis=1)
    data['旧有效户达标天数'] = data.apply(lambda x: 0 if pd.isnull(x['旧有效户达标天数']) else x['旧有效户达标天数'], axis=1)
    return  data

# 获取客户基于标识的降级情况
def get_down_acc_status(data):
    # 获取留存客户基础户降级情况
    data['存量基础户降级_标识'] = data.apply(lambda x: 1 if x['旧基础户标识'] == 1 and x['新基础户标识'] == 0 else 0, axis=1)
    # 如果旧基础户标识为1，账户销户为1，则基础户降级同样为1
    data['基础户销户_标识'] = data.apply(lambda x: 1 if x['账户销户'] == 1 and x['旧基础户标识'] == 1 else x['存量基础户降级_标识'], axis=1)
    # 存量基础户降级_标识为1 或 基础户销户_标识为1， 则基础户降级为1
    data['基础户降级_标识'] = data.apply(lambda x: 1 if x['存量基础户降级_标识'] == 1 or x['基础户销户_标识'] == 1 else 0, axis=1)
    data.drop(columns=['存量基础户降级_标识', '基础户销户_标识'], inplace=True)
    # 有效户同理
    data['存量有效户降级_标识'] = data.apply(lambda x: 1 if x['旧有效户标识'] == 1 and x['新有效户标识'] == 0 else 0, axis=1)
    data['有效户销户_标识'] = data.apply(lambda x: 1 if x['账户销户'] == 1 and x['旧有效户标识'] == 1 else x['存量有效户降级_标识'], axis=1)
    data['有效户降级_标识'] = data.apply(lambda x: 1 if x['存量有效户降级_标识'] == 1 or x['有效户销户_标识'] == 1 else 0, axis=1)
    data.drop(columns=['存量有效户降级_标识', '有效户销户_标识'], inplace=True)
    return  data

# 获取客户基于标识的升级情况
def get_up_acc_status(data):
    # 获取存量客户基础户升级情况
    data['基础户升级_标识'] = data.apply(lambda x: 1 if x['旧基础户标识'] == 0 and x['新基础户标识'] == 1 else 0, axis=1)
    # 获取存量客户有效户升级情况
    data['有效户升级_标识'] = data.apply(lambda x: 1 if x['旧有效户标识'] == 0 and x['新有效户标识'] == 1 else 0, axis=1)
    return  data

# 获取客户基于自然年日均的降级情况
def get_down_acc_year_ave(data, base, eff):
    # 如果旧基础户标识为1，当前年日均<=10万，则基础户降级为1
    data['存量基础户降级_年日均'] = data.apply(lambda x: 1 if x['旧基础户标识'] == 1 and x['当前年日均'] <= base else 0, axis=1)
    data['基础户销户_年日均'] = data.apply(lambda x: 1 if x['账户销户'] == 1 and x['旧基础户标识'] == 1 else x['存量基础户降级_年日均'], axis=1)
    data['基础户降级_年日均'] = data.apply(lambda x: 1 if x['存量基础户降级_年日均'] == 1 or x['基础户销户_年日均'] == 1 else 0, axis=1)
    data.drop(columns=['存量基础户降级_年日均', '基础户销户_年日均'], inplace=True)
    # 如果旧有效户标识为1，当前年日均<=10万，则有效户降级为1
    data['存量有效户降级_年日均'] = data.apply(lambda x: 1 if x['旧有效户标识'] == 1 and x['当前年日均'] <= eff else 0, axis=1)
    data['有效户销户_年日均'] = data.apply(lambda x: 1 if x['账户销户'] == 1 and x['旧有效户标识'] == 1 else x['存量有效户降级_年日均'], axis=1)
    data['有效户降级_年日均'] = data.apply(lambda x: 1 if x['存量有效户降级_年日均'] == 1 or x['有效户销户_年日均'] == 1 else 0, axis=1)
    data.drop(columns=['存量有效户降级_年日均', '有效户销户_年日均'], inplace=True)
    return  data

# 获取客户基于自然年日均的升级情况
def get_up_acc_year_ave(data, base, eff):
    # 如果旧基础户标识为0，当前年日均>=base，则基础户升级为1
    data['基础户升级_年日均'] = data.apply(lambda x: 1 if x['旧基础户标识'] == 0 and x['当前年日均'] >= base else 0, axis=1)
    # 如果旧有效户标识为0，当前年日均>=eff，则有效户升级为1
    data['有效户升级_年日均'] = data.apply(lambda x: 1 if x['旧有效户标识'] == 0 and x['当前年日均'] >= eff else 0, axis=1)
    return  data

# 获取预警客户信息，预警客户目前年日均达标，但是若继续维持当前时点数据，在目标时间时，自然年日均会降级
def get_warning_acc(data, total_days, passed_days, left_days, base, eff):

    # 假设当前时点数据继续维持，根据当前时点数据以及年日均数据计算target_date时的年日均
    # 计算公式为： 预计年日均 = (当前年日均 * pass_period + 新时点 * left_period） / tol_period
    # 需要计算每个客户的预计年日均
    data['预计年日均'] = data.apply(lambda x: (x['当前年日均'] * passed_days + x['新时点'] * left_days) / total_days, axis=1)
    # 如果当前年日均 >= base 且 预计年日均 <= base，则预警客户为1
    data['预警基础户'] = data.apply(lambda x: 1 if x['当前年日均'] >= base >= x['预计年日均'] else 0, axis=1)
    data['预警有效户'] = data.apply(lambda x: 1 if x['当前年日均'] >= eff >= x['预计年日均'] else 0, axis=1)
    return data

# 获取临界客户标识
def get_critical_acc(data, threshold_base, threshold_eff, base, eff):
    # 如果当前年日均大于threshold_base，则基础户临界为1
    data['基础户临界'] = data.apply(lambda x: 1 if base > x['当前年日均'] > threshold_base else 0, axis=1)
    # 如果当前年日均大于threshold_eff，则有效户临界为1
    data['有效户临界'] = data.apply(lambda x: 1 if eff > x['当前年日均'] > threshold_eff else 0, axis=1)
    return data

# 计算需求来款金额
def get_demand_amount(data, base,  eff, total_days, passed_days, keep_days):
    # 基础户达标需来款金额 = (（base * total_days - 当前年日均 * passed_days） / keep_days) - 新时点
    data['基础户来款_零时点'] = data.apply(lambda x: ((base * total_days - x['当前年日均'] * passed_days) / keep_days) - x['新时点'], axis=1)
    # 若基础户达标需来款金额 < 0，则基础户来款为0
    data['基础户来款_零时点'] = data.apply(lambda x: 0 if x['基础户来款_零时点'] < 0 else x['基础户来款_零时点'], axis=1)
    # 有效户达标需来款金额 = (（eff * total_days - 当前年日均 * passed_days） / keep_days) - 新时点
    data['有效户来款_零时点'] = data.apply(lambda x: ((eff * total_days - x['当前年日均'] * passed_days) / keep_days) - x['新时点'], axis=1)
    # 若有效户达标需来款金额 < 0，则有效户来款为0
    data['有效户来款_零时点'] = data.apply(lambda x: 0 if x['有效户来款_零时点'] < 0 else x['有效户来款_零时点'], axis=1)
    return data

# 计算基于当前年日均是否达标基础户和有效户
def get_status_year_ave(data, base, eff):
    data['年日均基础户达标'] = data.apply(lambda x: 1 if x['当前年日均'] >= base else 0, axis=1)
    data['年日均有效户达标'] = data.apply(lambda x: 1 if x['当前年日均'] >= eff else 0, axis=1)
    return data

# 获取客户保持当前时点金额预计基础户有效户维持情况
def get_keep_acc_status(data, base, eff):
    # 如果预计年日均 >= base 则基础户保持为1
    data['年日均基础户保持'] = data.apply(lambda x: 1 if x['预计年日均'] >= base else 0, axis=1)
    # 如果预计年日均 >= eff 则有效户保持为1
    data['年日均有效户保持'] = data.apply(lambda x: 1 if x['预计年日均'] >= eff else 0, axis=1)
    return data

# 获取附表
# 首先获取基础户基于标识的降级情况表
def get_down_base_table(data):
    data = data[['客户名', '管户经理', '账户销户', '基础户降级_标识', '去年年日均', '当前年日均', '新时点',
                 '旧基础户达标天数', '新基础户达标天数', '基础户来款_零时点']]
    # 筛选出基础户基于标识的降级情况
    data = data[data['基础户降级_标识'] == 1]
    # 去除基础户降级_标识列
    data.drop(columns=['基础户降级_标识'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取基础户基于自然年日均的降级情况表
def get_down_base_year_ave_table(data):
    data = data[['客户名', '管户经理', '账户销户', '基础户降级_年日均', '去年年日均', '当前年日均', '新时点',
                 '旧基础户达标天数', '新基础户达标天数', '基础户来款_零时点']]
    # 筛选出客户基于自然年日均的降级情况
    data = data[data['基础户降级_年日均'] == 1]
    # 去除基础户降级_年日均列
    data.drop(columns=['基础户降级_年日均'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取客户基于标识的升级情况表
def get_up_base_table(data):
    data = data[['客户名', '管户经理', '基础户升级_标识', '去年年日均', '当前年日均', '新时点',
                 '旧基础户达标天数', '新基础户达标天数', '有效户来款_零时点']]
    # 筛选出客户基于标识的升级情况
    data = data[data['基础户升级_标识'] == 1]
    # 去除基础户升级_标识列
    data.drop(columns=['基础户升级_标识'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取客户基于年日均的升级情况表
def get_up_base_year_ave_table(data):
    data = data[['客户名', '管户经理', '基础户升级_年日均', '去年年日均', '当前年日均', '新时点',
                 '旧基础户达标天数', '新基础户达标天数', '有效户来款_零时点']]
    # 筛选出客户基于年日均的升级情况
    data = data[data['基础户升级_年日均'] == 1]
    # 去除基础户升级_年日均列
    data.drop(columns=['基础户升级_年日均'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取有效户升降级情况表
# 获取客户基于标识的升级情况表
def get_up_eff_table(data):
    data = data[['客户名', '管户经理', '有效户升级_标识', '去年年日均', '当前年日均', '新时点',
                 '旧有效户达标天数', '新有效户达标天数', '有效户来款_零时点']]
    # 筛选出客户基于标识的升级情况
    data = data[data['有效户升级_标识'] == 1]
    # 去除有效户升级_标识列
    data.drop(columns=['有效户升级_标识'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取有效户基于自然年日均的升级情况表
def get_up_eff_year_ave_table(data):
    data = data[['客户名', '管户经理', '有效户升级_年日均', '去年年日均', '当前年日均', '新时点',
                 '旧有效户达标天数', '新有效户达标天数', '有效户来款_零时点']]
    # 筛选出客户基于自然年日均的升级情况
    data = data[data['有效户升级_年日均'] == 1]
    # 去除有效户升级_年日均列
    data.drop(columns=['有效户升级_年日均'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取有效户基于标识的降级情况表
def get_down_eff_table(data):
    data = data[['客户名', '管户经理', '账户销户', '有效户降级_标识', '去年年日均', '当前年日均', '新时点',
                 '旧有效户达标天数', '新有效户达标天数', '有效户来款_零时点']]
    # 筛选出客户基于标识的降级情况
    data = data[data['有效户降级_标识'] == 1]
    # 去除有效户降级_标识列
    data.drop(columns=['有效户降级_标识'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取有效户基于年日均的降级情况表
def get_down_eff_year_ave_table(data):
    data = data[['客户名', '管户经理', '账户销户', '有效户降级_年日均', '去年年日均', '当前年日均', '新时点',
                 '旧有效户达标天数', '新有效户达标天数', '有效户来款_零时点']]
    # 筛选出客户基于年日均的降级情况
    data = data[data['有效户降级_年日均'] == 1]
    # 去除有效户降级_年日均列
    data.drop(columns=['有效户降级_年日均'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取预警客户以及临界客户信息表
# 获取预警基础户信息表
def get_warning_base_table(data):
    # 仅保留有用列
    data = data[['客户名', '管户经理', '去年年日均', '当前年日均', '新时点', '预警基础户', '基础户来款_零时点', '有效户来款_零时点']]
    # 仅保留预警基础户信息
    data = data[data['预警基础户'] == 1]
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    return data

# 获取预警有效户信息表
def get_warning_eff_table(data):
    # 仅保留有用列
    data = data[['客户名', '管户经理', '去年年日均', '当前年日均', '新时点', '预警有效户', '基础户来款_零时点', '有效户来款_零时点']]
    # 仅保留预警有效户信息
    data = data[data['预警有效户'] == 1]
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    return data

# 获取临界基础户信息表
def get_critical_base_table(data):
    # 仅保留有用列
    data = data[['客户名', '管户经理', '去年年日均', '当前年日均', '新时点', '基础户临界', '基础户来款_零时点', '有效户来款_零时点']]
    # 仅保留临界基础户信息
    data = data[data['基础户临界'] == 1]
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    return data

# 获取临界有效户信息表
def get_critical_eff_table(data):
    # 仅保留有用列
    data = data[['客户名', '管户经理', '去年年日均', '当前年日均', '新时点', '有效户临界', '基础户来款_零时点', '有效户来款_零时点']]
    # 仅保留临界有效户信息
    data = data[data['有效户临界'] == 1]
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    return data

# 分别从支行层面以及管户经理层面分析基础户以及有效户的升降级情况并输出表格(基于标识)
def get_acc_status_table(data, managers):
    # 获取旧基础户有效户数量
    old_base_num = data['旧基础户标识'].sum()
    old_eff_num = data['旧有效户标识'].sum()
    # 获取新基础户数量
    new_base_num = data['新基础户标识'].sum()
    new_eff_num = data['新有效户标识'].sum()
    # 获取支行基础户有效户增量情况
    base_inc_num = new_base_num - old_base_num
    eff_inc_num = new_eff_num - old_eff_num

    # 创建输出表格
    acc_status_table = pd.DataFrame(columns=['管户经理', '基础户增量', '有效户增量', '旧基础户数量', '新基础户数量',
                                             '旧有效户数量', '新有效户数量'])
    # 现将支行情况添加到表格中
    acc_status_table.loc[0] = ['支行', base_inc_num, eff_inc_num, old_base_num, new_base_num, old_eff_num, new_eff_num]

    # 分析每位客户经理的基础户有效户数量以及增量情况
    for m in managers:
        manager_data = data[data['管户经理'] == m]
        manger_old_base_num = manager_data['旧基础户标识'].sum()
        manger_old_eff_num = manager_data['旧有效户标识'].sum()
        manger_new_base_num = manager_data['新基础户标识'].sum()
        manger_new_eff_num = manager_data['新有效户标识'].sum()
        manger_base_inc_num = manger_new_base_num - manger_old_base_num
        manger_eff_inc_num = manger_new_eff_num - manger_old_eff_num
        acc_status_table.loc[len(acc_status_table)] = [m, manger_base_inc_num, manger_eff_inc_num,
                                                       manger_old_base_num, manger_new_base_num,
                                                       manger_old_eff_num, manger_new_eff_num]

    return acc_status_table

# 从年日均的角度分析基础户以及有效户的升降级情况并输出表格(基于年日均)
def get_acc_year_ave_table(data, managers):
    # 获取旧基础户有效户数量
    old_base_num = data['旧基础户标识'].sum()
    old_eff_num = data['旧有效户标识'].sum()
    # 获取新基础户数量
    new_base_num = data['年日均基础户达标'].sum()
    new_eff_num = data['年日均有效户达标'].sum()
    # 获取支行基础户有效户增量情况
    base_inc_num = new_base_num - old_base_num
    eff_inc_num = new_eff_num - old_eff_num
    acc_status_table = pd.DataFrame(columns=['管户经理', '基础户增量', '有效户增量', '旧基础户数量', '新基础户数量',
                                             '旧有效户数量', '新有效户数量'])
    acc_status_table.loc[0] = ['支行', base_inc_num, eff_inc_num, old_base_num, new_base_num, old_eff_num, new_eff_num]
    for m in managers:
        manager_data = data[data['管户经理'] == m]
        manger_old_base_num = manager_data['旧基础户标识'].sum()
        manger_old_eff_num = manager_data['旧有效户标识'].sum()
        manger_new_base_num = manager_data['年日均基础户达标'].sum()
        manger_new_eff_num = manager_data['年日均有效户达标'].sum()
        manger_base_inc_num = manger_new_base_num - manger_old_base_num
        manger_eff_inc_num = manger_new_eff_num - manger_old_eff_num
        acc_status_table.loc[len(acc_status_table)] = [m, manger_base_inc_num, manger_eff_inc_num,
                                                       manger_old_base_num, manger_new_base_num,
                                                       manger_old_eff_num, manger_new_eff_num]
    return acc_status_table

# 根据时点变动预计到目标日期获取基础户有效户年日均达标情况
def get_acc_year_predict_table(data, managers):
    # 获取旧基础户有效户数量
    old_base_num = data['旧基础户标识'].sum()
    old_eff_num = data['旧有效户标识'].sum()
    # 获取新基础户数量
    new_base_num = data['年日均基础户保持'].sum()
    new_eff_num = data['年日均有效户保持'].sum()
    # 获取支行基础户有效户增量情况
    base_inc_num = new_base_num - old_base_num
    eff_inc_num = new_eff_num - old_eff_num
    acc_status_table = pd.DataFrame(columns=['管户经理', '基础户增量', '有效户增量', '旧基础户数量', '新基础户数量',
                                             '旧有效户数量', '新有效户数量'])
    acc_status_table.loc[0] = ['支行', base_inc_num, eff_inc_num, old_base_num, new_base_num, old_eff_num, new_eff_num]
    for m in managers:
        manager_data = data[data['管户经理'] == m]
        manger_old_base_num = manager_data['旧基础户标识'].sum()
        manger_old_eff_num = manager_data['旧有效户标识'].sum()
        manger_new_base_num = manager_data['年日均基础户保持'].sum()
        manger_new_eff_num = manager_data['年日均有效户保持'].sum()
        manger_base_inc_num = manger_new_base_num - manger_old_base_num
        manger_eff_inc_num = manger_new_eff_num - manger_old_eff_num
        acc_status_table.loc[len(acc_status_table)] = [m, manger_base_inc_num, manger_eff_inc_num,
                                                       manger_old_base_num, manger_new_base_num,
                                                       manger_old_eff_num, manger_new_eff_num]
    return acc_status_table


