import streamlit as st
import random
import time
import os

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="CyberTech Store", layout="centered")

# --- 2. CSS 科技感魔改 (Cyberpunk/Glassmorphism) ---
st.markdown("""
<style>
    /* 引入 Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;600&display=swap');

    /* 全域背景：深色科技藍 */
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        font-family: 'Inter', sans-serif;
        color: #e0e6ed;
    }

    /* 頂部導航欄 */
    .nav-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px 25px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }
    
    .brand-text {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .brand-highlight { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }

    /* 商品卡片：毛玻璃特效 */
    .product-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    /* 卡片頂部裝飾條 */
    .product-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 4px;
        background: linear-gradient(90deg, #00f2ff, #0066ff);
    }

    /* 價格標籤 */
    .price-tag {
        font-family: 'Rajdhani', sans-serif;
        color: #00f2ff;
        font-size: 2.2em;
        font-weight: 700;
        margin: 10px 0;
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }

    /* 結帳按鈕：霓虹按鈕 */
    .stButton > button {
        background: linear-gradient(45deg, #FF5722, #F44336);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 12px 0;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(244, 67, 54, 0.6);
    }

    /* --- 資安訊號樣式 --- */

    /* 1. External (外部): 證書容器 */
    .cert-container {
        background: white; /* 配合你的白底圖片 */
        padding: 10px;
        border-radius: 12px;
        display: inline-block;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
        text-align: center;
        border: 2px solid #00f2ff; /* 科技藍邊框 */
    }
    .verified-badge {
        color: #00c853;
        font-weight: bold;
        font-size: 0.8rem;
        margin-top: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 2. Internal (內部): 系統訊息框 */
    .internal-signal-box {
        background: rgba(0, 230, 118, 0.05);
        border-left: 4px solid #00e676;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 20px;
    }
    .internal-title {
        color: #00e676;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .internal-text {
        color: #b0bec5;
        font-size: 0.85rem;
        margin-top: 4px;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. 狀態與邏輯 ---
def go_to_step(next_step):
    st.session_state['step'] = next_step

if 'step' not in st.session_state:
    st.session_state['security'] = random.choice(['External', 'Internal'])
    st.session_state['involvement'] = random.choice(['High', 'Low'])
    st.session_state['step'] = 'consent'
    st.session_state['verified'] = False # 用來控制驗證按鈕的狀態

# --- 4. 渲染元件 (使用 Streamlit 原生元件以避免 Bug) ---

def render_navbar():
    # 使用 columns 取代 HTML 排版，絕對安全
    c1, c2, c3 = st.columns([2, 1, 0.5])
    with c1:
        st.markdown('<div class="brand-text">CYBER<span class="brand-highlight">STORE</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown("🛒 <span style='color:#00f2ff'>0</span>", unsafe_allow_html=True)
    st.markdown("---")

def render_security_signal(security):
    if security == 'External':
        # === 外部訊號：包含圖片與驗證功能 ===
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            if os.path.exists("cert_badges.PNG"):
                # 用 div 包住圖片製造白底卡片效果
                st.markdown('<div class="cert-container">', unsafe_allow_html=True)
                st.image("cert_badges.PNG", width=110)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Img Missing")

        with col_info:
            st.markdown("### 🛡️ 安全認證已啟用")
            st.caption("本網站通過 ISO 27001 與 TRUSTe 雙重稽核。")
            
            # === [新功能] 點擊驗證 ===
            if not st.session_state['verified']:
                if st.button("🔍 點此驗證證書有效性", key="verify_btn"):
                    with st.spinner("正在連線至 TRUSTe 資料庫驗證..."):
                        time.sleep(1.5) # 模擬延遲
                    st.session_state['verified'] = True
                    st.rerun()
            else:
                # 驗證成功後的狀態
                st.success("✅ 驗證通過：證書有效且受保護")
                st.markdown("<small style='color:#00c853'>Last checked: Just now</small>", unsafe_allow_html=True)

    elif security == 'Internal':
        # === 內部訊號：科技感系統通知 ===
        st.markdown("""
        <div class="internal-signal-box">
            <div class="internal-title">🛡️ OFFICIAL GUARANTEE</div>
            <div class="internal-text">
                本站採用端對端加密技術 (E2EE)。<br>
                我們承諾您的數據僅用於交易，絕不外洩。
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_product_area(involvement):
    c1, c2 = st.columns([1.2, 1])
    
    with c1:
        if involvement == 'High':
            img, title, price = "Lp.AVIF", "ProBook X1 Ultimate", "NT$ 45,900"
            desc = "Titanium Chassis / Neural Engine / Military Grade Security"
        else:
            img, title, price = "Pen.jpg", "Tactical Gel Pen", "NT$ 150"
            desc = "Aerospace Aluminum / Quick-Dry Ink / Minimalist Design"
        
        if os.path.exists(img):
            st.image(img, use_container_width=True)
        else:
            st.warning("Product Image Missing")

    with c2:
        # 用 HTML 渲染卡片文字
        st.markdown(f"""
        <div style="padding:10px;">
            <h2 style="margin:0; color:white;">{title}</h2>
            <p style="color:#8b949e; margin-top:10px;">{desc}</p>
            <div class="price-tag">{price}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.button("CHECKOUT ➔", disabled=True)
        
        # 額外的小字
        st.markdown("""
        <div style="margin-top:15px; font-size:0.8rem; color:#58a6ff; display:flex; align-items:center; gap:5px;">
            <span>🔒</span> SSL Encrypted Transaction
        </div>
        """, unsafe_allow_html=True)

# --- 5. 主流程 ---

if st.session_state['step'] == 'consent':
    st.markdown("<br><h1 style='text-align:center;'>🚀 購物體驗研究</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8b949e;'>請想像您正打算購買以下科技產品...</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("進入商店 / Enter Store"):
            go_to_step('stimulus')

elif st.session_state['step'] == 'stimulus':
    # 1. 渲染導航
    render_navbar()
    
    # 2. 渲染資安訊號 (若是 External，這裡會有互動按鈕)
    render_security_signal(st.session_state['security'])
    
    st.markdown("---")
    
    # 3. 渲染商品
    render_product_area(st.session_state['involvement'])
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("已完成瀏覽，填寫問卷 (Next Step)"):
        go_to_step('survey')

elif st.session_state['step'] == 'survey':
    st.title("📝 Data Collection")
    
    with st.form("survey_form"):
        st.write("1. Willingness to Pay (WTP)?")
        st.number_input("Amount (NT$)", step=100)
        
        st.write("2. Perceived Security?")
        st.slider("Score", 1, 7)
        
        st.write("3. Brand Authenticity?")
        st.slider("Score", 1, 7)
        
        if st.form_submit_button("Submit"):
            st.success("Thank you! Data recorded.")
            # 顯示組別供確認
            st.code(f"Group: {st.session_state['security']} / {st.session_state['involvement']}")
            if st.button("Reset"):
                st.session_state.clear()
                st.rerun()
