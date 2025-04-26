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
                # 採点プロンプト
                system_message = """
あなたは英語の採点官です。
以下の英作文について、次の7点を日本語で出力してください。

1. CEFRレベル(A1〜C2)を判定してください。
2. TOEFLのライティング基準に基づいて10点満点で採点してください。
3. 文法・語法・単語・表現に間違いや不適切な点があれば、すべて指摘してください。
   【ミス箇所】→【どのように間違っているか】→【なぜ間違いか(ルールや理由)】→【正しい例】を必ず示してください。
4. 内容の展開やアイデアに不十分な点、また設問に十分に答えていない場合は、どのように改善すればよいかをやさしくアドバイスしてください。
5. First, Second, Finally, In conclusionなどの論理展開の接続表現が適切に使われているかをチェックしてください。
   不足している場合は、どこで使うべきかを指摘し、具体例も示してください。
6. 指示された語数(例:100語程度)に対して語数が不足または超過している場合は指摘し、適切な長さにする方法もアドバイスしてください。
7. 100語程度の模範解答を英語で示してください。

※すべての説明は日本語(です・ます調)でやさしく書いてください。
※間違いが見つからない場合でも「間違いは見つかりませんでした」と必ず書いてください。
※内容が十分に良い場合は「内容は十分に良いです」と必ず書いてください。
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
