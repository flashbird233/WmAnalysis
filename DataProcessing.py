# 模块儿导入
import pandas as pd
import streamlit as st

#-----------------------------------------------------------------------------------------------------------------------
# 基数对比总表处理
# 基数对比总表处理主方法
def main():
    # 将file文件读取为DataFrame，第三行为表头
    file_to_data()
    # 获取或计算相关参数
    calc_params()
    # 标准化数据
    st.session_state.last_year_data, st.session_state.current_data = (
        standardize_data(st.session_state.last_year_data, st.session_state.current_data))
    # 合并数据
    st.session_state.total_table = merge_data(st.session_state.last_year_data, st.session_state.current_data)
    # 总表加工
    total_table_processing()
    # 生成表格
    get_tables(st.session_state.total_table, st.session_state.manager_list)

#-----------------------------------------------------------------------------------------------------------------------
# 基数对比总表次方法
# 将file文件读取为DataFrame，第三行为表头
def file_to_data():
    # 获取去年数据
    st.session_state.last_year_data = pd.read_excel(st.session_state.last_year_file, header=3)
    # 获取当前数据
    st.session_state.current_data = pd.read_excel(st.session_state.current_file, header=3)

# 计算或获取相关参数
def calc_params():
    # 计算相关参数
    # 计算日期相关参数
    # 总天数
    st.session_state.total_days = (st.session_state.ass_end_date - st.session_state.last_year_date).days + 1
    # 已过天数
    st.session_state.passed_days = (st.session_state.current_date - st.session_state.last_year_date).days + 1
    # 剩余天数
    st.session_state.left_days = st.session_state.total_days - st.session_state.passed_days

    # 获取客户经理列表，客户经理列表应为去年的客户经理列表和当前客户经理列表的并集，并且去重
    st.session_state.manager_list = (list(set(st.session_state.last_year_data['绩效归属员工名称'].unique())
                                          .union(set(st.session_state.current_data['绩效归属员工名称'].unique()))))

# 总表加工
def total_table_processing():
    # 获得账户销户情况
    st.session_state.total_table['账户销户'] = st.session_state.total_table.apply(
        lambda x: 1 if pd.isna(x['当前时点']) else 0, axis=1)
    # 获取客户降级情况(基于标识：基于标识则年日均和天数双达标）
    st.session_state.total_table = get_down_acc_status(st.session_state.total_table)
    # 获取客户降级情况(基于自然年日均：不考虑当年天数达标情况，考虑去年天数达标情况)
    st.session_state.total_table = get_down_acc_year_ave(st.session_state.total_table, st.session_state.base_standard,
                                                         st.session_state.eff_standard)
    # 获取客户升级情况（基于标识：基于标识则年日均和天数双达标）
    st.session_state.total_table = get_up_acc_status(st.session_state.total_table)
    # 获取客户升级情况（基于自然年日均：不考虑当年天数达标情况，考虑去年天数达标情况）
    st.session_state.total_table = get_up_acc_year_ave(st.session_state.total_table, st.session_state.base_standard,
                                                       st.session_state.eff_standard)
    # 获取预警客户信息
    st.session_state.total_table = get_warning_acc(st.session_state.total_table, st.session_state.total_days,
                                                   st.session_state.passed_days, st.session_state.left_days,
                                                   st.session_state.base_standard, st.session_state.eff_standard)
    # 获取临界客户标识
    st.session_state.total_table = get_critical_acc(st.session_state.total_table,
                                                    st.session_state.base_critical_standard,
                                                    st.session_state.eff_critical_standard,
                                                    st.session_state.base_standard, st.session_state.eff_standard)
    # 计算需求来款金额
    st.session_state.total_table = get_demand_amount(st.session_state.total_table, st.session_state.base_standard,
                                                     st.session_state.eff_standard, st.session_state.total_days,
                                                     st.session_state.passed_days, st.session_state.keep_days,
                                                     st.session_state.left_days)
    # 获取当前年日均达标情况
    st.session_state.total_table = get_status_year_ave(st.session_state.total_table, st.session_state.base_standard,
                                                       st.session_state.eff_standard)
    # 获取客户保持当前时点金额预计基础户有效户维持情况
    st.session_state.total_table = get_keep_acc_status(st.session_state.total_table, st.session_state.base_standard,
                                                       st.session_state.eff_standard)

# 获取各项表格
def get_tables(data, managers):
    # 获取客户升降级表格
    # 获取基础户基于标识的降级情况表
    base_acc_down = get_down_base_table(data)
    # 获取基础户基于自然年日均的降级情况表
    base_acc_down_year_ave = get_down_base_year_ave_table(data)
    # 获取基础户基于标识的升级情况表
    eff_acc_up = get_up_base_table(data)
    # 获取基础户基于年日均的升级情况表
    eff_acc_up_year_ave = get_up_base_year_ave_table(data)

    st.session_state.base_acc_changes_dict = {
        '基础户降级': base_acc_down,
        '基础户升级': eff_acc_up,
        '基础户降级（基于年日均）': base_acc_down_year_ave,
        '基础户升级（基于年日均）': eff_acc_up_year_ave
    }

    # 获取有效户升降级明细表
    up_eff_table = get_up_eff_table(data)
    up_eff_year_table = get_up_eff_year_ave_table(data)
    down_eff_table = get_down_eff_table(data)
    down_eff_year_table = get_down_eff_year_ave_table(data)

    value_change_detail = {
        '有效户标识降级情况': down_eff_table,
        '有效户年日均降级情况': down_eff_year_table,
        '有效户标识升级情况': up_eff_table,
        '有效户年日均升级情况': up_eff_year_table
    }

    # 获取预警客户以及临界客户信息表
    warning_base_table = get_warning_base_table(data)
    warning_eff_table = get_warning_eff_table(data)
    critical_base_table = get_critical_base_table(data)
    critical_eff_table = get_critical_eff_table(data)

    alarm_and_threshold_detail = {
        '预警基础户信息表': warning_base_table,
        '预警有效户信息表': warning_eff_table,
        '临界基础户信息表': critical_base_table,
        '临界有效户信息表': critical_eff_table
    }

    # 获取基础户有效户数量以及增量情况
    acc_analysis_table = get_acc_status_table(data, managers)
    # 获取基础户有效户数量以及增量情况(基于年日均)
    acc_year_analysis_table = get_acc_year_ave_table(data, managers)
    # 获取基础户有效户数量以及增量情况(基于时点变动预计到目标日期)
    acc_year_predict_analysis_table = get_acc_year_predict_table(data, managers)

    acc_change_summary = {
        '当前标识变动情况': acc_analysis_table,
        '当前年日均变动情况': acc_year_analysis_table,
        '预计变动情况': acc_year_predict_analysis_table
    }

#-----------------------------------------------------------------------------------------------------------------------
# 可复用方法 - 表格处理
# 标准化数据
def standardize_data(base_data, new_data):
    # 仅保留有用列
    base_data = base_data[
        ['客户编号', '数据日期', '客户名称', '绩效归属员工名称', '时点余额', '自然年日均', '基础户', '有效户',
         '基础户达标天数', '有效户达标天数']]
    new_data = new_data[
        ['客户编号', '数据日期', '客户名称', '绩效归属员工名称', '时点余额', '自然年日均', '基础户', '有效户',
         '基础户达标天数', '有效户达标天数']]

    # 重命名列名
    # 重命名基底数据列名
    base_data.rename(
        columns={'客户编号': '客户号', '数据日期': '旧日期', '客户名称': '旧客户名', '绩效归属员工名称': '旧管户经理',
                 '时点余额': '旧时点', '自然年日均': '去年年日均', '基础户': '旧基础户标识', '有效户': '旧有效户标识',
                 '基础户达标天数': '旧基础户达标天数', '有效户达标天数': '旧有效户达标天数'}, inplace=True)
    # 重命名当前数据列名
    new_data.rename(
        columns={'客户编号': '客户号', '数据日期': '新日期', '客户名称': '新客户名', '绩效归属员工名称': '新管户经理',
                 '时点余额': '当前时点', '自然年日均': '当前年日均', '基础户': '新基础户标识', '有效户': '新有效户标识',
                 '基础户达标天数': '新基础户达标天数', '有效户达标天数': '新有效户达标天数'}, inplace=True)

    return base_data, new_data

# 合并数据
def merge_data(base_data, new_data):
    data = pd.merge(base_data, new_data, on=['客户号'], how='outer')
    # 客户名以新客户名为准，若新客户名为空，则取旧客户名
    data['客户名'] = data.apply(lambda x: x['新客户名'] if pd.notnull(x['新客户名']) else x['旧客户名'], axis=1)
    # 去除新旧客户名列
    data.drop(columns=['旧客户名', '新客户名'], inplace=True)
    # 管户经理以新管户经理为准，若新管户经理为空，则取旧管户经理
    data['管户经理'] = data.apply(lambda x: x['新管户经理'] if pd.notnull(x['新管户经理']) else x['旧管户经理'], axis=1)
    # 删除新、旧管户经理列
    data.drop(columns=['旧管户经理', '新管户经理'], inplace=True)
    # 重新排列列，相关数据并列，方便数据对比
    data = data[['客户号', '客户名', '管户经理', '旧时点', '当前时点', '去年年日均', '当前年日均',
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
    # 若新标识为空，则标识为0
    data['新基础户标识'] = data.apply(lambda x: 0 if pd.isnull(x['新基础户标识']) else x['新基础户标识'], axis=1)
    data['新有效户标识'] = data.apply(lambda x: 0 if pd.isnull(x['新有效户标识']) else x['新有效户标识'], axis=1)
    return  data

#-----------------------------------------------------------------------------------------------------------------------
# 可复用方法 - 总表加工：相关变量计算
# 获取客户基于标识的降级情况
def get_down_acc_status(data):
    # 获取留存客户基础户降级情况
    data['存量基础户降级_标识'] = data.apply(lambda x: 1 if x['旧基础户标识'] == 1 and x['新基础户标识'] == 0 else 0, axis=1)
    # 如果旧基础户标识为1，账户销户为1，则基础户降级同样为1
    data['基础户销户_标识'] = data.apply(lambda x: 1 if x['账户销户'] == 1
                                                        and x['旧基础户标识'] == 1 else x['存量基础户降级_标识'], axis=1)
    # 存量基础户降级_标识为1 或 基础户销户_标识为1， 则基础户降级为1
    data['基础户降级_标识'] = data.apply(lambda x: 1 if x['存量基础户降级_标识'] == 1 or x['基础户销户_标识'] == 1 else 0, axis=1)
    data.drop(columns=['存量基础户降级_标识', '基础户销户_标识'], inplace=True)
    # 有效户同理
    data['存量有效户降级_标识'] = data.apply(lambda x: 1 if x['旧有效户标识'] == 1 and x['新有效户标识'] == 0 else 0, axis=1)
    data['有效户销户_标识'] = data.apply(lambda x: 1 if x['账户销户'] == 1
                                                        and x['旧有效户标识'] == 1 else x['存量有效户降级_标识'], axis=1)
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
    data['基础户销户_年日均'] = data.apply(lambda x: 1 if x['账户销户'] == 1
                                                          and x['旧基础户标识'] == 1 else x['存量基础户降级_年日均'], axis=1)
    data['基础户降级_年日均'] = data.apply(lambda x: 1 if x['存量基础户降级_年日均'] == 1
                                                          or x['基础户销户_年日均'] == 1 else 0, axis=1)
    data.drop(columns=['存量基础户降级_年日均', '基础户销户_年日均'], inplace=True)
    # 如果旧有效户标识为1，当前年日均<=10万，则有效户降级为1
    data['存量有效户降级_年日均'] = data.apply(lambda x: 1 if x['旧有效户标识'] == 1
                                                              and x['当前年日均'] <= eff else 0, axis=1)
    data['有效户销户_年日均'] = data.apply(lambda x: 1 if x['账户销户'] == 1
                                                          and x['旧有效户标识'] == 1 else x['存量有效户降级_年日均'], axis=1)
    data['有效户降级_年日均'] = data.apply(lambda x: 1 if x['存量有效户降级_年日均'] == 1
                                                          or x['有效户销户_年日均'] == 1 else 0, axis=1)
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
    # 计算公式为： 预计年日均 = (当前年日均 * pass_period + 当前时点 * left_period） / tol_period
    # 需要计算每个客户的预计年日均
    data['预计年日均'] = data.apply(lambda x: (x['当前年日均'] * passed_days + x['当前时点'] * left_days) / total_days,
                                    axis=1)
    # 如果当前年日均 >= base 且 预计年日均 <= base，则预警客户为1
    data['预警基础户'] = data.apply(lambda x: 1 if x['当前年日均'] >= base >= x['预计年日均'] else 0, axis=1)
    data['预警有效户'] = data.apply(lambda x: 1 if x['当前年日均'] >= eff >= x['预计年日均'] else 0, axis=1)
    return data

# 获取临界客户标识
def get_critical_acc(data, threshold_base, threshold_eff, base, eff):
    # 如果当前年日均大于threshold_base，则基础户临界为1
    data['基础户临界'] = data.apply(lambda x: 1 if base > x['当前年日均'] >= threshold_base else 0, axis=1)
    # 如果当前年日均大于threshold_eff，则有效户临界为1
    data['有效户临界'] = data.apply(lambda x: 1 if eff > x['当前年日均'] >= threshold_eff else 0, axis=1)
    return data

# 计算需求来款金额
def get_demand_amount(data, base,  eff, total_days, passed_days, keep_days, left_days):
    # 获取在目标日期外时点金额为0的预计来款金额
    # 基础户达标需来款金额 = (（base * total_days - 当前年日均 * passed_days） / keep_days) - 当前时点
    data['基础户来款_零时点'] = data.apply(lambda x: ((base * total_days - x['当前年日均'] * passed_days) / keep_days)
                                                     - x['当前时点'], axis=1)
    # 若基础户达标需来款金额 < 0，则基础户来款为0
    data['基础户来款_零时点'] = data.apply(lambda x: 0 if x['基础户来款_零时点'] < 0 else x['基础户来款_零时点'], axis=1)
    # 有效户达标需来款金额 = (（eff * total_days - 当前年日均 * passed_days） / keep_days) - 当前时点
    data['有效户来款_零时点'] = data.apply(lambda x: ((eff * total_days - x['当前年日均'] * passed_days) / keep_days)
                                                     - x['当前时点'], axis=1)
    # 若有效户达标需来款金额 < 0，则有效户来款为0
    data['有效户来款_零时点'] = data.apply(lambda x: 0 if x['有效户来款_零时点'] < 0 else x['有效户来款_零时点'], axis=1)

    # 获取在目标日期外时点金额保持当前时点金额的预计来款金额
    # 基础户来款_时点保持 = ((base * total_days - 当前年日均 * passed_days - 当前时点 * left_days） / keep_days)
    data['基础户来款_时点保持'] = data.apply(lambda x: ((base * total_days - x['当前年日均'] * passed_days - x['当前时点']
                                                         * left_days) / keep_days), axis=1)
    # 若基础户来款_时点保持 < 0，则基础户来款_时点保持为0
    data['基础户来款_时点保持'] = data.apply(lambda x: 0 if x['基础户来款_时点保持'] < 0 else x['基础户来款_时点保持'], axis=1)
    # 获取在目标日期外时点金额保持当前时点金额的预计来款金额
    data['有效户来款_时点保持'] = data.apply(lambda x: ((eff * total_days - x['当前年日均'] * passed_days - x['当前时点']
                                                         * left_days) / keep_days), axis=1)
    # 若有效户来款_时点保持 < 0，则有效户来款_时点保持为0
    data['有效户来款_时点保持'] = data.apply(lambda x: 0 if x['有效户来款_时点保持'] < 0 else x['有效户来款_时点保持'], axis=1)
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
#-----------------------------------------------------------------------------------------------------------------------
# 可复用方法，基数对比对应表格获取
# 获取基础户基于标识的降级情况表
def get_down_base_table(data):
    data = data[['客户名', '管户经理', '账户销户', '基础户降级_标识', '去年年日均', '当前年日均', '当前时点',
                 '旧基础户达标天数', '新基础户达标天数', '基础户来款_零时点', '基础户来款_时点保持']]
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
    data = data[['客户名', '管户经理', '账户销户', '基础户降级_年日均', '去年年日均', '当前年日均', '当前时点',
                 '旧基础户达标天数', '新基础户达标天数', '基础户来款_零时点', '基础户来款_时点保持']]
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
    data = data[['客户名', '管户经理', '基础户升级_标识', '去年年日均', '当前年日均', '当前时点',
                 '旧基础户达标天数', '新基础户达标天数', '有效户来款_零时点', '有效户来款_时点保持']]
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
    data = data[['客户名', '管户经理', '基础户升级_年日均', '去年年日均', '当前年日均', '当前时点',
                 '旧基础户达标天数', '新基础户达标天数', '有效户来款_零时点', '有效户来款_时点保持']]
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
    data = data[['客户名', '管户经理', '有效户升级_标识', '去年年日均', '当前年日均', '当前时点',
                 '旧有效户达标天数', '新有效户达标天数', '有效户来款_零时点', '有效户来款_时点保持']]
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
    data = data[['客户名', '管户经理', '有效户升级_年日均', '去年年日均', '当前年日均', '当前时点',
                 '旧有效户达标天数', '新有效户达标天数', '有效户来款_零时点', '有效户来款_时点保持']]
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
    data = data[['客户名', '管户经理', '账户销户', '有效户降级_标识', '去年年日均', '当前年日均', '当前时点',
                 '旧有效户达标天数', '新有效户达标天数', '有效户来款_零时点', '有效户来款_时点保持']]
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
    data = data[['客户名', '管户经理', '账户销户', '有效户降级_年日均', '去年年日均', '当前年日均', '当前时点',
                 '旧有效户达标天数', '新有效户达标天数', '有效户来款_零时点', '有效户来款_时点保持']]
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
    data = data[['客户名', '管户经理', '去年年日均', '当前年日均', '当前时点', '预警基础户', '基础户来款_零时点', '基础户来款_时点保持']]
    # 仅保留预警基础户信息
    data = data[data['预警基础户'] == 1]
    # 去除预警基础户列
    data.drop(columns=['预警基础户'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取预警有效户信息表
def get_warning_eff_table(data):
    # 仅保留有用列
    data = data[['客户名', '管户经理', '去年年日均', '当前年日均', '当前时点', '预警有效户', '有效户来款_零时点', '有效户来款_时点保持']]
    # 仅保留预警有效户信息
    data = data[data['预警有效户'] == 1]
    # 去除预警有效户列
    data.drop(columns=['预警有效户'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取临界基础户信息表
def get_critical_base_table(data):
    # 仅保留有用列
    data = data[['客户名', '管户经理', '去年年日均', '当前年日均', '当前时点', '基础户临界', '年日均基础户保持', '基础户来款_零时点',
                 '基础户来款_时点保持']]
    # 仅保留临界基础户信息
    data = data[data['基础户临界'] == 1]
    # 去除基础户临界列
    data.drop(columns=['基础户临界'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
    return data

# 获取临界有效户信息表
def get_critical_eff_table(data):
    # 仅保留有用列
    data = data[['客户名', '管户经理', '去年年日均', '当前年日均', '当前时点', '有效户临界', '年日均有效户保持', '有效户来款_零时点', '有效户来款_时点保持']]
    # 仅保留临界有效户信息
    data = data[data['有效户临界'] == 1]
    # 去除有效户临界列
    data.drop(columns=['有效户临界'], inplace=True)
    # 基于管户经理进行排序
    data = data.sort_values(by=['管户经理'])
    # 重设行索引
    data = data.reset_index(drop=True)
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
#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()