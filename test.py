'''''''''

    
    if st.button('生成', type='primary'):
        import cus_change
        cus_change.main()
        st.success('生成成功!')



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