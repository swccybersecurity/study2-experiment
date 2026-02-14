import streamlit as st
import random
import time
import os

# --- 1. 頁面基本設定 (必須放第一行) ---
st.set_page_config(page_title="購物體驗研究", layout="centered")

# --- 2. 進階美化技巧 (CSS Injection) ---
st.markdown("""
<style>
    /* 讓主按鈕看起來像電商的 '立即結帳' (橘紅色系) */
    .stButton > button {
        background-color: #FF5722;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #E64A19;
        color: white;
        box-shadow: 0 4px 12px rgba(255, 87, 34, 0.3);
    }
    
    /* 圖片美化：圓角 + 陰影 */
    img {
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    
    /* 價格文字特效 */
    .price-tag {
        color: #d32f2f;
        font-size: 1.5em;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
    }
    
    /* 資安標章區塊特效 */
    .security-badge {
        background-color: #e8f5e9;
        border: 1px solid #c8e6c9;
        border-radius: 8px;
        padding: 8px 12px;
        color: #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 核心邏輯：頁面跳轉 (Callback) ---
def go_to_step(next_step):
    st.session_state['step'] = next_step

# --- 4. 初始化 Session State (防呆邏輯) ---
if 'step' not in st.session_state:
    security_levels = ['Strong', 'Weak']
    involvement_levels = ['High', 'Low']
    
    # 隨機分派
    st.session_state['security'] = random.choice(security_levels)
    st.session_state['involvement'] = random.choice(involvement_levels)
    
    # 初始狀態
    st.session_state['step'] = 'consent' 
    st.session_state['start_time'] = time.time()

# --- 5. 介面渲染函數：模擬電商頁面 (讀取 GitHub 本地圖片版) ---
def render_ecommerce_page(security, involvement):
    st.markdown("---")
    
    # === Header 區塊 ===
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🛒 SuperStore 官方旗艦店")
    with col2:
        # [操弄點 1] 強訊號組顯示 ISO 標章與鎖頭
        if security == 'Strong':
            # 使用 Emoji 🔒，解決外部圖片破圖問題
            st.markdown(
                """
                <div class="security-badge" style="display: flex; align-items: center; justify-content: center;">
                    <div style="text-align: right; margin-right: 10px; line-height: 1.2;">
                        <span style="font-weight: bold; font-size: 0.9em;">SSL 安全加密</span><br>
                        <span style="font-size: 0.8em;">ISO 27001 認證</span>
                    </div>
                    <div style="font-size: 2.5rem; line-height: 1; margin-left: 5px;">🔒</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            # 弱訊號組：只顯示一般客服資訊
            st.markdown(
                """
                <div style="text-align: right; color: #666; font-size: 0.8em; padding: 10px;">
                    客服專線：0800-000-123<br>
                    營業時間：09:00-18:00
                </div>
                """, unsafe_allow_html=True
            )

    st.markdown("---")
    
    # === Product 區塊 ===
    prod_col1, prod_col2 = st.columns([1, 1.5], gap="large")
    
    with prod_col1:
        # [操弄點 2] 根據涉入度顯示不同圖片 (直接讀取 GitHub 上的檔案)
        if involvement == 'High':
            # 筆電圖片 (注意：檔名大小寫必須與 GitHub 上完全一致)
            img_path = "Lp.AVIF"  
            product_name = "ProBook X1 - 商務旗艦筆電"
            desc = "搭載最新 AI 處理器 / 32GB RAM / 1TB SSD / 24小時續航"
            price = "NT$ 45,900"
        else:
            # 文具圖片 (注意：檔名大小寫必須與 GitHub 上完全一致)
            img_path = "Pen.jpg"
            product_name = "極簡風格原子筆組 (3入)"
            desc = "滑順好寫 / 速乾墨水 / 經典黑藍紅三色 / 學生辦公首選"
            price = "NT$ 150"
        
        # 檢查檔案是否存在 (防呆機制)
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            # 如果讀不到檔案，顯示錯誤訊息 (方便除錯)
            st.error(f"找不到圖片: {img_path}")
            st.caption("請確認 GitHub 上的檔名大小寫是否完全一致，且檔案位於根目錄。")

    with prod_col2:
        st.markdown(f"### {product_name}")
        st.caption(desc)
        st.markdown(f"<div class='price-tag'>{price}</div>", unsafe_allow_html=True)
        
        st.write("---")
        
        # 模擬結帳欄位
        st.text_input("💳 信用卡號碼", placeholder="**** **** **** 1234", disabled=True)
        col_exp, col_cvc = st.columns(2)
        with col_exp:
            st.text_input("有效期限", placeholder="MM/YY", disabled=True)
        with col_cvc:
            st.text_input("CVC", placeholder="123", disabled=True)
            
        st.text_input("📍 收件地址", placeholder="請輸入您的收件地址...", disabled=True)
        
        # [操弄點 3] 強訊號組的額外承諾
        if security == 'Strong':
            st.success("🛡️ **資安承諾**：本站採用金融級加密技術，若發生個資外洩，我們承諾提供**全額賠償**。")
        
        st.button("確認結帳 (模擬按鈕)", disabled=True)
    
    st.markdown("---")

# --- 6. 主程式流程控制 ---

# 階段 1: 知情同意
if st.session_state['step'] == 'consent':
    st.title("🛒 消費者購物體驗研究")
    st.info("👋 歡迎參與本研究！")
    st.write("""
    本研究旨在了解消費者的網購決策過程。
    在下一頁中，您將看到一個**模擬的購物網站頁面**。
    
    請您想像自己**正準備購買該商品**，並仔細閱讀頁面上的資訊。
    """)
    
    st.write("")
    st.button("我已了解，開始實驗 👉", on_click=go_to_step, args=['stimulus'])

# 階段 2: 實驗刺激
elif st.session_state['step'] == 'stimulus':
    st.write("### 請瀏覽下方的商品頁面")
    
    render_ecommerce_page(st.session_state['security'], st.session_state['involvement'])
    
    st.warning("⚠️ 請確認您已仔細閱讀頁面資訊（包含商品、價格、版面標示等）")
    st.button("我已閱讀完畢，填寫問卷 👉", on_click=go_to_step, args=['survey'])

# 階段 3: 問卷填答
elif st.session_state['step'] == 'survey':
    st.title("📝 填答反應")
    st.write("請根據剛剛看到的網頁，回答以下問題：")
    
    with st.form("survey_form"):
        st.write("#### 1. 操弄檢核")
        st.write("您覺得剛剛的網站是否強調「資訊安全」？")
        check_q = st.slider("1 (完全不強調) - 7 (非常強調)", 1, 7, 4)
        
        st.write("#### 2. 網站信任度")
        st.write("您對該網站的信任程度？")
        trust_q = st.slider("1 (非常不信任) - 7 (非常信任)", 1, 7, 4)
        
        st.write("#### 3. 風險感知")
        st.write("您認為在此網站輸入信用卡號的風險高嗎？")
        risk_q = st.slider("1 (風險極低) - 7 (風險極高)", 1, 7, 4)
        
        st.write("#### 4. 購買意願 (WTP)")
        st.write("您最高願意支付多少錢購買此商品？ (請輸入數字)")
        wtp_val = st.number_input("金額 (NT$)", min_value=0, step=10)
        
        submitted = st.form_submit_button("送出答案")
        
        if submitted:
            st.session_state['data'] = {
                "Group_Security": st.session_state['security'],
                "Group_Involvement": st.session_state['involvement'],
                "Check_Score": check_q,
                "Trust_Score": trust_q,
                "Risk_Score": risk_q,
                "WTP": wtp_val
            }
            st.session_state['step'] = 'finish'
            st.rerun()

# 階段 4: 結束
elif st.session_state['step'] == 'finish':
    st.balloons() # 撒花特效 🎉
    st.success("✅ 感謝您的填答！實驗結束。")
    
    st.markdown("### 【Demo 模式：後台數據】")
    st.code(st.session_state.get('data', {}), language='json')
    
    st.info(f"當前受試者組別：{st.session_state['security']} Signal / {st.session_state['involvement']} Involvement")
    
    def reset_exp():
        st.session_state.clear()
        
    st.button("🔄 重新開始 (測試下一組)", on_click=reset_exp)
