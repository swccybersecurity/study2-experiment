import os
import csv
import uuid
import time
import random
import threading
from datetime import datetime

import pandas as pd
import streamlit as st

# =========================
# 1. 基本設定與全域變數
# =========================
st.set_page_config(
    page_title="Cybersecurity Label Experiment v4",
    page_icon="🛡️",
    layout="centered"
)

CSV_FILE = "experiment_data_v4.csv"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
csv_lock = threading.Lock() # 用於防止多人同時寫入CSV的Race Condition

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        color: #e8eef5;
    }
    .card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .brand {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 1px;
    }
    .subtle {
        color: #b7c4d1;
        font-size: 0.95rem;
    }
    .price {
        font-size: 2rem;
        font-weight: 700;
        color: #00e5ff;
    }
    .signal-strong {
        border: 2px solid #ffd54f;
        background: rgba(255, 213, 79, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-top: 12px;
    }
    .signal-weak {
        border-left: 4px solid #90a4ae;
        background: rgba(144, 164, 174, 0.08);
        border-radius: 0 10px 10px 0;
        padding: 16px;
        margin-top: 12px;
    }
    .scenario-high {
        background: rgba(255, 87, 34, 0.10);
        border-left: 5px solid #ff7043;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .scenario-low {
        background: rgba(33, 150, 243, 0.10);
        border-left: 5px solid #42a5f5;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .small-note {
        color: #9fb0c3;
        font-size: 0.88rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 2. 工具函數
# =========================
def init_session():
    if "participant_id" not in st.session_state:
        st.session_state["participant_id"] = str(uuid.uuid4())[:8]

    if "condition_initialized" not in st.session_state:
        st.session_state["condition_initialized"] = True
        st.session_state["signal_type"] = random.choice(["High_Signal", "Low_Signal"])
        st.session_state["privacy_context"] = random.choice(["High_Privacy", "Low_Privacy"])
        st.session_state["step"] = "intro"
        st.session_state["survey_data"] = {} # 暫存跨頁問卷資料
        st.session_state["opened_signal_doc"] = False
        st.session_state["product_time_sec"] = 0.0
        st.session_state["attitude_time_sec"] = 0.0

    if "page_start_time" not in st.session_state:
        st.session_state["page_start_time"] = time.time()

def set_step(step_name: str):
    """切換頁面狀態，重置計時器並強制重整。"""
    st.session_state["step"] = step_name
    st.session_state["page_start_time"] = time.time()
    st.rerun()

def get_elapsed_seconds():
    return round(time.time() - st.session_state.get("page_start_time", time.time()), 2)

def save_to_csv(data: dict):
    with csv_lock: # 使用 Thread Lock 確保多受試者併發寫入安全
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=list(data.keys()))
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

def reset_for_next_participant():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def get_product_info(privacy_context: str):
    info = {
        "brand": "SecureView",
        "product_name": "SecureView Home Cam X1",
        "category": "無線家用攝影裝置",
        "features": "2K 高畫質 / 夜視 / App 遠端查看 / 雙向語音",
        "base_price": 8000
    }
    if privacy_context == "High_Privacy":
        info["scenario_title"] = "高隱私敏感情境：嬰兒房／臥室照護"
        info["scenario_icon"] = "👶"
        info["scenario_class"] = "scenario-high"
        info["image_file"] = "baby.PNG"
        info["scenario_desc"] = (
            "您正考慮購買一台家用攝影裝置，用於嬰兒房或臥室照護。"
            "由於此情境涉及家庭私密空間、兒童活動與日常作息，"
            "若影像遭未授權存取，可能造成明顯的隱私風險與心理壓力。"
        )
    else:
        info["scenario_title"] = "低隱私敏感情境：玄關外／車庫監看"
        info["scenario_icon"] = "🚪"
        info["scenario_class"] = "scenario-low"
        info["image_file"] = "garage.PNG"
        info["scenario_desc"] = (
            "您正考慮購買一台家用攝影裝置，用於玄關外或車庫等外部空間監看。"
            "此情境雖然仍涉及安全與監控功能，但相較於室內私密空間，"
            "您認為資料暴露造成的隱私敏感程度較低。"
        )
    return info

def get_price_schedule(base_price: int):
    premiums = [0, 5, 10, 15, 20, 25, 30]
    rows = []
    for p in premiums:
        target_price = int(round(base_price * (1 + p / 100)))
        rows.append({"premium_pct": p, "target_price": target_price})
    return rows

def infer_wtp_switch(responses: dict):
    accepted = []
    for pct in sorted(responses.keys()):
        if responses[pct] == "會":
            accepted.append(pct)
    if len(accepted) == 0:
        return -1
    return max(accepted)

def is_non_monotonic(mpl_answers: dict):
    sorted_keys = sorted(mpl_answers.keys())
    numeric_pattern = [1 if mpl_answers[k] == "會" else 0 for k in sorted_keys]
    seen_zero = False
    for v in numeric_pattern:
        if v == 0:
            seen_zero = True
        if seen_zero and v == 1:
            return True
    return False

# =========================
# 3. 畫面區塊 (Steps)
# =========================
def render_intro():
    st.title("🛡️ 智慧設備消費決策研究")
    st.markdown(
        """
        歡迎參與本研究。  
        本研究將模擬一段簡短的商品評估情境，請您依照**直覺與真實想法**回答。

        - 作答時間：約 3–5 分鐘
        - 您的資料僅供學術研究分析
        - 本研究不蒐集不必要之個人身分資訊
        """
    )
    if st.button("開始研究"):
        set_step("scenario")

def render_scenario():
    info = get_product_info(st.session_state["privacy_context"])

    st.markdown("## 步驟 1/5：使用情境")
    st.markdown(
        f"""
        <div class="{info["scenario_class"]}">
            <h3>{info["scenario_icon"]} {info["scenario_title"]}</h3>
            <p>{info["scenario_desc"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("請想像您正在評估是否購買此產品，接下來您將看到商品頁面。")
    if st.button("查看商品頁面"):
        set_step("product")

def render_product():
    info = get_product_info(st.session_state["privacy_context"])
    # 修正錨點：商品頁面直接顯示市場基準價 8,000，不預先加上溢價
    display_price = info["base_price"] 
    signal_type = st.session_state["signal_type"]

    st.markdown("## 步驟 2/5：商品資訊")
    st.markdown('<div class="brand">CYBERSTORE</div>', unsafe_allow_html=True)
    st.markdown("---")

    left, right = st.columns([1, 1.2])
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        img_path = info["image_file"]
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.warning(f"⚠️ 找不到圖片：{img_path}")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(f"### {info['product_name']}")
        st.markdown(f"**產品類型：** {info['category']}")
        st.markdown(f"**主要功能：** {info['features']}")
        st.markdown(f'<div class="price">NT$ {display_price:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtle">含稅／標準保固／App 支援</div>', unsafe_allow_html=True)

        if signal_type == "High_Signal":
            st.markdown(
                """
                <div class="signal-strong">
                    <b>🛡️ 第三方產品級資安標示</b><br>
                    本產品通過第三方檢測機構之產品級安全測試，並取得獨立驗證之資安標示。<br><br>
                    <span class="small-note">文件內容強調：具基本帳號保護、更新機制與安全設定要求。</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="signal-weak">
                    <b>🔒 品牌自述式隱私／資安聲明</b><br>
                    本品牌表示產品設計重視使用者隱私與安全，並承諾將持續改善系統防護。<br><br>
                    <span class="small-note">文件內容為品牌自我聲明，未呈現外部驗證資訊。</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    with st.expander("查看資安資訊文件（選填）"):
        st.session_state["opened_signal_doc"] = True
        if signal_type == "High_Signal":
            st.write("文件摘要：本產品已完成第三方產品級安全測試，測試內容包含帳號保護、軟體更新、基本設定安全與未授權存取防護等。")
        else:
            st.write("文件摘要：本品牌表示產品設計已考量使用者隱私與安全，並由內部團隊持續維護產品品質。")

    st.markdown("---")
    if st.button("進入品牌評估問卷"):
        st.session_state["product_time_sec"] = get_elapsed_seconds()
        set_step("survey_attitude")

def render_survey_attitude():
    scale_7 = [1, 2, 3, 4, 5, 6, 7]
    st.markdown("## 步驟 3/5：產品與品牌評估")
    st.info("請根據您剛剛看到的商品資訊與情境回答。所有題目皆為必填。")

    with st.form("form_attitude"):
        st.markdown("### A. 資訊確認與觀感")
        attention_check = st.radio("注意力檢查：您剛剛看到的產品是什麼類型？", ["智慧燈泡", "家用攝影裝置", "智慧手錶", "藍牙耳機"], index=None)
        signal_source_check = st.radio("您剛剛看到的安全資訊主要來自哪一種來源？", ["第三方驗證／獨立標示", "品牌自行聲明", "我不確定"], index=None)
        
        q_sc_1 = st.radio("我認為該資安資訊是可信的。", scale_7, horizontal=True, index=None)
        q_sc_2 = st.radio("我認為該資安資訊具有專業性。", scale_7, horizontal=True, index=None)
        q_pr_1 = st.radio("我擔心此產品可能造成隱私外洩。", scale_7, horizontal=True, index=None)
        q_pr_2 = st.radio("我認為使用此產品會讓我承擔隱私風險。", scale_7, horizontal=True, index=None)

        st.markdown("### B. 品牌信任評估")
        q_bt_1 = st.radio("我認為這個品牌是可靠的。", scale_7, horizontal=True, index=None)
        q_bt_2 = st.radio("我相信這個品牌會顧及使用者利益。", scale_7, horizontal=True, index=None)
        q_bt_3 = st.radio("我相信這個品牌不會讓我承擔不必要的資料安全風險。", scale_7, horizontal=True, index=None)

        submit_attitude = st.form_submit_button("下一頁：價格與購買意願")

        if submit_attitude:
            fields = [attention_check, signal_source_check, q_sc_1, q_sc_2, q_pr_1, q_pr_2, q_bt_1, q_bt_2, q_bt_3]
            if None in fields:
                st.error("⚠️ 請確認所有題目皆已完成。")
            else:
                st.session_state["attitude_time_sec"] = get_elapsed_seconds()
                # 暫存資料
                st.session_state["survey_data"].update({
                    "attention_check_product": attention_check,
                    "signal_source_check": signal_source_check,
                    "q_sc_1": q_sc_1, "q_sc_2": q_sc_2,
                    "signal_credibility_avg": round((q_sc_1 + q_sc_2) / 2, 3),
                    "q_pr_1": q_pr_1, "q_pr_2": q_pr_2,
                    "privacy_risk_avg": round((q_pr_1 + q_pr_2) / 2, 3),
                    "q_bt_1": q_bt_1, "q_bt_2": q_bt_2, "q_bt_3": q_bt_3,
                    "brand_trust_avg": round((q_bt_1 + q_bt_2 + q_bt_3) / 3, 3)
                })
                set_step("survey_mpl")

def render_survey_mpl():
    info = get_product_info(st.session_state["privacy_context"])
    base_price = info["base_price"]
    scale_7 = [1, 2, 3, 4, 5, 6, 7]

    st.markdown("## 步驟 4/5：價格評估與個人背景")

    with st.form("form_mpl"):
        st.markdown("### C. 購買決策與價格接受度")
        q_pi_1 = st.radio("若我近期有需求，我會考慮購買此產品。", scale_7, horizontal=True, index=None)
        q_pi_2 = st.radio("整體而言，我對此產品有購買傾向。", scale_7, horizontal=True, index=None)

        st.markdown("---")
        st.markdown(
            f"**情境假設：**\n\n"
            f"請假設市場上**一般同規格，但未經任何第三方資安驗證的同類常態產品**，其基準價格約為 **NT$ {base_price:,}**。\n\n"
            f"以下列出了幾個不同的定價情境。請評估您剛剛看過的那款產品（包含其提供的安全資訊），若它的售價高於市場基準，您是否仍願意購買它？"
        )

        price_rows = get_price_schedule(base_price)
        mpl_answers = {}
        for row in price_rows:
            pct = row["premium_pct"]
            target_price = row["target_price"]
            answer = st.radio(
                f"若此產品售價為 NT$ {target_price:,}（比基準價高 {pct}%），您是否仍會購買此產品？",
                ["會", "不會"], horizontal=True, index=None, key=f"mpl_{pct}"
            )
            mpl_answers[pct] = answer

        st.markdown("### D. 個人背景與經驗")
        privacy_concern = st.radio("整體而言，我平時很重視個人隱私。(1=非常不同意，7=非常同意)", scale_7, horizontal=True, index=None)
        digital_familiarity = st.radio("我對智慧家電／聯網設備相當熟悉。(1=非常不同意，7=非常同意)", scale_7, horizontal=True, index=None)
        data_breach_experience = st.radio("您是否曾有帳號外洩、詐騙或個資風險相關經驗？", ["有", "沒有", "不確定"], index=None)

        submit_mpl = st.form_submit_button("完成並提交")

        if submit_mpl:
            all_required = [q_pi_1, q_pi_2, privacy_concern, digital_familiarity, data_breach_experience] + list(mpl_answers.values())
            if None in all_required:
                st.error("⚠️ 請確認所有題目皆已完成。")
            else:
                mpl_time_sec = get_elapsed_seconds()
                highest_accepted_premium = infer_wtp_switch(mpl_answers)
                non_monotonic = is_non_monotonic(mpl_answers)

                # 合併資料
                record = {
                    "participant_id": st.session_state["participant_id"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "signal_type": st.session_state["signal_type"],
                    "privacy_context": st.session_state["privacy_context"],
                    "product_name": info["product_name"],
                    "base_price": base_price,
                    
                    "opened_signal_doc": st.session_state["opened_signal_doc"],
                    "product_page_time_sec": st.session_state["product_time_sec"],
                    "attitude_page_time_sec": st.session_state["attitude_time_sec"],
                    "mpl_page_time_sec": mpl_time_sec,
                }
                
                # 更新 A & B 區塊資料
                record.update(st.session_state["survey_data"])

                # 更新 C & D 區塊資料
                record.update({
                    "q_pi_1": q_pi_1, "q_pi_2": q_pi_2,
                    "purchase_intention_avg": round((q_pi_1 + q_pi_2) / 2, 3),
                    "mpl_0": mpl_answers[0], "mpl_5": mpl_answers[5],
                    "mpl_10": mpl_answers[10], "mpl_15": mpl_answers[15],
                    "mpl_20": mpl_answers[20], "mpl_25": mpl_answers[25],
                    "mpl_30": mpl_answers[30],
                    "highest_accepted_premium_pct": highest_accepted_premium,
                    "mpl_non_monotonic": non_monotonic,
                    "privacy_concern": privacy_concern,
                    "digital_familiarity": digital_familiarity,
                    "data_breach_experience": data_breach_experience
                })

                save_to_csv(record)
                set_step("thanks")

def render_thanks():
    st.markdown("## 步驟 5/5：完成")
    st.success("✅ 您已完成本研究，感謝您的參與。")
    st.balloons()
    st.write(f"受試者編號：**{st.session_state['participant_id']}**")
    if st.button("下一位受試者"):
        reset_for_next_participant()

def render_sidebar_admin():
    st.sidebar.markdown("---")
    st.sidebar.header("🔧 管理員專區")
    
    # 修正密碼安全性 Edge Case (避免空字串破解)
    if ADMIN_PASSWORD and ADMIN_PASSWORD != "":
        admin_input = st.sidebar.text_input("輸入管理密碼", type="password")
        if admin_input == ADMIN_PASSWORD:
            if os.path.exists(CSV_FILE):
                df = pd.read_csv(CSV_FILE)
                st.sidebar.success(f"目前已收集 {len(df)} 筆資料")
                csv_data = df.to_csv(index=False).encode("utf-8-sig")
                st.sidebar.download_button(
                    label="📥 下載資料 CSV",
                    data=csv_data,
                    file_name="experiment_data_v4.csv",
                    mime="text/csv"
                )
            else:
                st.sidebar.warning("目前尚無資料。")
    else:
        st.sidebar.caption("未設定有效的 ADMIN_PASSWORD 環境變數，管理功能停用。")

# =========================
# 4. 主流程路由
# =========================
init_session()
render_sidebar_admin()

step = st.session_state["step"]

if step == "intro":
    render_intro()
elif step == "scenario":
    render_scenario()
elif step == "product":
    render_product()
elif step == "survey_attitude":
    render_survey_attitude()
elif step == "survey_mpl":
    render_survey_mpl()
elif step == "thanks":
    render_thanks()
