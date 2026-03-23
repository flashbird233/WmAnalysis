import streamlit as st
import home_page

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
        home_page.main()

# 设置初始化变量
def init_variables():
    # 初始化数据集变量
    # 初始化去年底数据变量
    if 'last_year_file' not in st.session_state:
        st.session_state.last_year_file = None
    # 初始化之前数据变量
    if 'previous_file' not in st.session_state:
        st.session_state.previous_file = None
    # 初始化当前数据变量
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None

if __name__ == '__main__':
    main()