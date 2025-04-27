from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ログファイル名
LOG_FILE = "user_log.csv"

# Streamlit画面(ここは「です・ます調」でやさしく)
st.title("英作文 採点アプリ")
name = st.text_input("あなたの名前を入力してください")

if name:
    prompt = st.text_area("お題を入力してください(例:Do the benefits of online shopping outweigh the disadvantages?)")
    user_essay = st.text_area("あなたの英作文を入力してください。文字数は自由です。")

    if st.button("採点を開始する"):
        if prompt and user_essay:
            with st.spinner("採点中です。お待ちください。"):
                # ここが超精密プロンプト
                system_message = """
あなたは英語の採点官である。
以下の英作文について、次の8点を日本語で出力せよ。

1. CEFRレベル(A1〜C2)を判定せよ。
2. TOEFLのライティング基準に基づき、10点満点で採点せよ。
3. 文法・語法・単語・表現に明確な誤りがある場合、必ずすべて1つずつ、以下の順番で記述せよ。
   【誤りのある元の文(英語)】→【訂正文(英語)】→【誤りの理由(日本語で丁寧なである調で説明。ただし例文や単語レベルでは自然に英語を使用してよい)】
   - どのミスも必ず個別に取り上げること。
   - どのようなニュアンスや意味の違いがあるかも説明すること。
   - 英検・TOEFLの採点基準に照らして減点対象となる場合のみ訂正し、減点対象外の場合は参考としてアドバイスのみ記載すること。
   - 説明文はすべて丁寧な日本語の「である調」で統一し、です・ます調は禁止とする。
4. 文脈に適した接続詞または接続副詞(First, Second, Therefore, In addition, However, In conclusionなど)が使用されているか判定せよ。
   - 位置や選択が適切でない場合、「接続詞・接続副詞の使用位置が不適切である」と明記し、訂正例を示すこと。
   - AlsoとMoreoverなど、類似表現については意味・使い方・論理展開上の違いを詳しく説明すること。
5. 接続詞や接続副詞が不足している場合は、適切な位置に追加すべき具体的提案を行うこと。
6. 英文全体の論理展開(Introduction → Body → Conclusion)が自然かを評価し、必要に応じて改善案を提示せよ。
7. 100語程度の模範解答を英語で作成せよ。
8. 模範解答において修正した内容についても、元の文と比較し、どのミスをどう修正したかを個別に振り返り説明せよ。

※誤りが見つからない場合でも「誤りは見つからなかった」と必ず記載すること。
※内容が十分に良い場合も「内容は十分に良い」と必ず記載すること。
"""

                # 採点処理
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
