import streamlit as st

def main():
    st.markdown('<h1 style="text-align: center;">总表数据</h1>', unsafe_allow_html=True)
    st.write('---')

    # 检查数据是否存在
    if "last_year_data" not in st.session_state or st.session_state.last_year_data is None:
        st.warning("⚠️ 去年数据尚未加载，请先在主页上传文件并点击生成按钮")
        return

    # 显示去年数据
    st.subheader("去年底数据")
    st.dataframe(st.session_state.last_year_data, use_container_width=True)