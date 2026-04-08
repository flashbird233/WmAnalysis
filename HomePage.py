# 导入包
import streamlit as st
import datetime
import pandas as pd
import io

import DataProcessing


#-----------------------------------------------------------------------------------------------------------------------
# 主页页面主方法，设置主页内容
def main():
    # 为页面添加标题：维明对公客户指标分析 居中
    st.markdown('<h1 style="text-align: center;">对公客户指标分析</h1>', unsafe_allow_html=True)

    # 分割页面
    st.write('---')

    # 数据文件上传
    # 创建一个标题，请上传数据文件并进行相关参数设置
    st.markdown('<h3 style="text-align: center;">请上传相关数据文件</h3>', unsafe_allow_html=True)
    # 设置上传数据文件的输入框
    upload_file()

    # 分割页面
    st.write('---')

    # 其他参数上传
    # 创建一个标题，请用户进行相关参数设置
    st.markdown('<h3 style="text-align: center;">请确定默认值，或更改相关参数</h3>', unsafe_allow_html=True)
    # 其他参数设置
    other_parameters()

    # 分割页面
    st.write('---')
    # 生成按钮
    generage_button()

#-----------------------------------------------------------------------------------------------------------------------
# 页面内容次方法
# 生成按钮和数据处理
def generage_button():
    # 点击生成按钮，进行数据处理
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with (col4):
        # 如果上述内容设定完毕，则用户点击生成按钮，则运行 cus_change.py
        if st.button('生成', type='primary'):
            # 检查文件是否已上传
            if st.session_state.last_year_file is None:
                st.error('❌ 请上传去年底数据文件！')
            elif st.session_state.current_file is None:
                st.error('❌ 请上传当前数据文件！')
            else:
                DataProcessing.main()
                st.success('生成成功！点击左侧侧边栏查看表格')

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

# 其他参数上传控件
def other_parameters():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col2:
        # 请用户选择去年数据日期, 默认为去年12月31日
        st.session_state.last_year_date = st.date_input('请选择去年数据日期：', st.session_state.last_year_date)
        # 请用户输入基础户达标年日均金额标准, 默认为100000
        st.session_state.base_standard = st.number_input('请设置基础户年日均标准(元): ',
                                                         value=st.session_state.base_standard)
        # 请用户输入来款天数变量，默认为10
        st.session_state.keep_days = st.number_input('请设置来款天数标准(天): ',
                                                     value = st.session_state.keep_days)

    with col3:
        # 请用户选择之前数据日期，默认为当前日期前三天
        st.session_state.previous_date = st.date_input('请选择之前数据日期：', st.session_state.previous_date)
        # 请用户输入有效户达标年日均金额标准, 默认为有效户标准的当前值
        st.session_state.eff_standard = st.number_input('请设置有效户年日均标准(元): ',
                                                        value=st.session_state.eff_standard)

    with col4:
        # 请用户选择当前数据日期, 默认为当前日期前两天
        st.session_state.current_date = st.date_input('请选择当前数据日期：', st.session_state.current_date)
        # 请用户输入基础户临界金额标准, 默认为70000
        st.session_state.base_critical_standard = st.number_input('请设置基础户临界标准(元): ',
                                                                  value=st.session_state.base_critical_standard)

    with col5:
        # 请用户选择考核截止日期, 默认为当前当前季度的最后一天
        st.session_state.ass_end_date = st.date_input('请选择考核截止日期：',
                                                             st.session_state.ass_end_date)
        # 请用户输入有效户临界金额标准, 默认为400000
        st.session_state.eff_critical_standard = st.number_input('请设置有效户临界标准(元): ',
                                                                 value=st.session_state.eff_critical_standard)
#-----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()

