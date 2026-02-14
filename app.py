import streamlit as st
import random
import time
import os

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="購物體驗研究", layout="centered")

# --- 2. CSS 美化 (含內部訊號樣式) ---
st.markdown("""
<style>
    /* 按鈕樣式 */
    .stButton > button {
        background-color: #FF5722;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
        border: none;
    }
    .stButton > button:hover {
        background-color: #E64A19;
    }
    
    /* 價格標籤 */
    .price-tag {
        color: #d32f2f;
        font-size: 1.8em;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
    }
    
    /* 內部訊號 (Internal Signal) 專用的文字框樣式 */
    .internal-signal-box {
        background-color: #f1f8e9; /* 淡綠色背景 */
        border: 1px dashed #8bc34a; /* 綠色虛線框 */
        padding: 10px;
        border-radius: 5px;
        font-size: 0.9em;
        color: #2e7d32;
        text-align: center;
        margin-top: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* 外部訊號圖片容器 */
    .external-badge-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 核心邏輯：狀態管理 ---
def go_to_step(next_step):
    st.session_state['step'] = next_step

if 'step' not in st.session_state:
    # === 實驗設計：2x2 ===
    # Security: External (外部認證圖) vs. Internal (內部聲明文)
    # Involvement: High (筆電) vs. Low (原子筆)
    security_levels = ['External', 'Internal']
    involvement_levels = ['High', 'Low']
    
    # 隨機分派
    st.session_state['security'] = random.choice(security_levels)
    st.session_state['involvement'] = random.choice(involvement_levels)
    
    st.session_state['step'] = 'consent'

# --- 4. 介面渲染函數 ---
def render_ecommerce_page(security, involvement):
    st.markdown("---")
    
    # === Header 區域 (Logo + 資安訊號) ===
    col1, col2 = st.columns([1.5, 1.5]) 
    with col1:
        st.markdown("## 🛒 SuperStore 旗艦店")
    
    with col2:
        # === [自變數 1] 資安訊號操弄 ===
        if security == 'External':
            # --- 強訊號：外部認證 (使用圖片) ---
            # 注意：檔名大小寫必須完全吻合
            cert_img = "cert_badges.PNG" 
            
            if os.path.exists(cert_img):
                st.markdown('<div class="external-badge-container">', unsafe_allow_html=True)
                st.image(cert_img, width=180) # 調整寬度以適應版面
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # 防呆：如果圖片沒上傳成功，顯示錯誤提示
                st.error(f"圖片讀取失敗：{cert_img}")
                st.caption("請確認 GitHub 檔名是否為 cert_badges.PNG (注意大寫)")
                
        elif security == 'Internal':
            # --- 弱訊號：內部聲明 (使用 CSS 樣式框) ---
            # 模擬廠商自己寫的承諾 (Cheap Talk)
            st.markdown("""
            <div class="internal-signal-box">
                🛡️ <b>官方資安聲明</b><br>
                <span style="font-size:0.85em;">
                本站採用嚴格加密技術<br>
                承諾保護您的個人隱私
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    # === 商品區域 (產品涉入度操弄) ===
    prod_c1, prod_c2 = st.columns([1, 1.2])
    
    with prod_c1:
        # === [自變數 2] 產品涉入度操弄 ===
        if involvement == 'High':
            # 高涉入：筆電
            img_file = "Lp.AVIF"  # 檔名需與 GitHub 一致
            title = "ProBook X1 商務筆電"
            desc = "AI 運算核心 / 32GB RAM / 1TB SSD / 適合高階商務人士"
            price = "NT$ 45,900"
        else:
            # 低涉入：原子筆
            img_file = "Pen.jpg"  # 檔名需與 GitHub 一致
            title = "極簡風格中性筆 (3入)"
            desc = "0.5mm 滑順筆觸 / 速乾墨水 / 學生與辦公室必備"
            price = "NT$ 150"
            
        # 顯示商品圖
        if os.path.exists(img_file):
            st.image(img_file, use_container_width=True)
        else:
            st.warning(f"缺少圖片: {img_file}")

    with prod_c2:
        st.markdown(f"### {title}")
        st.caption(desc)
        st.markdown(f"<div class='price-tag'>{price}</div>", unsafe_allow_html=True)
        st.write("---")
        
        # 模擬結帳欄位 (裝飾用，不可輸入)
        st.text_input("💳 信用卡號", placeholder="**** **** **** 1234", disabled=True)
        
        c_exp, c_cvc = st.columns(2)
        with c_exp: 
            st.text_input("有效期限", placeholder="MM/YY", disabled=True)
        with c_cvc: 
            st.text_input("CVC", placeholder="123", disabled=True)
        
        # 若是 Internal 組，在結帳按鈕上方再次強化「官方承諾」感
        if security == 'Internal':
            st.caption("ℹ️ 我們保證不會將您的資料用於行銷用途。")
            
        st.button("立即結帳 (模擬) ➔", disabled=True)

# --- 5. 主程式流程 ---

# 階段 1: 同意書
if st.session_state['step'] == 'consent':
    st.title("🛒 網購決策研究")
    st.info("👋 歡迎參與！本研究將模擬真實購物情境。")
    st.write("""
    請想像您**正打算購買**接下來顯示的商品。
    請仔細瀏覽網頁資訊，稍後將詢問您的購物感受。
    """)
    
    if st.button("開始實驗 👉"):
        go_to_step('stimulus')

# 階段 2: 刺激物 (網頁瀏覽)
elif st.session_state['step'] == 'stimulus':
    # 呼叫渲染函數，傳入隨機分派的變數
    render_ecommerce_page(st.session_state['security'], st.session_state['involvement'])
    
    st.write("")
    st.info("💡 提示：請確認您已看清楚商品與網站標示")
    
    if st.button("我已看完，前往問卷 👉"):
        go_to_step('survey')

# 階段 3: 問卷填答
elif st.session_state['step'] == 'survey':
    st.subheader("📝 填答區")
    
    with st.form("my_form"):
        st.write(f"針對剛剛看到的 **{st.session_state['involvement']} (涉入度)** 商品網站：")
        
        st.markdown("**1. 您願意支付多少錢購買此商品？(WTP)**")
        wtp = st.number_input("請輸入金額 (NTD)", min_value=0, step=10)
        
        st.markdown("**2. 您認為該網站的資安防護可信嗎？(訊號可信度)**")
        trust = st.slider("1 (完全不可信) - 7 (非常可信)", 1, 7, 4)
        
        st.markdown("**3. 您認為該網站真心重視消費者的隱私嗎？(品牌真實性)**")
        auth = st.slider("1 (完全不重視) - 7 (非常重視)", 1, 7, 4)
        
        # 隱藏欄位：記錄受試者組別 (方便你之後分析數據)
        # 實際上這需要寫入資料庫，目前僅顯示在畫面上供確認
        
        if st.form_submit_button("送出答案"):
            st.success("✅ 感謝您的參與！")
            st.json({
                "Group_Signal": st.session_state['security'],
                "Group_Product": st.session_state['involvement'],
                "WTP": wtp,
                "Trust_Score": trust,
                "Authenticity_Score": auth
            })
            
            # 重置實驗按鈕 (方便你測試下一組)
            if st.button("重置實驗 (下一位受試者)"):
                st.session_state.clear()
                st.rerun()
