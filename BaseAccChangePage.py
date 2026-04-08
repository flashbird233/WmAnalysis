import streamlit as st
import io
import pandas as pd

def main(base_change_dict):
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

    st.markdown('---')

    # 接下来轮流显示每个Sheet
    for key, value in base_change_dict.items():
        st.markdown(f'<h3 style="text-align: center;">{key}</h3>', unsafe_allow_html=True)
        st.dataframe(value)
        st.markdown('---')