# 导入包
import streamlit as st
import datetime
import pandas as pd
import io


# 设置主页内容
def main():
    # 为页面添加标题: 维明对公客户指标分析 居中
    st.markdown('<h1 style="text-align: center;">维明对公客户指标分析</h1>', unsafe_allow_html=True)
    # 创建一个标题, 请上传数据文件并进行相关参数设置
    st.markdown('<h2 style="text-align: center;">请上传数据文件并进行相关参数设置</h2>', unsafe_allow_html=True)

    # 设置上传数据文件的输入框
    col1, col2, col3, col4, col5 = st.columns(5)
    with col2:
        # 让用户上传去年底数据, 该数据文件需要从第四行开始读取
        st.session_state.last_year_data = st.file_uploader('请上传去年底数据文件: ', type=['xlsx', 'xls'])
    with col3:
        # 请用户上传之前数据文件, 该数据文件需要从第四行开始读取
        st.session_state.previous_data = st.file_uploader('请上传之前数据文件: ', type=['xlsx', 'xls'])
    with col4:
        # 让用户上传当前数据文件, 该数据文件需要从第四行开始读取
        st.session_state.current_data = st.file_uploader('请上传当前数据文件: ', type=['xlsx', 'xls'])


if __name__ == '__main__':
    main()
