import streamlit as st
import random
import time
import os
import csv
from datetime import datetime

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="CyberSec Pricing Exp", layout="centered", page_icon="🛡️")

# --- 2. CSS 樣式 (強化標章視覺) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;600&display=swap');
    .stApp { background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%); font-family: 'Inter', sans-serif; color: #e0e6ed; }
    
    /* 標題與價格 */
    .brand-text { font-family: 'Rajdhani', sans-serif; font-size: 1.8rem; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: 2px; }
    .price-tag { font-family: 'Rajdhani', sans-serif; color: #00f2ff; font-size: 2.5em; font-weight: 700; margin: 10px 0; }
    
    /* 比較區塊 */
    .price-comparison { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; border: 1px solid #444; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .math-highlight { color: #ff5252; font-weight: bold; font-size: 1.2em; background: rgba(255, 82, 82, 0.1); padding: 2px 8px; border-radius: 4px;}
    
    /* 按鈕樣式 */
    .stButton>button { background: linear-gradient(90deg, #00c853, #64dd17); color: white; border: none; border-radius: 8px; font-weight: bold; width: 100%; padding: 12px; transition: all 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px rgba(100, 255, 100, 0.4); }
    
    /* High Signal: 權威認證標章樣式 */
    .trust-badge {
        border: 2px solid #ffd700;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(0,0,0,0.8));
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
        position: relative;
        overflow: hidden;
        margin-top: 20px;
    }
    .trust-badge::before { content: "★ ★ ★ ★ ★"; display: block; color: #ffd700; font-size: 0.8em; letter-spacing: 3px; margin-bottom: 5px; }
    .trust-title { color: #ffd700; font-weight: bold; font-size: 1.1em; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; }
    
    /* Low Signal: 普通聲明樣式 */
    .internal-signal { 
        border-left: 4px solid #607d8b; 
        background: rgba(96, 125, 139, 0.1);
        padding: 15px; 
        color: #b0bec5; 
        font-style: italic; 
        border-radius: 0 8px 8px 0;
        margin-top: 20px;
    }
    
    /* 圖片容器優化 */
    .product-image-container img {
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 數據儲存功能 (CSV) ---
CSV_FILE = 'experiment_data.csv'

def save_to_csv(data):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# --- 4. 狀態管理 ---
if 'init' not in st.session_state:
    st.session_state.clear()
    st.session_state['init'] = True
    # 實驗變因隨機化
    st.session_state['security_level'] = random.choice(['High_Signal', 'Low_Signal']) # 標章 vs 聲明
    st.session_state['privacy_risk'] = random.choice(['High_Risk', 'Low_Risk'])       # 監視器 vs 燈泡
    
    st.session_state['step'] = 'intro'
    st.session_state['submitted'] = False

    # 設定價格
    if st.session_state['privacy_risk'] == 'High_Risk':
        st.session_state['base_price'] = 8000 # 寶寶監視器
    else:
        st.session_state['base_price'] = 750  # 智慧燈泡

def go_next(step_name):
    st.session_state['step'] = step_name
    st.rerun()

# --- 5. 頁面函數 ---

def render_scenario_priming(risk_type):
    st.markdown("## 📢 步驟 1/3：購物情境")
    
    if risk_type == 'High_Risk':
        scenario_html = """
        <div style="background:rgba(255,87,34,0.1); padding:20px; border-left:5px solid #ff5722; border-radius:5px;">
            <h3 style="color:#ffab91; margin-top:0;">👶 情境：守護新生兒</h3>
            <p>您是新手爸媽，為了能隨時查看嬰兒狀況，計畫購買一台<b>「高畫質無線監控攝影機」</b>。</p>
            <p>ℹ️ 市場行情：一般基本款（無特別強調資安）售價約 <b>NT$ 8,000</b>。</p>
            <p>⚠️ <b>您的擔憂：</b>近期駭客入侵家用攝影機的新聞頻傳，您對於<b>「隱私外洩」</b>感到相當焦慮。</p>
        </div>
        """
    else:
        scenario_html = """
        <div style="background:rgba(33,150,243,0.1); padding:20px; border-left:5px solid #2196f3; border-radius:5px;">
            <h3 style="color:#90caf9; margin-top:0;">💡 情境：智慧照明</h3>
            <p>您想換一顆可用手機 App 控制的<b>「智慧 LED 燈泡」</b>。</p>
            <p>ℹ️ 市場行情：一般基本款（無特別強調資安）售價約 <b>NT$ 750</b>。</p>
            <p>ℹ️ <b>您的想法：</b>此設備僅控制燈光，功能單純，您認為<b>隱私風險較低</b>。</p>
        </div>
        """
    
    st.markdown(scenario_html, unsafe_allow_html=True)
    st.write("")
    if st.button("了解行情，前往商店選購 ➡️"):
        go_next('store')

def render_product_page(risk_type, security_level, base_price):
    # 設定顯示價格 (溢價 20%)
    display_price = int(base_price * 1.2)
    
    c1, c2 = st.columns([3, 1])
    with c1: st.markdown('<div class="brand-text">CYBER<span style="color:#00f2ff">STORE</span></div>', unsafe_allow_html=True)
    with c2: st.caption("🛒 Guest_User_007")
    st.markdown("---")

    # 產品內容設定 (加入圖片檔案)
    if risk_type == 'High_Risk':
        prod_name = "SecureView 寶寶監視器 Pro"
        desc = "4K 高畫質 / AI 哭聲偵測 / 雙向語音"
        img_file = "camera.jpg" # 您的圖片檔名
    else:
        prod_name = "LumiSmart 智慧燈泡 Plus"
        desc = "1600萬色 / 音樂律動 / 語音助理支援"
        img_file = "bulb.jpg"   # 您的圖片檔名

    c_img, c_info = st.columns([1, 1.2])
    
    with c_img:
        # --- 顯示真實產品圖片 ---
        st.markdown('<div class="product-image-container">', unsafe_allow_html=True)
        try:
            # 檢查圖片是否存在，避免報錯
            if os.path.exists(img_file):
                st.image(img_file, use_column_width=True)
            else:
                # 如果找不到圖片的備用方案
                st.error(f"找不到圖片: {img_file}")
                st.info("請確認圖片檔案已上傳至 GitHub 根目錄。")
        except Exception as e:
             st.error(f"圖片載入錯誤: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

        
        st.write("")
        # --- 關鍵變因：資安訊號 ---
        if security_level == 'High_Signal':
            st.markdown("""
            <div class="trust-badge">
                <div class="trust-title">🛡️ IoT Cybersecurity</div>
                <div style="font-size:0.8em; color:#fff; margin-top:5px;">GOLD CERTIFIED</div>
                <hr style="border-top: 1px solid rgba(255,215,0,0.5); margin:8px 0;">
                <small style="color:#ddd;">通過第三方滲透測試<br>符合國際資安標準</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="internal-signal">
                <b>🔒 廠商自主聲明：</b><br>
                <small>本產品由原廠工程團隊精心設計，致力於保護您的使用安全與隱私。</small>
            </div>
            """, unsafe_allow_html=True)

    with c_info:
        st.markdown(f"## {prod_name}")
        st.markdown(f"<p style='color:#bbb;'>{desc}</p>", unsafe_allow_html=True)
        
        st.markdown(f'<div class="price-tag">NT$ {display_price:,}</div>', unsafe_allow_html=True)
        st.caption("含稅 | 24h 快速到貨 | 1年原廠保固")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("加入購物車並結帳"):
            with st.spinner("安全連線中..."): time.sleep(0.5)
            go_next('survey')

def render_survey(risk_type, security_level, base_price):
    display_price = int(base_price * 1.2)
    diff_price = display_price - base_price
    
    signal_desc = "獲得「IoT 資安金級標章（第三方認證）」" if security_level == 'High_Signal' else "提供「廠商自主資安聲明」"

    st.markdown("## 📋 步驟 2/3：價值評估")
    st.info("系統提示：訂單已成立。請協助填寫以下滿意度調查，以完成交易。")

    with st.form("data_form"):
        # --- 價格比較與合理性 (WTP Proxy) ---
        st.markdown(f"""
        <div class="price-comparison">
            <h4 style="margin-top:0;">💰 價格分析</h4>
            <p>我們注意到您購買的產品價格略高於市場行情：</p>
            <ul>
                <li>一般市售同級產品（無特別資安強調）：<b>NT$ {base_price:,}</b></li>
                <li>您選購的產品（{signal_desc}）：<b>NT$ {display_price:,}</b></li>
            </ul>
            <hr style="border-color:#555;">
            <p style="text-align:right;">您多支付了： <span class="math-highlight">NT$ {diff_price:,} (+20%)</span></p>
        </div>
        """, unsafe_allow_html=True)

        st.write(f"**1. 考慮到此產品{signal_desc}，您認為多付這 20% (NT$ {diff_price}) 的費用是合理的嗎？**")
        q1_score = st.slider("請滑動評分 (1=非常不合理, 7=非常合理)", 1, 7, 4)

        st.write("**2. 承上題，如果價差進一步擴大，變成貴 30% (即再多加 10%)，您的購買意願是？**")
        q2_wtp_30 = st.select_slider("請選擇", options=["絕對不買", "不太會買", "可能會買", "一定會買"], value="可能會買")
        
        st.write("**3. 您認為這個產品發生「隱私外洩（如被駭客偷看）」的風險有多高？**")
        q3_risk_perc = st.slider("風險感知 (1=非常安全, 7=非常危險)", 1, 7, 4)

        st.write("**4. 您有多信任這個產品提供的資安保障？**")
        q4_trust = st.slider("信任程度 (1=完全不信, 7=非常信任)", 1, 7, 4)

        if st.form_submit_button("提交並結束實驗"):
            # 準備數據
            record = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Product_Type": risk_type,      # 高風險/低風險
                "Signal_Type": security_level,  # 強訊號/弱訊號
                "Base_Price": base_price,
                "Diff_Price": diff_price,
                "Q1_Reasonableness_20pct": q1_score,
                "Q2_WTP_30pct": q2_wtp_30,
                "Q3_Risk_Perception": q3_risk_perc,
                "Q4_Trust_Level": q4_trust
            }
            save_to_csv(record)
            st.session_state['submitted'] = True
            st.rerun()

    if st.session_state['submitted']:
        st.success("✅ 數據已成功儲存！感謝您的參與。")
        st.balloons()
        
        # 顯示簡易統計 (給你看的，實際實驗時可以隱藏)
        st.markdown("### 📊 目前數據預覽 (Debug Mode)")
        if os.path.exists(CSV_FILE):
            import pandas as pd
            df = pd.read_csv(CSV_FILE)
            st.dataframe(df.tail(3)) # 顯示最後3筆

        if st.button("重置實驗 (下一位受測者)"):
            st.session_state.clear()
            st.rerun()

# --- 6. 流程控制 ---
if st.session_state['step'] == 'intro':
    st.title("🛡️ 智慧家電消費決策實驗")
    st.markdown("""
    歡迎參與本實驗。
    本實驗將模擬真實的網購情境，請您放鬆心情，依照您的**直覺**進行判斷與決策。
    
    * 實驗時間：約 2 分鐘
    * 您的數據僅供學術研究使用
    """)
    if st.button("開始實驗"): go_next('priming')

elif st.session_state['step'] == 'priming':
    render_scenario_priming(st.session_state['privacy_risk'])

elif st.session_state['step'] == 'store':
    render_product_page(st.session_state['privacy_risk'], 
                       st.session_state['security_level'], 
                       st.session_state['base_price'])

elif st.session_state['step'] == 'survey':
    render_survey(st.session_state['privacy_risk'], 
                 st.session_state['security_level'], 
                 st.session_state['base_price'])
