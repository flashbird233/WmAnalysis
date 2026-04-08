# 导入模块儿
import streamlit as st
import datetime

# 导入页面
import HomePage  # 主页
import TotalTablePage  # 总表页面

#-----------------------------------------------------------------------------------------------------------------------
# 网站主方法
def main():
    # 设置页面格式
    st.set_page_config(page_title='对公客户指标分析', page_icon='', layout='wide')

    # 初始化变量
    init_variables()

    # 设置一个网页侧边栏, 有两个页面选项, 一个是主页, 一个是总表
    selected_page = st.sidebar.radio('', ['主页', '总表', '基础户较上年升降级', '有效户较上年升降级', '预警及临界客户明细',
                                                    '客户较上年升降级情况汇总'])

    # 当用户选择主页时, 显示主页内容
    if selected_page == '主页':
        HomePage.main()
    # 当用户选择总表时, 显示总表内容
    elif selected_page == '总表':
        TotalTablePage.main()

#-----------------------------------------------------------------------------------------------------------------------
# 初始化变量
# 初始化变量主方法
def init_variables():
    # 初始化数据集文件变量
    # 初始化去年底数据文件变量
    if 'last_year_file' not in st.session_state:
        st.session_state.last_year_file = None
    # 初始化之前数据文件变量
    if 'previous_file' not in st.session_state:
        st.session_state.previous_file = None
    # 初始化当前数据文件变量
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None

    # 初始化数据集变量
    # 初始化去年数据变量
    if 'last_year_data' not in st.session_state:
        st.session_state.last_year_data = None
    # 初始化之前数据变量
    if 'previous_data' not in st.session_state:
        st.session_state.previous_data = None
    # 初始化当前数据变量
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None


    # 初始化数据集日期变量
    # 初始化年底数据日期变量, 默认为去年年底
    if 'last_year_date' not in st.session_state:
        current_year = datetime.date.today().year  # 获取当前年份
        # 初始化last_year_date变量为去年年底日期
        st.session_state.last_year_date = datetime.date(current_year - 1, 12, 31)
    # 初始化之前数据日期变量, 默认为当前日期前三日
    if 'previous_date' not in st.session_state:
        st.session_state.previous_date = datetime.date.today() - datetime.timedelta(days=3)
    # 初始化当前数据日期变量, 默认为当前日期前两日
    if 'current_date' not in st.session_state:
        st.session_state.current_date = datetime.date.today() - datetime.timedelta(days=2)
    # 初始化考核截止日期变量, 默认为当前当前季度的最后一天
    if 'ass_end_date' not in st.session_state:
        st.session_state.ass_end_date = get_quarter_end_date(datetime.date.today())

    # 初始化各项标准变量
    # 初始化基础户标准变量, 默认为100000
    if 'base_standard' not in st.session_state:
        st.session_state.base_standard = 100000
    # 初始化有效户标准变量, 默认为500000
    if 'effective_standard' not in st.session_state:
        st.session_state.effective_standard = 500000
    # 初始化基础户临界标准变量, 默认为70000
    if 'base_critical_standard' not in st.session_state:
        st.session_state.base_critical_standard = 70000
    # 初始化有效户临界标准变量, 默认为400000
    if 'effective_critical_standard' not in st.session_state:
        st.session_state.effective_critical_standard = 400000

    # 初始化客户经理列表变量
    if 'manager_list' not in st.session_state:
        st.session_state.manager_list = None

# 获取指定日期所在季度的最后一天
def get_quarter_end_date(date):
    """获取指定日期所在季度的最后一天"""
    # 计算当前月份所在的季度
    quarter = (date.month - 1) // 3 + 1
    # 计算季度最后一个月的月份
    quarter_last_month = quarter * 3
    # 获取该月的天数(通过下个月第一天减一天得到)
    if quarter_last_month == 12:
        next_year = date.year + 1
        next_month_first_day = datetime.date(next_year, 1, 1)
    else:
        next_month_first_day = datetime.date(date.year, quarter_last_month + 1, 1)

    # 季度最后一天 = 下个月第一天 - 1天
    quarter_end = next_month_first_day - datetime.timedelta(days=1)
    return quarter_end
#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()