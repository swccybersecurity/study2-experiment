import streamlit as st
import random
import time
import os

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="CyberTech Store", layout="centered")

# --- 2. CSS 科技感樣式 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;600&display=swap');

    /* 全局背景 */
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        font-family: 'Inter', sans-serif;
        color: #e0e6ed;
    }

    /* 品牌 Logo 文字 */
    .brand-text {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0;
    }
    .brand-highlight { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }
    
    /* 導航欄容器 */
    .nav-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
    }

    /* 產品卡片 */
    .product-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    }

    /* 價格標籤 */
    .price-tag {
        font-family: 'Rajdhani', sans-serif;
        color: #00f2ff;
        font-size: 2.0em;
        font-weight: 700;
        margin: 10px 0;
    }

    /* 支付按鈕特別樣式 */
    .pay-btn-container button {
        background: linear-gradient(45deg, #00c853, #64dd17) !important;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
        padding: 12px 0;
        font-size: 1.1rem;
        margin-top: 10px;
    }
    .pay-btn-container button:hover {
        box-shadow: 0 0 15px rgba(100, 221, 23, 0.6);
        transform: scale(1.02);
    }
    
    /* 內部訊號框樣式 */
    .internal-box {
        background: rgba(0, 230, 118, 0.1);
        border-left: 4px solid #00e676;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    
    /* 外部認證徽章框 */
    .cert-box {
        background: white;
        padding: 10px;
        border-radius: 8px;
        display: inline-block;
        border: 2px solid #00f2ff;
        text-align: center;
    }

    /* 模擬信用卡輸入框樣式 (唯讀) */
    .fake-input {
        background: #0d1117;
        border: 1px solid #30363d;
        color: #8b949e;
        padding: 8px;
        border-radius: 5px;
        width: 100%;
        margin-bottom: 8px;
        font-family: monospace;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 狀態管理 ---
def go_to_step(next_step):
    st.session_state['step'] = next_step

if 'step' not in st.session_state:
    st.session_state['security'] = random.choice(['External', 'Internal'])
    st.session_state['involvement'] = random.choice(['High', 'Low'])
    st.session_state['step'] = 'consent'
    st.session_state['verified'] = False
    st.session_state['submission_completed'] = False

# --- 4. 渲染元件 ---

def render_navbar(security):
    with st.container():
        st.markdown('<div class="nav-box">', unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown('<div class="brand-text">CYBER<span class="brand-highlight">STORE</span></div>', unsafe_allow_html=True)
        with c2:
            if security == 'Internal':
                st.markdown("""
                <div style="text-align:right; font-size:0.8rem; color:#b0bec5; padding-top: 5px;">
                    隱私權保護政策
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:right; font-size:1.2rem;">🛒 <span style="color:#00f2ff">0</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_security_signal(security):
    if security == 'External':
        c1, c2 = st.columns([1, 2])
        with c1:
            if os.path.exists("cert_badges.PNG"):
                st.markdown('<div class="cert-box">', unsafe_allow_html=True)
                st.image("cert_badges.PNG", width=120)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("圖片缺失: cert_badges.PNG")
        with c2:
            st.markdown("### 🛡️ 安全認證已啟用")
            st.caption("本網站通過 ISO 27001 與 TRUSTe 雙重稽核，確保您的資訊安全。")
            
            if not st.session_state['verified']:
                if st.button("🔍 點此驗證證書有效性", key="btn_verify"):
                    with st.spinner("正在連線至 TRUSTe 資料庫驗證..."):
                        time.sleep(1.2)
                    st.session_state['verified'] = True
                    st.rerun()
            else:
                st.success("✅ 驗證通過：證書有效且受保護")

    elif security == 'Internal':
        st.markdown("""
        <div class="internal-box">
            <h4 style="margin:0; color:#00e676;">🛡️ 官方資安承諾 (Official Guarantee)</h4>
            <p style="margin:5px 0 0 0; color:#cfd8dc; font-size:0.9rem;">
                我們承諾您的數據僅用於交易，絕不外洩。
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_product_checkout(involvement):
    c1, c2 = st.columns([1.2, 1])
    
    # 左側：產品圖
    with c1:
        if involvement == 'High':
            img, title, price_str = "Lp.AVIF", "ProBook X1 Ultimate", "NT$ 45,900"
            desc = "專為極致效能打造。搭載最新 AI 神經運算引擎，鈦金屬機身。"
        else:
            img, title, price_str = "Pen.jpg", "Tactical Gel Pen", "NT$ 150"
            desc = "極簡工業設計。航空鋁合金材質，0.5mm 滑順筆觸。"
        
        if os.path.exists(img):
            st.image(img, use_container_width=True)
        else:
            st.warning(f"圖片遺失: {img}")

    # 右側：產品資訊 + 模擬結帳區
    with c2:
        # 重點修正：這裡的 HTML 字串取消了前面的縮排，確保靠左對齊
        st.markdown(f"""
<div class="product-card">
    <h3 style="margin:0; color:white;">{title}</h3>
    <p style="color:#8b949e; font-size:0.9rem; margin-top:5px;">{desc}</p>
    <div class="price-tag">{price_str}</div>
    <div style="font-size:0.8rem; color:#8b949e; margin-bottom:15px;">🛡️ 官方原廠保固</div>
    <hr style="border-color:rgba(255,255,255,0.1); margin: 15px 0;">
    <div style="background:rgba(0,0,0,0.3); padding:10px; border-radius:8px;">
        <div style="font-size:0.8rem; color:#fff; margin-bottom:5px;">💳 信用卡快速結帳 (Saved Card)</div>
        <div class="fake-input">xxxx-xxxx-xxxx-8829</div>
        <div style="display:flex; gap:10px;">
            <div class="fake-input" style="width:50%;">12/28</div>
            <div class="fake-input" style="width:50%;">***</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown('<div class="pay-btn-container">', unsafe_allow_html=True)
        if st.button(f"確認支付 {price_str}", key="btn_pay_trigger"):
            go_to_step('survey')
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 主程式流程 ---

if st.session_state['step'] == 'consent':
    st.markdown("<br><h1 style='text-align:center;'>🚀 網購體驗研究</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8b949e;'>請想像您正打算購買以下科技產品，並請您在瀏覽過程中留意網站資訊...</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("進入商店 (Enter Store)"):
            go_to_step('stimulus')

elif st.session_state['step'] == 'stimulus':
    render_navbar(st.session_state['security'])
    render_security_signal(st.session_state['security'])
    st.markdown("---")
    
    render_product_checkout(st.session_state['involvement'])

elif st.session_state['step'] == 'survey':
    st.title("📝 用戶感受調查")
    st.info("請根據剛剛瀏覽網頁的感受，回答以下問題：")

    with st.form("survey_form"):
        st.write("**1. 您願意支付多少金額購買此商品？ (WTP)**")
        st.caption("請填寫您內心認為合理的最高價格")
        wtp = st.number_input("金額 (NT$)", min_value=0, step=100, key="wtp_input")
        
        st.write("**2. 您認為此網站的資安防護可信嗎？**")
        trust = st.slider("1 (非常不可信) - 7 (非常可信)", 1, 7, 4, key="trust_score")
        
        st.write("**3. 您認為該網站真心重視消費者的隱私嗎？(品牌真實性)**")
        auth = st.slider("1 (完全不重視) - 7 (非常重視)", 1, 7, 4, key="auth_score")
        
        submitted = st.form_submit_button("送出問卷")
        
        if submitted:
            st.session_state['submission_completed'] = True
            st.session_state['last_data'] = {
                "組別 (訊號)": st.session_state['security'],
                "組別 (產品)": st.session_state['involvement'],
                "WTP": wtp,
                "信任度": trust,
                "真實性": auth
            }

    if st.session_state.get('submission_completed'):
        st.success("✅ 感謝您的填答！數據已記錄。")
        st.write("---")
        st.json(st.session_state['last_data'])
        
        if st.button("重置實驗 (下一位)", key="btn_reset"):
            st.session_state.clear()
            st.rerun()
