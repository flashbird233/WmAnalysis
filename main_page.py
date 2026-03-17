import streamlit as st
import datetime

def main():
    # 设置页面格式和标题
    set_page_and_title()

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
    with col2:
        # 如果上述内容设定完毕，则用户点击生成按钮，则运行 cus_change.py
        if st.button('生成', type='primary'):
            # 检查文件是否已上传
            if last_year_data is None:
                st.error('❌ 请上传去年底数据文件！')
            elif current_data is None:
                st.error('❌ 请上传当前数据文件！')
            else:
                import cus_change
                total_table = cus_change.main(
                    base_data=last_year_data,
                    cur_data=current_data,
                    base_num=base_num,
                    eff_num=valid_num,
                    threshold_base_num=base_threshold,
                    threshold_eff_num=valid_threshold,
                    base_date=last_year_time,
                    current_date=current_time,
                    target_date=target_time,
                    tar_days=tar_days
                )
                st.success('生成成功！')

def set_page_and_title():
    # 设置页面格式
    st.set_page_config(page_title='维明对公客户指标分析', page_icon='', layout='wide')

    # 为页面添加标题: 维明对公客户指标分析 居中
    st.markdown('<h1 style="text-align: center;">维明对公客户指标分析</h1>', unsafe_allow_html=True)

    # 创建一个标题, 请上传数据文件并进行相关参数设置
    st.markdown('<h2 style="text-align: center;">请上传数据文件并进行相关参数设置</h2>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
