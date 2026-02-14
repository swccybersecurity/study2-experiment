import streamlit as st
import random
import os

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="CyberTech Store", layout="centered")

# --- 2. CSS 美化 (保持不變，這部分是正常的) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* 導航欄 */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 20px;
        background: #161b22;
        border-bottom: 1px solid #30363d;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .brand-name {
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
    }
    .brand-highlight {
        color: #FF5722;
    }
    
    /* 商品卡片 */
    .product-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .price-tag {
        color: #58a6ff;
        font-size: 2em;
        font-weight: 800;
        margin: 10px 0;
        text-shadow: 0 0 10px rgba(88, 166, 255, 0.3);
    }
    
    /* 按鈕 */
    .stButton > button {
        background: linear-gradient(90deg, #FF5722, #FF8A65);
        color: white;
        font-weight: bold;
        border-radius: 30px;
        padding: 12px 30px;
        border: none;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px; 
    }
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(255, 87, 34, 0.6);
        transform: scale(1.02);
    }
    
    /* Internal 訊號樣式 */
    .internal-signal-modern {
        background: rgba(46, 160, 67, 0.1);
        border: 1px solid #2ea043;
        border-radius: 12px;
        padding: 15px;
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    
    /* External 圖片容器 */
    .cert-badge-wrapper {
        background-color: white;
        padding: 8px 12px;
        border-radius: 8px;
        display: inline-block;
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

# --- 4. 渲染邏輯 (Bug 修復區：改用單行字串拼接) ---
def render_ecommerce_page(security, involvement):
    
    # 準備 Navbar 右側內容
    # 注意：這裡我將 HTML 壓縮成一行，避免任何縮排問題
    if security == 'Internal':
        right_content = '<div style="text-align:right; font-size:0.8rem; color:#8b949e;"><span style="color:#2ea043;">✔ 官方認證商城</span><br>隱私權保護政策</div>'
    else:
        right_content = "" # External 組不顯示文字

    # 組合 Navbar HTML (全部壓縮為一行)
    navbar_html = f'<div class="navbar"><div class="brand-name">Cyber<span class="brand-highlight">Store</span></div><div style="display:flex; align-items:center;">{right_content}<div style="margin-left:20px; font-size:1.2rem;">🛒</div></div></div>'
    
    st.markdown(navbar_html, unsafe_allow_html=True)

    # === External 圖片的特殊處理 ===
    if security == 'External':
        col_space, col_badge = st.columns([3, 1.2])
        with col_badge:
            if os.path.exists("cert_badges.PNG"):
                # 同樣壓縮 HTML
                st.markdown('<div class="cert-badge-wrapper">', unsafe_allow_html=True)
                st.image("cert_badges.PNG", width=130)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("圖片缺失: cert_badges.PNG")

    # === Internal 訊號的特殊處理 ===
    if security == 'Internal':
        # 壓縮 HTML
        internal_signal_html = '<div class="internal-signal-modern"><div style="font-size: 2rem; margin-right: 15px;">🛡️</div><div><h4 style="margin:0; color:#2ea043; font-size:1rem;">官方資安承諾 (Official Guarantee)</h4><p style="margin:0; color:#b0b8c4; font-size:0.8rem;">本站採用端對端加密技術，確保您的交易與個資絕對安全。</p></div></div>'
        st.markdown(internal_signal_html, unsafe_allow_html=True)

    # === 商品展示區 ===
    c1, c2 = st.columns([1.2, 1])
    
    with c1:
        if involvement == 'High':
            img_file = "Lp.AVIF"
            title = "ProBook X1 Ultimate"
            price = "NT$ 45,900"
            desc = "為極致效能而生。搭載最新 AI 神經運算引擎，鈦金屬機身，軍規級資安防護晶片。"
        else:
            img_file = "Pen.jpg"
            title = "Muji Style Gel Pen"
            price = "NT$ 150"
            desc = "極簡美學。0.5mm 滑順筆觸，人體工學握感，辦公室必備的書寫體驗。"
            
        if os.path.exists(img_file):
            st.image(img_file, use_container_width=True)
        else:
            st.warning(f"圖片讀取失敗: {img_file}")

    with c2:
        # 商品卡片 HTML 也全部壓縮為一行
        card_html = f'<div class="product-card"><h2 style="margin-top:0; color:white;">{title}</h2><p style="color:#8b949e; font-size:0.9rem; line-height:1.5;">{desc}</p><div class="price-tag">{price}</div><hr style="border-color:#30363d; margin: 20px 0;"><div style="margin-bottom:15px;"><label style="color:#8b949e; font-size:0.8rem;">配送地址</label><div style="background:#0d1117; padding:10px; border-radius:8px; color:white; border:1px solid #30363d;">台北市大安區...</div></div></div>'
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        st.write("") 
        st.button("立即結帳 (CHECKOUT) ➔", key="btn_checkout", disabled=True)
        
        if security == 'Internal':
            st.caption("🔒 SSL Secure Connection | Official Warranty")

# --- 5. 主流程 ---
if st.session_state['step'] == 'consent':
    st.markdown("<h1 style='text-align:center; color:white;'>CyberStore 購物體驗研究</h1>", unsafe_allow_html=True)
    st.info("請想像您正打算購買這項科技產品...")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("進入商店 👉"):
            go_to_step('stimulus')

elif st.session_state['step'] == 'stimulus':
    render_ecommerce_page(st.session_state['security'], st.session_state['involvement'])
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("我已完成瀏覽，前往問卷"):
            go_to_step('survey')

elif st.session_state['step'] == 'survey':
    st.title("📝 用戶感受調查")
    with st.form("survey"):
        st.write("1. 您願意支付多少金額？")
        st.number_input("NT$", step=100)
        st.write("2. 您覺得這個網站安全嗎？")
        st.slider("信任分數", 1, 7)
        st.form_submit_button("送出")
