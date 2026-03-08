import os
import csv
import uuid
import time
import random
from datetime import datetime

import pandas as pd
import streamlit as st

# =========================
# 1. 基本設定
# =========================
st.set_page_config(
    page_title="Cybersecurity Label Experiment",
    page_icon="🛡️",
    layout="centered"
)

CSV_FILE = "experiment_data_v2.csv"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

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
        st.session_state["submitted"] = False
        st.session_state["opened_signal_doc"] = False
        st.session_state["product_time_sec"] = 0.0  # 記錄商品頁停留時間

    if "page_start_time" not in st.session_state:
        st.session_state["page_start_time"] = time.time()

def set_step(step_name: str):
    st.session_state["step"] = step_name
    st.session_state["page_start_time"] = time.time()
    st.rerun()

def get_elapsed_seconds():
    return round(time.time() - st.session_state.get("page_start_time", time.time()), 2)

def save_to_csv(data: dict):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(data.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def reset_for_next_participant():
    keys_to_keep = []
    for k in list(st.session_state.keys()):
        if k not in keys_to_keep:
            del st.session_state[k]
    st.rerun()

def get_product_info(privacy_context: str):
    """
    動態切換情境文字與 GitHub 上的圖片檔名
    """
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
        info["image_file"] = "baby.PNG"  # 👈 對應您 GitHub 上傳的高風險圖片
        info["scenario_desc"] = (
            "您正考慮購買一台家用攝影裝置，用於嬰兒房或臥室照護。"
            "由於此情境涉及家庭私密空間、兒童活動與日常作息，"
            "若影像遭未授權存取，可能造成明顯的隱私風險與心理壓力。"
        )
    else:
        info["scenario_title"] = "低隱私敏感情境：玄關外／車庫監看"
        info["scenario_icon"] = "🚪"
        info["scenario_class"] = "scenario-low"
        info["image_file"] = "garage.PNG"  # 👈 對應您 GitHub 上傳的低風險圖片
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
        rows.append({
            "premium_pct": p,
            "target_price": target_price
        })
    return rows

def infer_wtp_switch(responses: dict):
    accepted = []
    for pct in sorted(responses.keys()):
        if responses[pct] == "會":
            accepted.append(pct)
    if len(accepted) == 0:
        return -1
    return max(accepted)

# =========================
# 3. 畫面區塊
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
    with st.expander("研究參與說明"):
        st.write(
            "您將閱讀一段商品情境與產品資訊，接著回答幾個關於風險、信任、"
            "購買意願與價格判斷的問題。您可隨時停止作答。"
        )
    if st.button("開始研究"):
        set_step("scenario")

def render_scenario():
    info = get_product_info(st.session_state["privacy_context"])
    st.markdown("## 步驟 1/4：使用情境")
    st.markdown(
        f"""
        <div class="{info["scenario_class"]}">
            <h3>{info["scenario_icon"]} {info["scenario_title"]}</h3>
            <p>{info["scenario_desc"]}</p>
            <p><b>市場基準價格：</b>約 NT$ {info["base_price"]:,}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("請想像您正在評估是否購買此產品，接下來您將看到一個商品頁面。")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("返回上一頁"):
            set_step("intro")
    with col2:
        if st.button("查看商品頁面"):
            set_step("product")

def render_product():
    info = get_product_info(st.session_state["privacy_context"])
    base_price = info["base_price"]
    display_price = int(round(base_price * 1.20))
    signal_type = st.session_state["signal_type"]

    st.markdown("## 步驟 2/4：商品資訊")
    st.markdown('<div class="brand">CYBERSTORE</div>', unsafe_allow_html=True)
    st.markdown("---")

    left, right = st.columns([1, 1.2])
    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # 讀取對應的圖片 (動態抓取 GitHub 上的 baby.PNG 或 garage.PNG)
        img_path = info["image_file"]
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.warning(f"⚠️ 找不到圖片：{img_path}")
            st.info("請確認 GitHub 上的檔名與大小寫是否完全一致。")
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
                    本產品通過第三方檢測機構之產品級安全測試，
                    並取得獨立驗證之資安標示。<br><br>
                    <span class="small-note">
                    文件內容強調：具基本帳號保護、更新機制與安全設定要求。
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="signal-weak">
                    <b>🔒 品牌自述式隱私／資安聲明</b><br>
                    本品牌表示產品設計重視使用者隱私與安全，
                    並承諾將持續改善系統防護。<br><br>
                    <span class="small-note">
                    文件內容為品牌自我聲明，未呈現外部驗證資訊。
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    with st.expander("查看資安資訊文件"):
        st.session_state["opened_signal_doc"] = True
        if signal_type == "High_Signal":
            st.write(
                "文件摘要：本產品已完成第三方產品級安全測試，"
                "測試內容包含帳號保護、軟體更新、基本設定安全與未授權存取防護等。"
            )
        else:
            st.write(
                "文件摘要：本品牌表示產品設計已考量使用者隱私與安全，"
                "並由內部團隊持續維護產品品質。"
            )

    st.markdown("---")
    st.markdown("請依據目前看到的資訊，進行後續評估。")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("返回情境頁"):
            set_step("scenario")
    with col2:
        if st.button("進入評估問卷"):
            st.session_state["product_time_sec"] = get_elapsed_seconds()
            set_step("survey")

def render_survey():
    info = get_product_info(st.session_state["privacy_context"])
    base_price = info["base_price"]
    signal_type = st.session_state["signal_type"]
    page_time_sec = get_elapsed_seconds()
    
    # 建立 1~7 分的選項陣列，供轉換 Slider 使用
    scale_7 = [1, 2, 3, 4, 5, 6, 7]

    st.markdown("## 步驟 3/4：評估問卷")
    st.info("請根據您剛剛看到的商品資訊與情境，回答以下問題。（請注意：所有題目皆為必填）")

    with st.form("experiment_form"):
        st.markdown("### A. 操弄檢查與主要心理變數")

        attention_check = st.radio(
            "注意力檢查：您剛剛看到的產品是什麼類型？",
            ["智慧燈泡", "家用攝影裝置", "智慧手錶", "藍牙耳機"],
            index=None
        )

        signal_source_check = st.radio(
            "您剛剛看到的安全資訊主要來自哪一種來源？",
            ["第三方驗證／獨立標示", "品牌自行聲明", "我不確定"],
            index=None
        )

        st.markdown("#### 訊號可信度 (1=非常不同意，7=非常同意)")
        q_sc_1 = st.radio("我認為該資安資訊是可信的。", scale_7, horizontal=True, index=None, key="sc1")
        q_sc_2 = st.radio("我認為該資安資訊具有專業性。", scale_7, horizontal=True, index=None, key="sc2")
        q_sc_3 = st.radio("我認為該資安資訊能真實反映產品安全品質。", scale_7, horizontal=True, index=None, key="sc3")

        st.markdown("#### 感知隱私風險 (1=非常不同意，7=非常同意)")
        q_pr_1 = st.radio("我擔心此產品可能造成隱私外洩。", scale_7, horizontal=True, index=None, key="pr1")
        q_pr_2 = st.radio("我擔心此產品可能被未授權存取。", scale_7, horizontal=True, index=None, key="pr2")
        q_pr_3 = st.radio("我認為使用此產品會讓我承擔隱私風險。", scale_7, horizontal=True, index=None, key="pr3")

        st.markdown("#### 品牌信任 (1=非常不同意，7=非常同意)")
        q_bt_1 = st.radio("我認為這個品牌是可靠的。", scale_7, horizontal=True, index=None, key="bt1")
        q_bt_2 = st.radio("我相信這個品牌會顧及使用者利益。", scale_7, horizontal=True, index=None, key="bt2")
        q_bt_3 = st.radio("我相信這個品牌不會讓我承擔不必要的資料安全風險。", scale_7, horizontal=True, index=None, key="bt3")

        st.markdown("#### 購買意願 (1=非常不同意，7=非常同意)")
        q_pi_1 = st.radio("若我近期有需求，我會考慮購買此產品。", scale_7, horizontal=True, index=None, key="pi1")
        q_pi_2 = st.radio("我願意把此產品列入優先考慮名單。", scale_7, horizontal=True, index=None, key="pi2")
        q_pi_3 = st.radio("整體而言，我對此產品有購買傾向。", scale_7, horizontal=True, index=None, key="pi3")

        st.markdown("---")
        st.markdown("### B. 價格評估（多重價格列表）")
        st.write(
            f"請假設市場上**一般同類產品基準價格**約為 **NT$ {base_price:,}**。"
            "以下請您在每個價差條件下，判斷您是否仍會選擇目前這個產品。"
        )

        price_rows = get_price_schedule(base_price)
        mpl_answers = {}

        for row in price_rows:
            pct = row["premium_pct"]
            target_price = row["target_price"]
            answer = st.radio(
                f"若此產品售價為 NT$ {target_price:,}（比基準價高 {pct}%），您是否仍會選擇此產品？",
                ["會", "不會"],
                horizontal=True,
                index=None,
                key=f"mpl_{pct}"
            )
            mpl_answers[pct] = answer

        st.markdown("---")
        st.markdown("### C. 背景變數")

        privacy_concern = st.radio("整體而言，我平時很重視個人隱私。(1=非常不同意，7=非常同意)", scale_7, horizontal=True, index=None, key="bg1")
        digital_familiarity = st.radio("我對智慧家電／聯網設備相當熟悉。(1=非常不同意，7=非常同意)", scale_7, horizontal=True, index=None, key="bg2")
        data_breach_experience = st.radio(
            "您是否曾有帳號外洩、詐騙或個資風險相關經驗？",
            ["有", "沒有", "不確定"],
            index=None
        )

        submit = st.form_submit_button("提交問卷")

        if submit:
            all_required_fields = [
                attention_check, signal_source_check, 
                q_sc_1, q_sc_2, q_sc_3, q_pr_1, q_pr_2, q_pr_3,
                q_bt_1, q_bt_2, q_bt_3, q_pi_1, q_pi_2, q_pi_3,
                privacy_concern, digital_familiarity, data_breach_experience
            ] + list(mpl_answers.values())
            
            if None in all_required_fields:
                st.error("⚠️ 提交失敗：請確認「所有題目」皆已點選作答（包含價格評估與背景變數）。")
            else:
                signal_credibility_avg = round((q_sc_1 + q_sc_2 + q_sc_3) / 3, 3)
                privacy_risk_avg = round((q_pr_1 + q_pr_2 + q_pr_3) / 3, 3)
                brand_trust_avg = round((q_bt_1 + q_bt_2 + q_bt_3) / 3, 3)
                purchase_intention_avg = round((q_pi_1 + q_pi_2 + q_pi_3) / 3, 3)

                highest_accepted_premium = infer_wtp_switch(mpl_answers)

                sorted_keys = sorted(mpl_answers.keys())
                numeric_pattern = [1 if mpl_answers[k] == "會" else 0 for k in sorted_keys]
                non_monotonic = False
                seen_zero = False
                for v in numeric_pattern:
                    if v == 0:
                        seen_zero = True
                    if seen_zero and v == 1:
                        non_monotonic = True
                        break

                record = {
                    "participant_id": st.session_state["participant_id"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "signal_type": signal_type,
                    "privacy_context": st.session_state["privacy_context"],
                    "product_name": info["product_name"],
                    "base_price": base_price,
                    "opened_signal_doc": st.session_state["opened_signal_doc"],
                    "product_page_time_sec": st.session_state.get("product_time_sec", 0),
                    "survey_page_time_sec": page_time_sec,
                    "attention_check_product": attention_check,
                    "signal_source_check": signal_source_check,
                    "q_sc_1": q_sc_1, "q_sc_2": q_sc_2, "q_sc_3": q_sc_3,
                    "signal_credibility_avg": signal_credibility_avg,
                    "q_pr_1": q_pr_1, "q_pr_2": q_pr_2, "q_pr_3": q_pr_3,
                    "privacy_risk_avg": privacy_risk_avg,
                    "q_bt_1": q_bt_1, "q_bt_2": q_bt_2, "q_bt_3": q_bt_3,
                    "brand_trust_avg": brand_trust_avg,
                    "q_pi_1": q_pi_1, "q_pi_2": q_pi_2, "q_pi_3": q_pi_3,
                    "purchase_intention_avg": purchase_intention_avg,
                    "mpl_0": mpl_answers[0], "mpl_5": mpl_answers[5], "mpl_10": mpl_answers[10],
                    "mpl_15": mpl_answers[15], "mpl_20": mpl_answers[20], "mpl_25": mpl_answers[25], "mpl_30": mpl_answers[30],
                    "highest_accepted_premium_pct": highest_accepted_premium,
                    "mpl_non_monotonic": non_monotonic,
                    "privacy_concern": privacy_concern,
                    "digital_familiarity": digital_familiarity,
                    "data_breach_experience": data_breach_experience
                }

                save_to_csv(record)
                st.session_state["submitted"] = True
                set_step("thanks")

def render_thanks():
    st.markdown("## 步驟 4/4：完成")
    st.success("✅ 您已完成本研究，感謝您的參與。")
    st.balloons()
    st.write(f"受試者編號：**{st.session_state['participant_id']}**")
    if st.button("下一位受試者"):
        reset_for_next_participant()

def render_sidebar_admin():
    st.sidebar.markdown("---")
    st.sidebar.header("🔧 管理員專區")

    if ADMIN_PASSWORD:
        admin_input = st.sidebar.text_input("輸入管理密碼", type="password")
        if admin_input == ADMIN_PASSWORD:
            if os.path.exists(CSV_FILE):
                df = pd.read_csv(CSV_FILE)
                st.sidebar.success(f"目前已收集 {len(df)} 筆資料")
                csv_data = df.to_csv(index=False).encode("utf-8-sig")
                st.sidebar.download_button(
                    label="📥 下載資料 CSV",
                    data=csv_data,
                    file_name="experiment_data_v2.csv",
                    mime="text/csv"
                )
            else:
                st.sidebar.warning("目前尚無資料。")
    else:
        st.sidebar.caption("未設定 ADMIN_PASSWORD 環境變數，管理下載功能已停用。")

# =========================
# 4. 主流程
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
elif step == "survey":
    render_survey()
elif step == "thanks":
    render_thanks()
