# 模块儿导入
import pandas as pd
import streamlit as st

#-----------------------------------------------------------------------------------------------------------------------
# 基数对比总表处理
# 基数对比总表处理主方法
def get_total_table():
    # 将file文件读取为DataFrame，第三行为表头
    file_to_data()
    # 获取或计算相关参数
    calc_params()
    # 标准化数据
    st.session_state.last_year_data, st.session_state.current_data = (
        standardize_data(st.session_state.last_year_data, st.session_state.current_data))
    # 合并数据
    st.session_state.total_table = merge_data(st.session_state.last_year_data, st.session_state.current_data)

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

#-----------------------------------------------------------------------------------------------------------------------
# 可复用方法
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
    return  data

#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    get_total_table()