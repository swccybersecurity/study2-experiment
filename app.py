import streamlit as st
import random
import os

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="CyberTech Store", layout="centered")

# --- 2. CSS 魔改 (這是讓介面變高級的關鍵) ---
st.markdown("""
<style>
    /* 引入現代字體 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* 全域設定 */
    .stApp {
        background-color: #0E1117; /* 深色科技背景 */
        font-family: 'Inter', sans-serif;
    }

    /* 模擬導航欄 (Navbar) */
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
        color: #FF5722; /* 品牌橘色 */
    }

    /* 商品卡片容器 */
    .product-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: translateY(-2px);
        border-color: #58a6ff; /* 懸停時發光 */
    }

    /* 價格標籤 */
    .price-tag {
        color: #58a6ff; /* 科技藍 */
        font-size: 2em;
        font-weight: 800;
        margin: 10px 0;
        text-shadow: 0 0 10px rgba(88, 166, 255, 0.3);
    }

    /* 結帳按鈕優化 */
    .stButton > button {
        background: linear-gradient(90deg, #FF5722, #FF8A65);
        color: white;
        font-weight: bold;
        border-radius: 30px;
        padding: 12px 30px;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 87, 34, 0.4);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(255, 87, 34, 0.6);
        transform: scale(1.02);
    }

    /* --- 資安訊號樣式區 --- */

    /* External: 解決白底圖片難看的問題 */
    .cert-badge-wrapper {
        background-color: white;
        padding: 8px 15px;
        border-radius: 8px;
        display: inline-block;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
    }

    /* Internal: 高級盾牌樣式 */
    .internal-signal-modern {
        background: rgba(46, 160, 67, 0.1); /* 深綠色半透明 */
        border: 1px solid #2ea043;
        border-radius: 12px;
        padding: 15px;
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .shield-icon {
        font-size: 2rem;
        margin-right: 15px;
    }
    .signal-text h4 {
        margin: 0;
        color: #2ea043; /* 亮綠色 */
        font-size: 1rem;
        font-weight: 700;
    }
    .signal-text p {
        margin: 0;
        color: #b0b8c4;
        font-size: 0.8rem;
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

# --- 4. 頁面渲染邏輯 ---
def render_ecommerce_page(security, involvement):
    
    # === 頂部導航欄 (模擬真實網站 Header) ===
    # 這裡會根據訊號動態改變 Header 的右側內容
    
    header_html = """
    <div class="navbar">
        <div class="brand-name">Cyber<span class="brand-highlight">Store</span></div>
        <div style="display:flex; align-items:center;">
    """
    
    if security == 'External':
        # External 組：把原本很醜的圖片包在一個乾淨的 div 裡
        # 注意：這裡假設你已經上傳了圖片。我加了 style 來限制圖片高度，避免它太大
        img_path = "cert_badges.PNG" # 確保檔名大小寫正確
        
        # 為了能在 f-string 裡面放圖片，我們先檢查圖片是否存在
        if os.path.exists(img_path):
            # Streamlit 的 st.image 很難塞進 HTML 字串，所以我們把這一塊留給 st.columns 處理
            pass 
        else:
            header_html += "<span style='color:red; font-size:0.8em;'>[圖片缺失]</span>"
            
    elif security == 'Internal':
        # Internal 組：在 Header 放一個小的文字連結
        header_html += """
            <div style="text-align:right; font-size:0.8rem; color:#8b949e;">
                <span style="color:#2ea043;">✔ 官方認證商城</span><br>
                隱私權保護政策
            </div>
        """
    
    header_html += """
            <div style="margin-left:20px; font-size:1.2rem;">🛒</div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # === External 圖片的特殊處理 (為了排版漂亮) ===
    if security == 'External':
        col_space, col_badge = st.columns([3, 1])
        with col_badge:
            if os.path.exists("cert_badges.PNG"):
                # 用一個白底容器包住圖片，解決去背問題
                st.markdown('<div class="cert-badge-wrapper">', unsafe_allow_html=True)
                st.image("cert_badges.PNG", width=120)
                st.markdown('</div>', unsafe_allow_html=True)

    # === Internal 訊號的特殊處理 (放在商品上方) ===
    if security == 'Internal':
        st.markdown("""
        <div class="internal-signal-modern">
            <div class="shield-icon">🛡️</div>
            <div class="signal-text">
                <h4>官方資安承諾 (Official Guarantee)</h4>
                <p>本站採用端對端加密技術，確保您的交易與個資絕對安全。</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # === 商品展示區 (兩欄式佈局) ===
    c1, c2 = st.columns([1.2, 1])
    
    # 左欄：商品圖
    with c1:
        if involvement == 'High':
            img_file, title, price = "Lp.AVIF", "ProBook X1 Ultimate", "NT$ 45,900"
            desc = "為極致效能而生。搭載最新 AI 神經運算引擎，鈦金屬機身，軍規級資安防護晶片。"
        else:
            img_file, title, price = "Pen.jpg", "Muji Style Gel Pen", "NT$ 150"
            desc = "極簡美學。0.5mm 滑順筆觸，人體工學握感，辦公室必備的書寫體驗。"
            
        if os.path.exists(img_file):
            st.image(img_file, use_container_width=True)
        else:
            st.warning("圖片讀取失敗")

    # 右欄：資訊卡片
    with c2:
        # 開始 Product Card
        st.markdown(f"""
        <div class="product-card">
            <h2 style="margin-top:0; color:white;">{title}</h2>
            <p style="color:#8b949e; font-size:0.9rem; line-height:1.5;">{desc}</p>
            <div class="price-tag">{price}</div>
            <hr style="border-color:#30363d; margin: 20px 0;">
            <div style="margin-bottom:15px;">
                <label style="color:#8b949e; font-size:0.8rem;">配送地址</label>
                <div style="background:#0d1117; padding:10px; border-radius:8px; color:white; border:1px solid #30363d;">
                    台北市大安區...
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") # Spacer
        
        # 這裡放按鈕 (必須在 HTML 區塊外，才能保有 Python 功能)
        st.button("立即結帳 (CHECKOUT) ➔", key="btn_checkout", disabled=True)
        
        if security == 'Internal':
            st.caption("🔒 SSL Secure Connection | Official Warranty")

# --- 5. 主流程 ---

if st.session_state['step'] == 'consent':
    st.markdown("<h1 style='text-align:center;'>CyberStore 購物體驗研究</h1>", unsafe_allow_html=True)
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
