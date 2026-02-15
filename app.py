import streamlit as st
import random
import time
import os

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="CyberSec Experiment", layout="centered", page_icon="🛡️")

# --- 2. CSS 樣式 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;600&display=swap');
    .stApp { background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%); font-family: 'Inter', sans-serif; color: #e0e6ed; }
    .brand-text { font-family: 'Rajdhani', sans-serif; font-size: 1.8rem; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: 2px; }
    .brand-highlight { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }
    .scenario-box { background: rgba(255, 87, 34, 0.1); border-left: 5px solid #ff5722; padding: 20px; border-radius: 8px; margin-bottom: 25px; }
    .scenario-title { font-size: 1.2rem; font-weight: bold; color: #ffab91; margin-bottom: 10px; }
    .product-card { background: rgba(22, 27, 34, 0.8); border: 1px solid rgba(88, 166, 255, 0.2); border-radius: 20px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .price-tag { font-family: 'Rajdhani', sans-serif; color: #00f2ff; font-size: 2.2em; font-weight: 700; margin: 15px 0; }
    .stButton>button { background: linear-gradient(90deg, #00c853, #64dd17); color: white; border: none; border-radius: 8px; font-weight: bold; width: 100%; padding: 12px; transition: all 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px rgba(100, 255, 100, 0.4); }
    .cert-box { border: 2px solid #00f2ff; border-radius: 10px; padding: 10px; background: rgba(0, 242, 255, 0.05); text-align: center; }
    .internal-signal { border-left: 4px solid #9e9e9e; padding-left: 15px; color: #b0bec5; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# --- 3. 狀態管理 (自動修復與初始化) ---
if 'privacy_risk' not in st.session_state:
    st.session_state.clear()
    st.session_state['security_level'] = random.choice(['High_Signal', 'Low_Signal'])
    st.session_state['privacy_risk'] = random.choice(['High_Risk', 'Low_Risk'])
    st.session_state['step'] = 'intro'
    st.session_state['verified'] = False

def go_next(step_name):
    st.session_state['step'] = step_name
    st.rerun()

# --- 4. 輔助函數 ---

def render_scenario_priming(risk_type):
    st.markdown("## 📢 購物情境說明")
    if risk_type == 'High_Risk':
        st.markdown("""
        <div class="scenario-box">
            <div class="scenario-title">👶 情境 A：守護新生兒</div>
            <p>您剛成為新手爸媽，為了能隨時查看嬰兒狀況，計畫購買一台<b>「高畫質無線監控攝影機」</b>。</p>
            <p>⚠️ <b>警示：</b>近期新聞頻傳駭客入侵家用攝影機，私密影像遭直播至暗網，讓您對隱私極度焦慮。</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="scenario-box">
            <div class="scenario-title">💡 情境 B：更換燈泡</div>
            <p>您想換一顆可用手機 App 控制開關的<b>「智慧 LED 燈泡」</b>。</p>
            <p>ℹ️ <b>提示：</b>此設備僅控制燈光，若發生故障或被駭，頂多燈光無法控制，不會有隱私風險。</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("我已了解情境，進入商店 ➡️"):
        go_next('store')

def render_product_page(risk_type, security_level):
    c1, c2 = st.columns([3, 1])
    with c1: st.markdown('<div class="brand-text">CYBER<span class="brand-highlight">STORE</span></div>', unsafe_allow_html=True)
    with c2: st.markdown("👤 User: Guest_882")
    st.markdown("---")

    if risk_type == 'High_Risk':
        prod_name, prod_desc, price = "SecureView 寶寶監視器", "2K 高畫質 / 哭聲偵測 / 夜視", 1500
        img_name = "camera.jpg"
    else:
        prod_name, prod_desc, price = "SmartLight 智慧燈泡", "1600萬色 / 語音控制 / 節能", 500
        img_name = "bulb.jpg"

    c_img, c_info = st.columns([1, 1.2])
    with c_img:
        # 圖片防呆：若沒圖片會顯示文字
        if os.path.exists(img_name):
            st.image(img_name, use_container_width=True)
        else:
            st.warning(f"⚠️ 圖片未上傳: {img_name}")
            st.info("請將圖片上傳至 GitHub 以顯示")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if security_level == 'High_Signal':
            st.markdown('<div class="cert-box"><h4 style="margin:0; color:#00f2ff;">🛡️ TRUSTe 認證</h4><small>ISO 27001 資安稽核通過</small></div>', unsafe_allow_html=True)
            if not st.session_state['verified']:
                if st.button("🔍 驗證證書"):
                    with st.spinner("驗證中..."): time.sleep(0.5)
                    st.session_state['verified'] = True
                    st.rerun()
            else:
                st.success("✅ 證書有效")
        else:
            st.markdown('<div class="internal-signal">本網站承諾保護您的隱私安全。</div>', unsafe_allow_html=True)

    with c_info:
        st.markdown(f"## {prod_name}")
        st.markdown(f"<p style='color:#bbb;'>{prod_desc}</p>", unsafe_allow_html=True)
        
        # --- 關鍵修正處：這裡改用 f'...' (外單引號) 避免與 class="..." (內雙引號) 衝突 ---
        st.markdown(f'<div class="price-tag">NT$ {price}</div>', unsafe_allow_html=True)
        # -------------------------------------------------------------------------
        
        st.write("🚚 免運費 | ⚡ 24h 到貨")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"立即購買 (NT$ {price})"):
            with st.spinner("安全連線中..."): time.sleep(1)
            go_next('survey')

def render_survey(risk_type, security_level):
    st.success("✅ 模擬購買結束！")
    base_price = 1500 if risk_type == 'High_Risk' else 500
    
    with st.form("survey_form"):
        st.markdown("#### 💰 購買意願調查")
        st.write(f"1. 原價 (NT$ {base_price}) 購買機率？")
        p0 = st.slider("機率", 0, 100, 50, key="p0")
        st.write(f"2. 若**貴 10%** (NT$ {int(base_price*1.1)}) 購買機率？")
        p10 = st.slider("機率", 0, 100, 50, key="p10")
        st.write(f"3. 若**貴 20%** (NT$ {int(base_price*1.2)}) 購買機率？")
        p20 = st.slider("機率", 0, 100, 50, key="p20")
        
        st.markdown("#### 🧠 感受調查")
        risk = st.slider("4. 您覺得在此購買的**隱私風險**？ (1低-7高)", 1, 7, 4)
        auth = st.slider("5. 您覺得商家的**資安誠意**？ (1假-7真)", 1, 7, 4)
        
        if st.form_submit_button("提交數據"):
            # 顯示結果 JSON
            st.json({
                "Condition": risk_type, 
                "Signal": security_level, 
                "WTP_Slope": [p0, p10, p20], 
                "Perceived_Risk": risk
            })
            if st.button("重置實驗"):
                st.session_state.clear()
                st.rerun()

# --- 5. 主程式 ---
if st.session_state['step'] == 'intro':
    st.title("🛡️ 資安價值實驗室")
    if st.button("開始實驗"): go_next('priming')
elif st.session_state['step'] == 'priming':
    render_scenario_priming(st.session_state['privacy_risk'])
elif st.session_state['step'] == 'store':
    render_product_page(st.session_state['privacy_risk'], st.session_state['security_level'])
elif st.session_state['step'] == 'survey':
    render_survey(st.session_state['privacy_risk'], st.session_state['security_level'])
