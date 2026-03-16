import streamlit as st
import datetime

def main():
    # 设置页面格式
    st.set_page_config(page_title='维明对公客户指标分析', page_icon='', layout='wide')

    # 为页面添加标题: 维明对公客户指标分析 居中
    st.markdown('<h1 style="text-align: center;">维明对公客户指标分析</h1>', unsafe_allow_html=True)

    # 创建一个标题, 请上传数据文件并进行相关参数设置
    st.markdown('<h2 style="text-align: center;">请上传数据文件并进行相关参数设置</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col2:
        # 让用户上传去年底数据
        last_year_data = st.file_uploader('请上传去年底数据: ', type=['xlsx', 'xls'])
        # 让用户选择去年时间
        last_year_time = st.date_input('请选择去年数据日期: ', datetime.date(2025, 12, 31))
        # 让用户选择业绩目标日期
        target_time = st.date_input('请选择业绩目标日期: ', datetime.date(2026, 3, 31))

if __name__ == '__main__':
    main()
