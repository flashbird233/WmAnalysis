# 导入包
import streamlit as st
import datetime
import pandas as pd
import io


# 设置主页内容
def main():
    # 为页面添加标题：维明对公客户指标分析 居中
    st.markdown('<h1 style="text-align: center;">维明对公客户指标分析</h1>', unsafe_allow_html=True)
    # 创建一个标题，请上传数据文件并进行相关参数设置
    st.markdown('<h2 style="text-align: center;">请上传数据文件并进行相关参数设置</h2>', unsafe_allow_html=True)

    # 设置上传数据文件的输入框
    upload_file()


# 数据文件上传控件
def upload_file():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col2:
        # 让用户上传去年底数据，该数据文件需要从第四行开始读取
        last_year_file = st.file_uploader('请上传去年底数据文件：', type=['xlsx', 'xls'], key='uploader_last_year')
        # 判断用户是否上传了数据文件, 如果上传了数据文件，则保存数据文件
        if last_year_file is not None:
            st.session_state.last_year_file = last_year_file
        # 显示上传的文件名, 并显示上传状态
        if st.session_state.last_year_file:
            st.success(f"去年底数据：{st.session_state.last_year_file.name}")
        else:
            st.info("去年底数据：未上传")
    with col3:
        # 请用户上传之前数据文件，该数据文件需要从第四行开始读取
        previous_file = st.file_uploader('请上传之前数据文件：', type=['xlsx', 'xls'], key='uploader_previous')
        # 判断用户是否上传了数据文件, 如果上传了数据文件，则保存数据文件
        if previous_file is not None:
            st.session_state.previous_file = previous_file
        # 显示上传的文件名, 并显示上传状态
        if st.session_state.previous_file:
            st.success(f"之前数据：{st.session_state.previous_file.name}")
        else:
            st.info("之前数据：未上传")
    with col4:
        # 让用户上传当前数据文件，该数据文件需要从第四行开始读取
        current_file = st.file_uploader('请上传当前数据文件：', type=['xlsx', 'xls'], key='uploader_current')
        # 判断用户是否上传了数据文件, 如果上传了数据文件，则保存数据文件
        if current_file is not None:
            st.session_state.current_file = current_file
        # 显示上传的文件名, 并显示上传状态
        if st.session_state.current_file:
            st.success(f"当前数据：{st.session_state.current_file.name}")
        else:
            st.info("当前数据：未上传")


if __name__ == '__main__':
    main()

