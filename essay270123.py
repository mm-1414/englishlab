from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ログファイル名
LOG_FILE = "user_log.csv"

# 名前入力
st.title("英作文 採点アプリ")
name = st.text_input("あなたの名前を入力してください")

if name:
    prompt = st.text_area("お題(過去問などどんな問題でも入力可能です。例:Do the benefits of online shopping outweigh the disadvantages?)")
    user_essay = st.text_area("あなたの英作文を入力してください。問題に合わせて何文字でも入力可能です。")

    if st.button("採点する"):
        if prompt and user_essay:
            with st.spinner("採点中..."):
                # 採点プロンプト(超自然版)
                system_message = """
あなたは英語の採点官です。
以下の英作文について、次の5点を出力してください。

1. CEFRレベル(A1〜C2)を判定してください。
2. TOEFLのライティング基準に基づいて10点満点で採点してください。
3. 文法・語法・単語・表現に間違いや不適切な点があれば、ミス1つごとに次の順番で詳しく書いてください。
   【元の文のミス箇所(英語)】→【訂正文(英語)】→【なぜ間違いなのか(日本語で説明。ただし必要に応じて単語や例文レベルでは英語を自然に使ってよい)】
   この順番で、ミス1つごとにまとめて説明してください。
   小さなミス(冠詞、単数複数、時制、語順)も必ず拾ってください。
4. First, Second, In conclusionなどの論理的接続表現が適切に使われているかを必ずチェックしてください。
   接続表現が不足している場合は「接続表現が不足しています」と日本語で明記し、どこにどの接続詞を使えばよいか具体例も示してください。
5. 100語程度の模範解答を英語で示してください。

※説明は日本語(です・ます調)で書いてください。ただし単語や例文レベルでは自然に英語を使ってもよいです。
※訂正文と模範解答は英語で書いてください。
※間違いが見つからない場合でも「間違いは見つかりませんでした」と必ず日本語で書いてください。
※内容が十分に良い場合も「内容は十分に良いです」と日本語で書いてください。
"""

                # 採点処理
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": f"{prompt}\n\n{user_essay}"}
                    ]
                )
                result = response.choices[0].message.content

                st.success("採点が完了しました!")
                st.text_area("添削結果", result, height=600)

                # ログ保存
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_data = pd.DataFrame([[timestamp, name]], columns=["日時", "名前"])
                log_data.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)
        else:
            st.warning("お題と英作文の両方を入力してください。")
else:
    st.warning("最初に名前を入力してください。")
