import streamlit as st
import random
import time
import os

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="CyberSec Experiment", layout="centered", page_icon="🛡️")

# --- 2. CSS 科技感樣式 (維持原樣，微調細節) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;600&display=swap');

    /* 全局背景：深沈科技藍黑 */
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        font-family: 'Inter', sans-serif;
        color: #e0e6ed;
    }

    /* 品牌 Logo */
    .brand-text {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .brand-highlight { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }

    /* 情境引導框 (New) */
    .scenario-box {
        background: rgba(255, 87, 34, 0.1); 
        border-left: 5px solid #ff5722;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
    }
    .scenario-title { font-size: 1.2rem; font-weight: bold; color: #ffab91; margin-bottom: 10px; }

    /* 產品卡片 */
    .product-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid rgba(88, 166, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* 價格與按鈕 */
    .price-tag {
        font-family: 'Rajdhani', sans-serif;
        color: #00f2ff;
        font-size: 2.2em;
        font-weight: 700;
        margin: 15px 0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00c853, #64dd17);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 12px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(100, 255, 100, 0.4);
    }

    /* 資安標章樣式 */
    .cert-box {
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 10px;
        background: rgba(0, 242, 255, 0.05);
        text-align: center;
    }
    .internal-signal {
        border-left: 4px solid #9e9e9e;
        padding-left: 15px;
        color: #b0bec5;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 狀態管理 (State Management) ---
if 'step' not in st.session_state:
    # 隨機分派實驗組別
    st.session_state['security_level'] = random.choice(['High_Signal', 'Low_Signal']) # 有標章 vs 無標章
    st.session_state['privacy_risk'] = random.choice(['High_Risk', 'Low_Risk'])       # 攝影機 vs 燈泡
    
    st.session_state['step'] = 'intro' # 流程：intro -> priming -> store -> survey
    st.session_state['verified'] = False

def go_next(step_name):
    st.session_state['step'] = step_name
    st.rerun()

# --- 4. 輔助函數：渲染元件 ---

def render_scenario_priming(risk_type):
    """渲染情境引導頁面 (關鍵修正：喚醒危機感)"""
    st.markdown("## 📢 購物情境說明")
    st.markdown("在進入商店前，請仔細閱讀您目前的處境：")
    
    if risk_type == 'High_Risk':
        # 高風險情境：攝影機
        st.markdown("""
        <div class="scenario-box">
            <div class="scenario-title">👶 情境 A：守護新生兒</div>
            <p>您剛成為新手爸媽，為了能隨時在手機上查看嬰兒房的狀況，您計畫購買一台<b>「高畫質無線監控攝影機」</b>。</p>
            <p>然而，您最近在新聞上看到：<b>「駭客入侵家用攝影機，私密影像遭直播至暗網販售」</b>的消息，這讓您對隱私安全感到非常焦慮。</p>
            <p>現在，您在網路上找到了這款產品...</p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # 低風險情境：燈泡
        st.markdown("""
        <div class="scenario-box">
            <div class="scenario-title">💡 情境 B：更換書房燈泡</div>
            <p>您覺得書房的燈光太暗，想換一顆可以調整亮度的<b>「智慧 LED 燈泡」</b>，讓閱讀更舒適。</p>
            <p>這款燈泡可以用手機 App 開關。如果發生故障或被駭，頂多是燈光無法控制，<b>不會造成個人隱私外洩或財產損失</b>。</p>
            <p>現在，您在網路上找到了這款產品...</p>
        </div>
        """, unsafe_allow_html=True)
        

    if st.button("我已了解情境，進入商店選購 ➡️"):
        go_next('store')

def render_product_page(risk_type, security_level):
    """渲染商店頁面"""
    
    # 1. 導覽列
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown('<div class="brand-text">CYBER<span class="brand-highlight">STORE</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown("👤 User: Guest_882")
    st.markdown("---")

    # 2. 定義產品內容
    if risk_type == 'High_Risk':
        prod_name = "SecureView 360° 寶寶監視器"
        prod_desc = "2K 高畫質 / 雙向語音 / AI 哭聲偵測 / 夜視功能"
        price = 1500
        img_file = "camera.jpg" # 請準備這張圖
    else:
        prod_name = "SmartLight 智慧調節燈泡"
        prod_desc = "1600萬色 / 語音控制 / 節能省電 / 排程設定"
        price = 500
        img_file = "bulb.jpg"   # 請準備這張圖

    # 3. 版面配置
    col_img, col_info = st.columns([1, 1.2])
    
    with col_img:
        # 顯示產品圖片 (若無圖片顯示替代文字)
        if os.path.exists(img_file):
            st.image(img_file, use_container_width=True)
        else:
            st.info(f"📸 (圖片預留位: {img_file})")
            st.markdown(f"### {prod_name}")

        # --- 關鍵修正：資安訊號顯示區 ---
        st.markdown("#### 🔒 安全性資訊")
        if security_level == 'High_Signal':
            # 強訊號：顯示標章
            st.markdown("""
            <div class="cert-box">
                <h3 style="margin:0; color:#00f2ff;">🛡️ TRUSTe Privacy Verified</h3>
                <p style="font-size:0.8rem; margin:5px 0;">通過 ISO 27001 國際資安認證</p>
                <p style="font-size:0.8rem; margin:0;">包含：資料加密傳輸、防駭客滲透測試</p>
            </div>
            """, unsafe_allow_html=True)
            if not st.session_state['verified']:
                if st.button("🔍 點此查驗證書真偽"):
                    with st.spinner("連線至第三方資料庫驗證中..."):
                        time.sleep(1)
                    st.session_state['verified'] = True
                    st.rerun()
            else:
                st.success("✅ 驗證成功：證書有效")
        else:
            # 弱訊號：僅內部文字
            st.markdown("""
            <div class="internal-signal">
                本網站重視您的隱私。<br>
                我們會盡力保護您的資料安全。
            </div>
            """, unsafe_allow_html=True)

    with col_info:
        st.markdown(f"## {prod_name}")
        st.markdown(f"<p style='color:#bbb;'>{prod_desc}</p>", unsafe_allow_html=True)
        st.markdown(f"<div class="price-tag">NT$ {price}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.write("🚚 全台免運費 | ⚡ 24h 到貨")
        
        # 模擬結帳按鈕
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"立即購買 (NT$ {price})", key="buy_btn"):
            with st.spinner("正在建立安全連線..."):
                time.sleep(1)
            go_next('survey')

def render_survey(risk_type, security_level):
    """渲染問卷 (關鍵修正：WTP 階梯式問法)"""
    st.success("✅ 模擬購買程序已結束！(不會發生真實扣款)")
    st.markdown("### 📋 購買決策調查")
    
    # 根據產品動態調整基準價格
    base_price = 1500 if risk_type == 'High_Risk' else 500
    
    with st.form("research_form"):
        st.markdown("#### 第一部分：購買意願與溢價測試 (WTP)")
        st.write(f"請回想剛才的產品 **({risk_type.replace('_',' ')})** 與網站提供的**資安資訊**：")
        
        # Q1: 原價購買意願
        st.write(f"1. 如果此產品售價為 **NT$ {base_price}** (原價)，您的購買機率是？")
        wtp_0 = st.slider("購買機率 (0% - 100%)", 0, 100, 50, key="q1")
        
        # Q2: 溢價 10%
        p_10 = int(base_price * 1.1)
        st.write(f"2. 如果此產品售價提高至 **NT$ {p_10}** (貴10%)，但保證擁有上述的資安防護，您的購買機率是？")
        wtp_10 = st.slider("購買機率 (0% - 100%)", 0, 100, 50, key="q2")
        
        # Q3: 溢價 20%
        p_20 = int(base_price * 1.2)
        st.write(f"3. 如果此產品售價提高至 **NT$ {p_20}** (貴20%)，您的購買機率是？")
        wtp_20 = st.slider("購買機率 (0% - 100%)", 0, 100, 50, key="q3")
        
        st.markdown("---")
        st.markdown("#### 第二部分：感受調查")
        
        # Q4: 感知風險 (Perceived Risk) - 核心變數
        st.write("4. **感知風險**：您覺得在這個網站購買此產品，個人隱私外洩的風險有多高？")
        risk_score = st.slider("1 (風險極低) - 7 (風險極高)", 1, 7, 4)

        # Q5: 品牌真實性 (Brand Authenticity)
        st.write("5. **品牌真實性**：您覺得這個網站的資安聲明是真心誠意的嗎？")
        auth_score = st.slider("1 (虛假/行銷話術) - 7 (非常真誠/說到做到)", 1, 7, 4)

        if st.form_submit_button("提交數據"):
            # 顯示結果 (模擬後端記錄)
            result = {
                "Condition_Product": risk_type,
                "Condition_Signal": security_level,
                "WTP_0%": wtp_0,
                "WTP_10%": wtp_10,
                "WTP_20%": wtp_20,
                "Perceived_Risk": risk_score,
                "Brand_Authenticity": auth_score
            }
            st.json(result)
            st.success("數據已記錄！請截圖保存或進行下一位測試。")
            if st.button("重新開始"):
                st.session_state.clear()
                st.rerun()

# --- 5. 主程式邏輯 ---

if st.session_state['step'] == 'intro':
    st.title("🛡️ 資安價值實驗室")
    st.info("本實驗將模擬真實網購情境，請依照您的直覺進行決策。")
    if st.button("開始實驗"):
        go_next('priming')

elif st.session_state['step'] == 'priming':
    render_scenario_priming(st.session_state['privacy_risk'])

elif st.session_state['step'] == 'store':
    render_product_page(st.session_state['privacy_risk'], st.session_state['security_level'])

elif st.session_state['step'] == 'survey':
    render_survey(st.session_state['privacy_risk'], st.session_state['security_level'])
        
