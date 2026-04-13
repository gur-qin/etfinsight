import streamlit as st
import akshare as ak
import pandas as pd

# 页面基础配置
st.set_page_config(page_title="ETFInsight 智能终端", layout="wide")
st.title("🛡️ ETFInsight 智能投资辅助终端")

# --- 定义 Tabs ---
tab1, tab2, tab3 = st.tabs(["🔥 实时风险预警", "📈 策略回测中心", "⚡ 动量排序(20/25日)"])

# --- Tab 1 内容 ---
with tab1:
    st.write("这里是实时风险预警功能...")

# --- Tab 2 内容 ---
with tab2:
    st.write("这里是策略回测中心...")

# --- Tab 3 内容 ---
with tab3:
    st.subheader("动量强弱排序")
    input_codes = st.text_input("输入ETF代码(用逗号隔开)", "510300, 510500, 512100, 512880, 513100")
    code_list = [c.strip() for c in input_codes.split(',')]
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("计算20日动量排序"):
            st.write("20日动量排行计算中...")
    with col2:
        if st.button("计算25日动量排序"):
            st.write("25日动量排行计算中...")
            
    with st.expander("📖 动量策略说明文档 (点击展开)"):
        st.markdown("""
        ### 动量算法说明
        **核心公式**: `动量值 = (当前价格 - 历史价格) / 历史价格 * 100%`。
        **周期选择**: 短期周期 (20日/25日) 聚焦近期趋势，适合快速轮动。
        **优缺点**: 
        * **优点**: 计算简单、直观。
        * **缺点**: 未考虑波动率风险。可能会选出“高涨幅但高波动”的标的，在趋势反转时回撤风险较大。
        
        *建议: 在使用动量策略时，可结合仓位控制，并避开近期涨幅过大、波动率极高的品种。*
        """)
