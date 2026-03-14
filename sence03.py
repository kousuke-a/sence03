import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Debug Mode")

# Secretsを使わず、直接URLを指定（ここにスプレッドシートのURLを貼る）
public_gsheet_url = "https://docs.google.com/spreadsheets/d/あなたのスプレッドシートID/edit"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 試しに読み込む
    df = conn.read(spreadsheet=public_gsheet_url, worksheet="customers")
    st.write("✅ 接続成功！データの中身：")
    st.dataframe(df)
except Exception as e:
    st.error("❌ まだエラーが出ます")
    st.exception(e)
