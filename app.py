import streamlit as st
import pandas as pd

# 1. 網頁基礎設定
st.set_page_config(page_title="億萬富豪の退休航道 v5.5", layout="wide")

# 2. 套用深色高質感風格 CSS
st.markdown("""
    <style>
    .main { background-color: #1A1C2C; color: white; }
    /* 移除頂部不必要的空隙 */
    .block-container { padding-top: 2rem; }
    /* 按鈕樣式：橘底黑字，針對手機操作加高 */
    .stButton>button { 
        background-color: #F7931A; 
        color: black; 
        font-weight: bold; 
        width: 100%; 
        border-radius: 10px; 
        height: 3.5em; 
        font-size: 22px !important; 
        border: none;
    }
    /* 卡片式數據顯示 */
    .stMetric { background-color: #2D3047; padding: 15px; border-radius: 10px; border: 1px solid #4E5481; }
    div[data-testid="stExpander"] { background-color: #2D3047; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 頂部標題：使用 subheader 確保與下方階段規劃的字體一模一樣大
st.subheader("🚀 億萬富豪の退休航道 💵")

# 4. 金額格式化函數
def format_wealth(amount):
    wan = amount / 10000
    if wan >= 10000:
        yi = int(wan // 10000)
        rem_wan = int(wan % 10000)
        return f"{yi} 億 {rem_wan:,} 萬" if rem_wan != 0 else f"{yi} 億"
    return f"{int(wan):,} 萬"

# 5. --- 基礎設定區 ---
with st.expander("🛠 基礎設定與起始資產", expanded=True):
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        total_yrs = st.number_input("總投資年限", value=30, step=1)
    with col2:
        q_rate = st.number_input("QQQ 年報 (%)", value=13.0)
        init_q = st.number_input("QQQ 起始資金", value=0)
    with col3:
        b_rate = st.number_input("BTC 年報 (%)", value=28.0)
        init_b = st.number_input("BTC 起始資金", value=300000)

# 6. --- 階段投入區 (6 階段) ---
st.subheader("📅 階段性投入規劃 (共 6 階段)")
adj_data = []

container = st.container()
with container:
    h_cols = st.columns([1, 1.5, 1.5])
    h_cols[0].caption("開始年份")
    h_cols[1].caption("QQQ 每月投入")
    h_cols[2].caption("BTC 每月投入")

    for i in range(6):
        r_cols = st.columns([1, 1.5, 1.5])
        with r_cols[0]:
            y_val = "1" if i == 0 else ""
            y = st.text_input(f"Y", value=y_val, key=f"y{i}", label_visibility="collapsed", placeholder="年份")
        with r_cols[1]:
            q_val = "10000" if i == 0 else ""
            q = st.text_input(f"Q", value=q_val, key=f"q{i}", label_visibility="collapsed", placeholder="QQQ額度")
        with r_cols[2]:
            b_val = "15000" if i == 0 else ""
            b = st.text_input(f"B", value=b_val, key=f"b{i}", label_visibility="collapsed", placeholder="BTC額度")
        
        if y and (q or b):
            try:
                adj_data.append((int(y), float(q) if q else 0, float(b) if b else 0))
            except:
                pass

# 7. --- 計算按鈕與邏輯 ---
st.write("---")
if st.button("💰財富自由我來了🏆"):
    q_r = (1 + q_rate/100)**(1/12)-1
    b_r = (1 + b_rate/100)**(1/12)-1
    
    plan = {}
    current_q, current_b = 0.0, 0.0
    adj_data.sort()
    
    idx = 0
    for y in range(1, total_yrs + 1):
        if idx < len(adj_data) and y >= adj_data[idx][0]:
            current_q = adj_data[idx][1]
            current_b = adj_data[idx][2]
            idx += 1
        plan[y] = (current_q, current_b)

    results = []
    q_total, b_total = float(init_q), float(init_b)
    total_cost = q_total + b_total
    prev_total = 0.0

    for y in range(1, total_yrs + 1):
        qp, bp = plan[y]
        total_cost += (qp + bp) * 12
        for _ in range(12):
            q_total = (q_total + qp) * (1 + q_r)
            b_total = (b_total + bp) * (1 + b_r)
        
        grand = q_total + b_total
        growth = f"{(grand/prev_total-1)*100:.1f}%" if prev_total > 0 else "--"
        results.append({
            "年份": f"Y{y:02}",
            "累計成本": format_wealth(total_cost),
            "QQQ 市值": format_wealth(q_total),
            "BTC 市值": format_wealth(b_total),
            "總資產": format_wealth(grand),
            "年增率": growth
        })
        prev_total = grand

    # 結算報告
    st.success(f"🎉 第 {total_yrs} 年航道結算結果✨")
    c1, c2, c3 = st.columns(3)
    c1.metric("總成本", format_wealth(total_cost))
    c2.metric("淨獲利", format_wealth(grand - total_cost))
    c3.metric("最終資產", format_wealth(grand))

    # 詳細表格
    st.write("### 📈 歷年資產成長細節")
    st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
