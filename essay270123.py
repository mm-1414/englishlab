from openai import OpenAI
import streamlit as st
import pandas as pd
from datetime import datetime

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ログファイル名
LOG_FILE = "user_log.csv"

# 名前入力
st.title("英作文 採点アプリ")
name = st.text_input("あなたの名前を入力してください")

if name:
    prompt = st.text_area("お題(過去問などどんな問題でも入力可能です。例:Do the benefits of online shopping outweigh the disadvantages?)")
    user_essay = st.text_area("あなたの英作文を入力してください。問題に合わせて何文字でも入力可能です。")

    if st.button("採点する"):
        if prompt and user_essay:
            with st.spinner("採点中..."):
                # 採点プロンプト
                system_message = """
あなたは英語の採点官です。
以下の英作文について、次の4点を日本語で出力してください。

1. CEFRレベル(A1〜C2)を判定してください。
2. TOEFLのライティング基準に基づいて10点満点で採点してください。
3. 文法・語法・単語・表現・内容に間違いや不適切な点があれば、すべて指摘してください。
   【ミス箇所】→【どのように間違っているか】→【なぜ間違いか(ルールや理由)】→【正しい例】
   小さなミス(冠詞、単数複数、語順など)も、すべて漏れなく指摘してください。
4. 100語程度の模範解答を英語で示してください。

※解説はすべて「です・ます調」で優しく書いてください。
※間違いが見つからない場合でも「間違いは見つかりませんでした」と必ず書いてください。
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
                st.text_area("添削結果", result, height=500)

                # ログ保存
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_data = pd.DataFrame([[timestamp, name]], columns=["日時", "名前"])
                log_data.to_csv(LOG_FILE, mode='a', header=not pd.io.common.file_exists(LOG_FILE), index=False)
        else:
            st.warning("お題と英作文の両方を入力してください。")
else:
    st.warning("最初に名前を入力してください。")
