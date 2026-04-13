import streamlit as st
import akshare as ak
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="ETFInsight 智能终端", layout="wide")
st.title("🛡️ ETFInsight 智能投资辅助终端")

# --- 定义 Tabs ---
tab1, tab2, tab3 = st.tabs(["🔥 实时风险预警", "📈 策略回测中心", "⚡ 动量排序(20/25日)"])

# --- Tab 1 & 2 占位 ---
with tab1:
    st.write("实时风险预警功能开发中...")
with tab2:
    st.write("策略回测中心开发中...")

# --- Tab 3 内容 ---
with tab3:
    st.subheader("动量强弱排序")
    input_codes = st.text_input("输入ETF代码(用逗号隔开)", "510300, 510500, 512100, 512880, 513100")
    code_list = [c.strip() for c in input_codes.split(',')]
    
    col1, col2 = st.columns(2)
    
    # 定义一个统一的计算函数，代码小白也能看懂
    def get_momentum(codes, days):
        data_list = []
        for code in codes:
            try:
                hist = ak.fund_etf_hist_em(symbol=code, period="daily", start_date="20250101")
                if len(hist) > days:
                    mom = (hist['收盘'].iloc[-1] - hist['收盘'].iloc[-days]) / hist['收盘'].iloc[-days] * 100
                    data_list.append({"代码": code, f"{days}日动量(%)": round(mom, 2)})
            except:
                continue
        return pd.DataFrame(data_list)

    with col1:
        if st.button("计算20日动量排序"):
            with st.spinner("正在计算..."):
                df = get_momentum(code_list, 20)
                if not df.empty:
                    st.dataframe(df.sort_values(by="20日动量(%)", ascending=False))
                else:
                    st.warning("未抓取到有效数据，请稍后再试。")

    with col2:
        if st.button("计算25日动量排序"):
            with st.spinner("正在计算..."):
                df = get_momentum(code_list, 25)
                if not df.empty:
                    st.dataframe(df.sort_values(by="25日动量(%)", ascending=False))
                else:
                    st.warning("未抓取到有效数据，请稍后再试。")

    with st.expander("📖 动量策略说明文档"):
        st.markdown("""
        ### 动量算法说明
        **核心公式**: 动量值 = (当前价格 - 历史价格) / 历史价格 * 100%
        **优缺点**: 优点是简单直观；缺点是未考虑波动率风险，高波动标的需谨慎。
        """)
