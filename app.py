import streamlit as st
import random
import time

st.set_page_config(page_title="購物體驗研究", layout="centered")

# --- 核心改動 1: 定義跳轉函式 (Callback) ---
# 這個函式會在按鈕按下的「瞬間」執行，比頁面刷新還快
def go_to_step(next_step):
    st.session_state['step'] = next_step
    # 這裡不需要 st.rerun()，因為 on_click 執行完會自動 rerun

# --- 初始化 Session State ---
if 'experiment_group' not in st.session_state:
    security_levels = ['Strong', 'Weak']
    involvement_levels = ['High', 'Low']
    
    st.session_state['security'] = random.choice(security_levels)
    st.session_state['involvement'] = random.choice(involvement_levels)
    st.session_state['step'] = 'consent' 
    st.session_state['start_time'] = time.time()

# --- 輔助函數：模擬電商介面 (不用改) ---
def render_ecommerce_page(security, involvement):
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("🛒 SuperStore 結帳櫃檯")
    with col2:
        if security == 'Strong':
            st.markdown("""<div style="text-align: right; color: green; font-size: 0.8em;">🔒 <b>SSL 加密連線</b><br>✅ <b>ISO 27001 認證</b></div>""", unsafe_allow_html=True)

    st.markdown("---")
    prod_col1, prod_col2 = st.columns([1, 2])
    
    with prod_col1:
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
        st.text_input("信用卡號碼", placeholder="**** **** **** 1234", disabled=True)
        st.text_input("收件地址", placeholder="請輸入您的地址...", disabled=True)
        if security == 'Strong':
            st.info("🛡️ **安心保證**：本站若發生個資外洩，承諾提供全額賠償。")
        st.button("確認結帳 (模擬按鈕)", disabled=True)
    st.markdown("---")

# --- 主程式流程 ---

# 階段 1: 知情同意
if st.session_state['step'] == 'consent':
    st.title("消費者購物體驗研究")
    st.write("您好，感謝您參與本研究。本研究旨在了解消費者的網購體驗。")
    st.write("請想像您正在瀏覽接下來的購物網站，並準備進行結帳。")
    
    # --- 核心改動 2: 使用 on_click ---
    st.button("我同意參與並開始", on_click=go_to_step, args=['stimulus'])

# 階段 2: 實驗刺激
elif st.session_state['step'] == 'stimulus':
    st.write("### 請仔細閱讀下方的結帳頁面")
    st.caption("請想像您真的要購買此商品，觀察頁面上的資訊。")
    
    render_ecommerce_page(st.session_state['security'], st.session_state['involvement'])
    
    st.write("")
    st.write("")
    # --- 核心改動 3: 使用 on_click ---
    st.button("我已閱讀完畢，進入問卷", on_click=go_to_step, args=['survey'])

# 階段 3: 問卷填答
elif st.session_state['step'] == 'survey':
    st.title("填答反應")
    
    with st.form("survey_form"):
        st.write("#### 1. 您認為該網站是否重視資訊安全？")
        check_q = st.slider("1 (非常不重視) - 7 (非常重視)", 1, 7, 4)
        
        st.write("#### 2. 您對該網站的信任程度？")
        trust_q = st.slider("1 (非常不信任) - 7 (非常信任)", 1, 7, 4)
        
        st.write("#### 3. 您認為在此網站交易的風險高嗎？")
        risk_q = st.slider("1 (風險極低) - 7 (風險極高)", 1, 7, 4)
        
        st.write("#### 4. 您最高願意支付多少錢購買此商品？")
        wtp_val = st.number_input("請輸入金額 (NT$)", min_value=0, step=10)
        
        # 表單提交按鈕
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
            # 因為在 form 裡面不能直接用 on_click 跳轉，這裡用手動切換 + rerun
            st.session_state['step'] = 'finish'
            st.rerun()

# 階段 4: 結束
elif st.session_state['step'] == 'finish':
    st.success("感謝您的填答！實驗結束。")
    st.subheader("【Demo 模式：後台數據預覽】")
    st.json(st.session_state.get('data', {}))
    
    # 重置按鈕
    def reset_exp():
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    st.button("重新開始 (測試用)", on_click=reset_exp)
