# --- Tab 3: 动量排序核心功能 ---
with tab3:
    st.subheader("动量强弱排序")
    input_codes = st.text_input("输入ETF代码(用逗号隔开)", "510300, 510500, 512100, 512880, 513100")
    code_list = [c.strip() for c in input_codes.split(',')]
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("计算20日动量排序"):
            df_20 = calculate_momentum(code_list, 20)
            st.write("20日动量排行：")
            st.dataframe(df_20, use_container_width=True)
    with col2:
        if st.button("计算25日动量排序"):
            df_25 = calculate_momentum(code_list, 25)
            st.write("25日动量排行：")
            st.dataframe(df_25, use_container_width=True)
            
    # --- 策略文档区域 ---
    with st.expander("📖 动量策略说明文档 (点击展开)"):
        st.markdown("""
        ### 动量算法说明
        **核心公式**：`动量值 = (当前价格 - 历史价格) / 历史价格 × 100%`，即特定周期的涨跌幅。

        **周期选择**：
        * **短期周期 (20日/25日)**：聚焦近期趋势，适合捕捉市场快速轮动机会。
        * **中长期周期**：更反映趋势的持续性，能过滤短期杂波。

        **优缺点分析**：
        * **优点**：计算简单、直观易懂，是入门量化策略的最佳实践。
        * **缺点**：未考虑波动率风险。可能会选出“高涨幅但高波动”的标的，在趋势反转时回撤风险较大。
        
        *建议：在使用动量策略时，可结合仓位控制，并避开近期涨幅过大、波动率极高的品种。*
        """)
