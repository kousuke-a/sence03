import streamlit as st
from streamlit_gsheets import GSheetsConnection
import urllib.parse

st.title("Debug Mode - Encoding Fix")

# 1. スプレッドシートのURLをここに貼る（末尾は /edit まででOK）
raw_url = "https://docs.google.com/spreadsheets/d/あなたのスプレッドシートID/edit"

# 日本語が含まれていても大丈夫なように変換
public_gsheet_url = urllib.parse.quote(raw_url, safe=':/?&=#')

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 2. worksheet名がスプレッドシートのタブ名と「完全一致」しているか確認！
    df = conn.read(spreadsheet=public_gsheet_url, worksheet="customers")
    st.write("✅ 接続成功！")
    st.dataframe(df)
except Exception as e:
    st.error("❌ エラーが発生しました")
    st.write(f"現在のエラー内容: {e}")
