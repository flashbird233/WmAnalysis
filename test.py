'''''''''

    # 让用户选择去年时间
    last_year_time = st.date_input('请选择去年数据日期: ', datetime.date(2025, 12, 31))
    # 让用户选择业绩目标日期
    target_time = st.date_input('请选择业绩目标日期: ', datetime.date(2026, 3, 31))
    if st.button('生成', type='primary'):
        import cus_change
        cus_change.main()
        st.success('生成成功!')

with col3:
    # 让用户上传当前数据
    current_data = st.file_uploader('请上传当前数据: ', type=['xlsx', 'xls'])
    # 让用户选择当前时间
    current_time = st.date_input('请选择当前数据日期: ', datetime.date(2026, 3, 10))
    # 让用户设置目标来款天数, 默认为10天
    tar_days = st.number_input('请设置目标来款天数: ', value=10)
    # 如果上述内容设定完毕, 则用户点击生成按钮, 则运行cus_change.py

with col4:
    # 让客户设置基础户金额标准(单位元):
    base_num = st.number_input('请设置基础户金额标准(单位元): ', value=100000)
    # 让用户设置有效户金额标准(单位元):
    valid_num = st.number_input('请设置有效户金额标准(单位元): ', value=500000)
    # 请设置基础临界客户年日均标准(单位元):
    base_threshold = st.number_input('请设置基础户年日均标准(单位元): ', value=50000)
    # 请设置有效临界客户年日均标准(单位元):
    valid_threshold = st.number_input('请设置有效户年日均标准(单位元): ', value=400000)
''''''