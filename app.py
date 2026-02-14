import streamlit as st
import random
import time

# --- 設定頁面配置 ---
st.set_page_config(page_title="購物體驗研究", layout="centered")

# --- 1. 初始化 Session State (確保受試者分組後不會變動) ---
if 'experiment_group' not in st.session_state:
    # 定義因子
    security_levels = ['Strong', 'Weak']   # 資安訊號 (強/弱)
    involvement_levels = ['High', 'Low']   # 產品涉入度 (高/低)
    
    # 隨機分派 (2x2 設計)
    st.session_state['security'] = random.choice(security_levels)
    st.session_state['involvement'] = random.choice(involvement_levels)
    
    # 記錄當前頁面步驟
    st.session_state['step'] = 'consent' # consent -> stimulus -> survey -> finish
    
    # 記錄開始時間
    st.session_state['start_time'] = time.time()

# --- 輔助函數：模擬電商介面 ---
def render_ecommerce_page(security, involvement):
    st.markdown("---")
    
    # === A. 頂部導覽列與資安訊號 (Header Manipulation) ===
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("🛒 SuperStore 結帳櫃檯")
    
    with col2:
        # [操弄點 1] 強訊號組顯示 ISO 標章與鎖頭
        if security == 'Strong':
            st.markdown(
                """
                <div style="text-align: right; color: green; font-size: 0.8em;">
                    🔒 <b>SSL 加密連線</b><br>
                    ✅ <b>ISO 27001 認證</b>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            # 弱訊號組什麼都不顯示
            pass

    st.markdown("---")

    # === B. 產品呈現 (Product Manipulation) ===
    prod_col1, prod_col2 = st.columns([1, 2])
    
    with prod_col1:
        # [操弄點 2] 根據涉入度顯示不同產品圖片 (這裡用 placeholder 代替)
        if involvement == 'High':
            st.image("https://placehold.co/300x300/EEE/31343C?text=Laptop", caption="高階商務筆電")
            price = "NT$ 45,900"
            product_name = "ProBook X1 - 極致效能版"
        else:
            st.image("https://placehold.co/300x300/EEE/31343C?text=Pen", caption="精美文具組")
            price = "NT$ 150"
            product_name = "極簡風格原子筆組 (3入)"

    with prod_col2:
        st.write(f"### {product_name}")
        st.write(f"**價格：{price}**")
        st.write("運費：免運費")
        
        # 模擬信用卡輸入框 (裝飾用)
        st.text_input("信用卡號碼", placeholder="**** **** **** 1234", disabled=True)
        st.text_input("收件地址", placeholder="請輸入您的地址...", disabled=True)
        
        # [操弄點 3] 強訊號組的額外承諾
        if security == 'Strong':
            st.info("🛡️ **安心保證**：本站若發生個資外洩，承諾提供全額賠償。")
        
        st.button("確認結帳 (模擬按鈕)", disabled=True)

    st.markdown("---")

# --- 主程式流程控制 ---

# 階段 1: 知情同意與說明
if st.session_state['step'] == 'consent':
    st.title("消費者購物體驗研究")
    st.write("您好，感謝您參與本研究。本研究旨在了解消費者的網購體驗。")
    st.write("請想像您正在瀏覽接下來的購物網站，並準備進行結帳。")
    
    if st.button("我同意參與並開始"):
        st.session_state['step'] = 'stimulus'
        st.rerun()

# 階段 2: 實驗刺激 (模擬網頁)
elif st.session_state['step'] == 'stimulus':
    st.write("### 請仔細閱讀下方的結帳頁面")
    st.caption("請想像您真的要購買此商品，觀察頁面上的資訊。")
    
    # 呼叫模擬頁面函數，傳入隨機分派的結果
    render_ecommerce_page(st.session_state['security'], st.session_state['involvement'])
    
    st.write("")
    st.write("")
    if st.button("我已閱讀完畢，進入問卷"):
        st.session_state['step'] = 'survey'
        st.rerun()

# 階段 3: 問卷填答
elif st.session_state['step'] == 'survey':
    st.title("填答反應")
    
    with st.form("survey_form"):
        # 操弄檢核
        st.write("#### 1. 您認為該網站是否重視資訊安全？")
        check_q = st.slider("1 (非常不重視) - 7 (非常重視)", 1, 7, 4)
        
        # 依變項：信任度
        st.write("#### 2. 您對該網站的信任程度？")
        trust_q = st.slider("1 (非常不信任) - 7 (非常信任)", 1, 7, 4)
        
        # 依變項：風險感知
        st.write("#### 3. 您認為在此網站交易的風險高嗎？")
        risk_q = st.slider("1 (風險極低) - 7 (風險極高)", 1, 7, 4)
        
        # 依變項：WTP
        st.write("#### 4. 您最高願意支付多少錢購買此商品？")
        wtp_val = st.number_input("請輸入金額 (NT$)", min_value=0, step=10)
        
        submitted = st.form_submit_button("送出答案")
        
        if submitted:
            # 在這裡收集資料
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

# 階段 4: 結束與資料展示 (Demo 用)
elif st.session_state['step'] == 'finish':
    st.success("感謝您的填答！實驗結束。")
    
    st.subheader("【Demo 模式：後台數據預覽】")
    st.write("正式實驗時，這部分受試者看不到，數據會自動存入資料庫。")
    st.json(st.session_state['data'])
    
    if st.button("重新開始 (測試用)"):
        # 清除狀態，重新隨機分派
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
