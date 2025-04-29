from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ログファイル名
LOG_FILE = "user_log.csv"

# 初期化
if "prompt" not in st.session_state:
    st.session_state.prompt = ""
if "user_essay" not in st.session_state:
    st.session_state.user_essay = ""

# Streamlit画面
st.title("英作文 採点アプリ")

# 名前入力(必須)
name = st.text_input("あなたの名前を入力してください")

# 問題入力
st.session_state.prompt = st.text_area("お題を入力してください(例: Do the benefits of online shopping outweigh the disadvantages?)", value=st.session_state.prompt)

# 英作文入力
st.session_state.user_essay = st.text_area("あなたの英作文を入力してください(文字数自由)", value=st.session_state.user_essay)

# 問題文削除ボタン
if st.button("問題をすべて削除する"):
    st.session_state.prompt = ""

# 英作文削除ボタン
if st.button("英作文をすべて削除する"):
    st.session_state.user_essay = ""

# 採点ボタン
if st.button("採点を開始する"):
    if name and st.session_state.prompt and st.session_state.user_essay:
        with st.spinner("採点中です。お待ちください。"):
            system_message = """
あなたは英語の採点官である。
以下の英作文について、次の手順に厳密に従い、日本語で出力せよ。

1. CEFRレベル(A1〜C2)を判定せよ。
2. TOEFLのライティング基準に基づき、10点満点で採点せよ。
3. 文法・語法・単語・表現の誤りをすべて漏れなく以下の順番でまとめよ。
   【誤りのある元の文(英語)】
   【訂正文(英語)】
   【なぜ間違いなのか(英文法、語法、意味、文脈の観点から、やさしい日本語で、丁寧なである調で具体的に説明せよ)】

- 減点対象になるものだけ指摘すること。
- 減点対象にならない細かいニュアンスの違いは指摘しないこと。
- 模範解答を140〜160語以内で英語で作成せよ。

※すべての説明文は日本語の「丁寧なである調」で書くこと。
※です・ます調は禁止する。
"""

            # 採点処理
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"{st.session_state.prompt}\n\n{st.session_state.user_essay}"}
                ]
            )
            result = response.choices[0].message.content

        # 採点完了
        st.success("採点が完了しました!")
        st.text_area("添削結果", result, height=500)

        st.subheader("あなたの解答")
        st.text_area("あなたの英文", value=st.session_state.user_essay, height=150)

        st.subheader("お題と模範解答")
        st.text_area("問題文と模範解答", value=f"【問題】\n{st.session_state.prompt}\n\n【模範解答】\n{result}", height=500)

        # ダウンロードするか確認
        save = st.radio("添削結果をダウンロードしますか?(※いいえの場合、データは消えます)", ("いいえ", "はい"))

        if save == "はい":
            # ダウンロード処理
            full_text = f"【問題】\n{st.session_state.prompt}\n\n【あなたの英作文】\n{st.session_state.user_essay}\n\n【添削結果と模範解答】\n{result}"
            st.download_button("ダウンロードする", full_text, file_name="添削結果.txt")
        else:
            st.info("データは保存されません。")

        st.info("別の問題を解きたい場合は、この画面を更新してください。(画面を下に引っ張る、またはぐるっとした矢印ボタンを押してください)")

    else:
        st.warning("名前、お題、英作文をすべて入力してください。")
else:
    st.info("最初に名前を入力し、問題と英作文を書いてください。")
