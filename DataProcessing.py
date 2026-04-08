# 模块儿导入
import pandas as pd
import streamlit as st

#-----------------------------------------------------------------------------------------------------------------------
# 总表处理
# 总表处理主方法
def get_total_table():
    # 将file文件读取为DataFrame，第三行为表头
    st.session_state.previous_data = pd.read_excel(st.session_state.previous_file, header=3)
    print(st.session_state.previous_data)



#-----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    get_total_table()