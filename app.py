import streamlit as st 
import akshare as ak 
import pandas as pd 
import plotly.graph_objects as go 
from datetime import datetime, timedelta 

# 页面基础配置 
st.set_page_config(page_title="ETFInsight.top 智能终端", layout="wide") 

# --- 数据获取函数 --- 
@st.cache_data(ttl=3600) 
def load_all_etf_spot(): 
    return ak.fund_etf_spot_em() 

def get_hist_data(code, start_date): 
    try: 
        df = ak.fund_etf_hist_em(symbol=code, period="daily", start_date=start_date.strftime('%Y%m%d')) 
        return df[['日期', '收盘']].rename(columns={'收盘': code}) 
    except: 
        return None 

# --- UI 界面 --- 
st.title("🛡️ ETFInsight 智能投资辅助终端") 
st.caption("域名：etfinsight.top | 驱动：AI & 量化数据") 

# 侧边栏设置 
st.sidebar.header("控制台") 
premium_threshold = st.sidebar.slider("溢价预警阈值 (%)", 0.5, 5.0, 1.5) 
backtest_codes = st.sidebar.text_input("回测组合(代码用逗号隔开)", "510300, 510500, 512100") 
days = st.sidebar.selectbox("回测时长", [180, 365, 730], index=1) 

tab1, tab2 = st.tabs(["🔥 实时风险预警", "📈 策略回测中心"]) 

# --- Tab 1: 实时预警逻辑 --- 
with tab1: 
    st.subheader("高溢价 ETF 实时雷达") 
    with st.spinner("正在扫描全市场数据..."): 
        all_data = load_all_etf_spot() 
        
        # 自动识别折价/溢价率相关的列名
        target_col = '折价率' 
        if target_col not in all_data.columns: 
            possible_cols = [c for c in all_data.columns if '折价' in c or '溢价' in c] 
            if possible_cols: 
                target_col = possible_cols[0] 
            else: 
                st.error(f"无法找到相关列，当前列名有: {all_data.columns.tolist()}") 
                st.stop() 
        
        # 使用正确的列名进行筛选
        high_premium = all_data[all_data[target_col].astype(float) > premium_threshold].copy() 
        
        if not high_premium.empty: 
            st.error(f"警告：检测到 {len(high_premium)} 只标的处于高溢价状态！") 
            st.dataframe(high_premium[['代码', '名称', '最新价', target_col, '成交额']], use_container_width=True) 
        else: 
            st.success("全市场主流 ETF 溢价水平暂处于安全区间。") 

# --- Tab 2: 回测系统 --- 
with tab2: 
    st.subheader("等权组合历史表现") 
    if st.button("开始运行回测"): 
        code_list = [c.strip() for c in backtest_codes.split(',')] 
        start_dt = datetime.now() - timedelta(days=days) 
        combined_df = pd.DataFrame() 
        with st.spinner("正在对齐历史净值..."): 
            for code in code_list: 
                hist = get_hist_data(code, start_dt) 
                if hist is not None: 
                    hist['日期'] = pd.to_datetime(hist['日期']) 
                    if combined_df.empty: 
                        combined_df = hist 
                    else: 
                        combined_df = pd.merge(combined_df, hist, on='日期', how='outer') 
            
            if not combined_df.empty: 
                combined_df.set_index('日期', inplace=True) 
                # 归一化计算 
                norm_df = combined_df.ffill() / combined_df.ffill().iloc[0] 
                combined_df['组合净值'] = norm_df.mean(axis=1) 
                
                # 画图 
                fig = go.Figure() 
                fig.add_trace(go.Scatter(x=combined_df.index, y=combined_df['组合净值'], name="我的组合", line=dict(color='red', width=2))) 
                st.plotly_chart(fig, use_container_width=True) 
                final_return = (combined_df['组合净值'].iloc[-1] - 1) * 100 
                st.metric("累计收益率", f"{final_return:.2f}%") 
            else: 
                st.warning("未能获取有效数据，请检查代码输入。") 

st.divider() 
st.markdown("#### 免责声明\n本工具仅供技术参考，不构成任何投资建议。")
