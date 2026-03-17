import streamlit as st
import datetime
import pandas as pd
import io

def main():
    # 设置页面格式
    st.set_page_config(page_title='维明对公客户指标分析', page_icon='', layout='wide')

    # 设置一个网页侧边栏, 有两个页面选项, 一个是主页, 一个是总表
    st.sidebar.title('页面选项')
    selected_page = st.sidebar.radio('选择页面: ', ['主页', '总表', '基础户升降级明细', '有效户升降级明细', '预警及临界客户明细'])
    # 初始化变量
    if 'total_table' not in st.session_state:
        st.session_state.total_table = pd.DataFrame()
    if 'base_change_detail' not in st.session_state:
        st.session_state.base_change_detail = {}
    if 'value_change_detail' not in st.session_state:
        st.session_state.value_change_detail = {}
    if 'alarm_and_threshold_detail' not in st.session_state:
        st.session_state.alarm_and_threshold_detail = {}
    # 当用户选择主页时, 显示主页内容
    if selected_page == '主页':
        home_page()
    # 当用户选择总表时, 显示总表内容
    elif selected_page == '总表':
        total_table_page(st.session_state.total_table)
    elif selected_page == '基础户升降级明细':
        base_change_detail_page(st.session_state.base_change_detail)
    elif selected_page == '有效户升降级明细':
        value_change_detail_page(st.session_state.value_change_detail)
    elif selected_page == '预警及临界客户明细':
        alarm_and_threshold_detail_page(st.session_state.alarm_and_threshold_detail)


def home_page():
    # 为页面添加标题: 维明对公客户指标分析 居中
    st.markdown('<h1 style="text-align: center;">维明对公客户指标分析</h1>', unsafe_allow_html=True)

    # 创建一个标题, 请上传数据文件并进行相关参数设置
    st.markdown('<h2 style="text-align: center;">请上传数据文件并进行相关参数设置</h2>', unsafe_allow_html=True)

    # 用户数据录入
    col1, col2, col3, col4, col5 = st.columns(5)
    with col2:
        # 让用户上传去年底数据, 该数据文件需要从第四行开始读取
        last_year_data = st.file_uploader('请上传去年底数据: ', type=['xlsx', 'xls'])
        # 让用户选择去年时间
        last_year_time = st.date_input('请选择去年数据日期: ', datetime.date(2025, 12, 31))
        # 让用户选择业绩目标日期
        target_time = st.date_input('请选择业绩目标日期: ', datetime.date(2026, 3, 31))

    with col3:
        # 让用户上传当前数据
        current_data = st.file_uploader('请上传当前数据: ', type=['xlsx', 'xls'])
        # 让用户选择当前时间
        current_time = st.date_input('请选择当前数据日期: ', datetime.date(2026, 3, 10))
        # 让用户设置目标来款天数, 默认为10天
        tar_days = st.number_input('请设置目标来款天数: ', value=10)


    with col4:
        # 让客户设置基础户金额标准(单位元):
        base_num = st.number_input('请设置基础户金额标准(单位元): ', value=100000)
        # 让用户设置有效户金额标准(单位元):
        valid_num = st.number_input('请设置有效户金额标准(单位元): ', value=500000)
        # 请设置基础临界客户年日均标准(单位元):
        base_threshold = st.number_input('请设置基础户年日均标准(单位元): ', value=50000)
        # 请设置有效临界客户年日均标准(单位元):
        valid_threshold = st.number_input('请设置有效户年日均标准(单位元): ', value=400000)

    col1, col2, col3 = st.columns(3)
    with (col2):
        # 如果上述内容设定完毕，则用户点击生成按钮，则运行 cus_change.py
        if st.button('生成', type='primary'):
            # 检查文件是否已上传
            if last_year_data is None:
                st.error('❌ 请上传去年底数据文件！')
            elif current_data is None:
                st.error('❌ 请上传当前数据文件！')
            else:
                import cus_change
                st.session_state.total_table, st.session_state.base_change_detail, st.session_state.value_change_detail, st.session_state.alarm_and_threshold_detail = cus_change.main(
                    base_data=last_year_data,
                    cur_data=current_data,
                    base_num=base_num,
                    eff_num=valid_num,
                    base_date=last_year_time,
                    current_date=current_time,
                    target_date=target_time,
                    tar_days=tar_days,
                    threshold_base_num=base_threshold,
                    threshold_eff_num=valid_threshold
                )
                st.success('生成成功！点击左侧侧边栏查看表格')

def total_table_page(total_table):
    # 以下是总表内容, 可以根据总表内容产出相关表格
    st.markdown('<h1 style="text-align: center;">维明对公客户指标分析</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">总表</h2>', unsafe_allow_html=True)

    # 方法 1：使用 BytesIO 创建内存中的 Excel 文件
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        total_table.to_excel(writer, index=False, sheet_name='总表')

    st.download_button(
        label='下载总表',
        data=buffer.getvalue(),
        file_name='总表.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    st.dataframe(total_table)


def base_change_detail_page(base_change_dict):
    st.markdown('<h1 style="text-align: center;">维明对公客户指标分析</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">基础户升降级明细</h2>', unsafe_allow_html=True)

    # 检查是否有数据
    if not base_change_dict or len(base_change_dict) == 0:
        st.warning('⚠️ 暂无数据，请先在主页上传数据文件并点击"生成"按钮')
        return

    # 将base_change_dict这个字典转化为Excel文件供客户下载, Sheet名为key, data为value
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for key, value in base_change_dict.items():
            value.to_excel(writer, index=False, sheet_name=key)

    # 下载Excel文件
    st.download_button(
        label='下载基础户升降级明细表',
        data=buffer.getvalue(),
        file_name='基础户升降级明细表.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # 接下来轮流显示每个Sheet
    for key, value in base_change_dict.items():
        st.markdown(f'<h3 style="text-align: center;">{key}</h3>', unsafe_allow_html=True)
        st.dataframe(value)
        st.markdown('---')

def value_change_detail_page(value_change_dict):
    st.markdown('<h1 style="text-align: center;">维明对公客户指标分析</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">有效户升降级明细</h2>', unsafe_allow_html=True)
    # 检查是否有数据
    if not value_change_dict or len(value_change_dict) == 0:
        st.warning('⚠️ 暂无数据，请先在主页上传数据文件并点击"生成"按钮')
        return
    # 将value_change_dict这个字典转化为Excel文件供客户下载, Sheet名为key, data为value
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for key, value in value_change_dict.items():
            value.to_excel(writer, index=False, sheet_name=key)

    # 下载Excel文件
    st.download_button(
        label='下载有效户升降级明细表',
        data=buffer.getvalue(),
        file_name='有效户升降级明细表.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # 接下来轮流显示每个Sheet
    for key, value in value_change_dict.items():
        st.markdown(f'<h3 style="text-align: center;">{key}</h3>', unsafe_allow_html=True)
        st.dataframe(value)
        st.markdown('---')

def alarm_and_threshold_detail_page(alarm_and_threshold_dict):
    st.markdown('<h1 style="text-align: center;">维明对公客户指标分析</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">异常及阈值明细</h2>', unsafe_allow_html=True)
    # 检查是否有数据
    if not alarm_and_threshold_dict or len(alarm_and_threshold_dict) == 0:
        st.warning('⚠️ 暂无数据，请先在主页上传数据文件并点击"生成"按钮')
        return
    # 将alarm_and_threshold_dict这个字典转化为Excel文件供客户下载, Sheet名为key, data为value
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for key, value in alarm_and_threshold_dict.items():
            value.to_excel(writer, index=False, sheet_name=key)

    # 下载Excel文件
    st.download_button(
        label='下载异常及阈值明细表',
        data=buffer.getvalue(),
        file_name='异常及阈值明细表.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # 接下来轮流显示每个Sheet
    for key, value in alarm_and_threshold_dict.items():
        st.markdown(f'<h3 style="text-align: center;">{key}</h3>', unsafe_allow_html=True)
        st.dataframe(value)
        st.markdown('---')


if __name__ == '__main__':
    main()
