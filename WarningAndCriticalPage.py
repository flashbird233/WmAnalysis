import streamlit as st
import io
import pandas as pd

def main(warning_and_critical_dict):
    st.markdown('<h2 style="text-align: center;">预警及临界客户</h2>', unsafe_allow_html=True)
    # 检查是否有数据
    if not warning_and_critical_dict or len(warning_and_critical_dict) == 0:
        st.warning('⚠️ 暂无数据，请先在主页上传数据文件并点击"生成"按钮')
        return
    # 将alarm_and_threshold_dict这个字典转化为Excel文件供客户下载, Sheet名为key, data为value
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for key, value in warning_and_critical_dict.items():
            value.to_excel(writer, index=False, sheet_name=key)

    # 下载Excel文件
    st.download_button(
        label='下载预警及临界客户明细表',
        data=buffer.getvalue(),
        file_name='预警及临界客户明细表.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # 接下来轮流显示每个Sheet
    for key, value in warning_and_critical_dict.items():
        st.markdown(f'<h3 style="text-align: center;">{key}</h3>', unsafe_allow_html=True)
        st.dataframe(value)
        st.markdown('---')