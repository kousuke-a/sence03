import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- ページ設定 ---
st.set_page_config(page_title="SALES ARENA", layout="wide")
st.title("⚡ SALES ARENA")

# --- 定数設定 ---
ACTIONS = {
    "📞 架電": 1,
    "📅 アポ": 10,
    "🚪 訪問": 3,
    "🏆 受注": 50
}

# --- Google Sheets 接続 ---
conn = st.connection("gsheets", type=GSheetsConnection)

# データの読み込み
df_customers = conn.read(worksheet="customers")
df_logs = conn.read(worksheet="logs")

tab1, tab2, tab3 = st.tabs(["🏆 ランキング", "👥 顧客管理", "➕ 顧客追加"])

with tab1:
    st.subheader("リアルタイム・リーダーボード")
    if not df_logs.empty:
        # メンバーごとの合計ポイントを計算
        ranking = df_logs.groupby("member_name")["points"].sum().sort_values(ascending=False).reset_index()
        for i, row in ranking.iterrows():
            st.metric(label=f"{i+1}位: {row['member_name']}", value=f"{row['points']} pt")
    else:
        st.write("まだ記録がありません。")

with tab2:
    st.subheader("顧客リスト & アクション記録")
    # 自分の名前を選択（ログイン代わり）
    me = st.selectbox("あなたの名前を選択", ["田中 蓮", "佐藤 陽菜", "山本 颯太", "鈴木 結衣"])
    
    for index, row in df_customers.iterrows():
        with st.expander(f"{row['name']} ({row['company']})"):
            cols = st.columns(len(ACTIONS))
            for i, (action_label, pts) in enumerate(ACTIONS.items()):
                if cols[i].button(action_label, key=f"{index}_{action_label}"):
                    # ログ追加
                    new_log = pd.DataFrame([{
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "member_name": me,
                        "action_type": action_label,
                        "points": pts
                    }])
                    df_logs = pd.concat([df_logs, new_log], ignore_index=True)
                    conn.update(worksheet="logs", data=df_logs)
                    st.success(f"{action_label}を記録しました！(+{pts}pt)")
                    st.rerun()

with tab3:
    st.subheader("新規顧客の登録")
    with st.form("add_client"):
        new_name = st.text_input("顧客名")
        new_comp = st.text_input("会社名")
        if st.form_submit_button("登録"):
            new_cust = pd.DataFrame([{
                "id": len(df_customers) + 1,
                "name": new_name,
                "company": new_comp,
                "status": "未接触",
                "assignee": ""
            }])
            df_customers = pd.concat([df_customers, new_cust], ignore_index=True)
            conn.update(worksheet="customers", data=df_customers)
            st.success("顧客を登録しました！")
            st.rerun()