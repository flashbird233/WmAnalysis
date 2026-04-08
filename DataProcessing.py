# 模块儿导入
import pandas as pd
import streamlit as st

#-----------------------------------------------------------------------------------------------------------------------
# 基数对比总表处理
# 基数对比总表处理主方法
def get_total_table():
    # 将file文件读取为DataFrame，第三行为表头
    main_to_data()

    # 获取或计算相关参数
    calc_params()

# 基数对比总表次方法
# 将file文件读取为DataFrame，第三行为表头
def main_to_data():
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


if __name__ == '__main__':
    get_total_table()