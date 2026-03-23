# 导入包
import streamlit as st
import datetime
import pandas as pd
import io

def main():
    # 设置页面格式
    st.set_page_config(page_title='对公客户指标分析', page_icon='', layout='wide')

    # 设置一个网页侧边栏, 有两个页面选项, 一个是主页, 一个是总表
    st.sidebar.title('页面选项')
    selected_page = st.sidebar.radio('选择页面: ', ['主页', '总表', '基础户较上年升降级', '有效户较上年升降级', '预警及临界客户明细',
                                                    '客户较上年升降级情况汇总'])

    # 当用户选择主页时, 显示主页内容
    if selected_page == '主页':
        home_page()


# 设置主页内容
def home_page():
    # 为页面添加标题: 维明对公客户指标分析 居中
    st.markdown('<h1 style="text-align: center;">维明对公客户指标分析</h1>', unsafe_allow_html=True)
    # 创建一个标题, 请上传数据文件并进行相关参数设置
    st.markdown('<h2 style="text-align: center;">请上传数据文件并进行相关参数设置</h2>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
