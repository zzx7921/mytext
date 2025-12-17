import pandas as pd
import streamlit as st
import os

def get_dataframe_from_excel():
    try:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        excel_file_path = os.path.join(desktop_path, "（商场销售数据）supermarket_sales.xlsx")
        
        # 新增 engine='openpyxl' 显式指定引擎
        df = pd.read_excel(
            excel_file_path,
            sheet_name='销售数据',
            skiprows=1,
            index_col='订单号',
            engine='openpyxl'  # 关键：指定解析xlsx的引擎
        )
        df['小时数'] = pd.to_datetime(df["时间"], format="%H:%M:%S").dt.hour
        return df
    except FileNotFoundError:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        st.error(f"未找到文件！请确认Excel在桌面，且文件名为：\n{desktop_path}\\（商场销售数据）supermarket_sales.xlsx")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"读取Excel出错：{str(e)}")
        return pd.DataFrame()

def add_sidebar_func(df):
    with st.sidebar:
        st.header("请筛选数据：")
        city_unique = df["城市"].unique()
        city = st.multiselect("请选择城市：", options=city_unique, default=city_unique)
        
        customer_type_unique = df["顾客类型"].unique()
        customer_type = st.multiselect("请选择顾客类型：", options=customer_type_unique, default=customer_type_unique)
        
        gender_unique = df["性别"].unique()
        gender = st.multiselect("请选择性别", options=gender_unique, default=gender_unique)
    
    df_selection = df.query("城市 == @city & 顾客类型 ==@customer_type & 性别 == @gender")
    return df_selection

if __name__ == "__main__":
    sale_df = get_dataframe_from_excel()
    if not sale_df.empty:
        df_selection = add_sidebar_func(sale_df)
        st.header('筛选后的数据')
        st.write(df_selection)
        st.write(f'筛选后的数据有 **{df_selection.shape[0]}** 行')
    else:
        st.warning("暂无数据可展示，请检查Excel文件！")
