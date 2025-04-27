from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ログファイル名
LOG_FILE = "user_log.csv"

# Streamlit画面側は「です・ます調」でOK
st.title("英作文 採点アプリ")
name = st.text_input("あなたの名前を入力してください")

if name:
    prompt = st.text_area("お題を入力してください(例:Do the benefits of online shopping outweigh the disadvantages?)")
    user_essay = st.text_area("あなたの英作文を入力してください。文字数は自由です。")

    if st.button("採点を開始する"):
        if prompt and user_essay:
            with st.spinner("採点中です。お待ちください。"):
                # system_message:AIへの指示(完全である調版+接続詞・論理展開チェック追加)
                system_message = """
あなたは英語の採点官である。
以下の英作文について、次の7点を日本語で出力せよ。

1. CEFRレベル(A1〜C2)を判定せよ。
2. TOEFLのライティング基準に基づき、10点満点で採点せよ。
3. 文法・語法・単語・表現に誤りまたは不適切な点があれば、ミスごとに以下の順番で詳しく記述せよ。
   【誤りのある元の文(英語)】→【訂正文(英語)】→【誤りの理由(日本語で丁寧なである調で記述。ただし例文や単語レベルでは英語を自然に使用してよい)】
   この順番で、ミスごとにまとめて記述すること。
   小さなミス(冠詞、単数・複数、時制、語順)も漏れなく指摘すること。
4. 文脈に適した接続詞または接続副詞(First, Second, Therefore, In addition, However, In conclusionなど)が使用されているかを判定せよ。
   位置や種類が不適切であれば、「接続詞・接続副詞の使用位置が不適切である」と明記し、どのように修正すべきか具体的な訂正文を示すこと。
5. 接続詞や接続副詞が使用されていない場合は、適切な位置に追加する提案を行うこと。
6. 英文全体の論理展開(Introduction → Body → Conclusion)が適切かを評価し、改善案があれば提示すること。
7. 100語程度の模範解答を英語で作成せよ。

※すべての説明は丁寧な日本語の「である調」で記述すること。ただし例文や単語提示には自然に英語を使用してよい。
※訂正文と模範解答は英語で記載すること。
※誤りが見つからない場合でも「誤りは見つからなかった」と必ず明記すること。
※内容が十分に良い場合も「内容は十分に良い」と必ず明記すること。
"""

                # 採点処理(gpt-4-turbo)
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": f"{prompt}\n\n{user_essay}"}
                    ]
                )
                result = response.choices[0].message.content

                st.success("採点が完了しました。")
                st.text_area("添削結果", result, height=600)

                # ログ保存
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_data = pd.DataFrame([[timestamp, name]], columns=["日時", "名前"])
                log_data.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)
        else:
            st.warning("お題と英作文の両方を入力してください。")
else:
    st.warning("最初にあなたの名前を入力してください。")
