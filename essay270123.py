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
                # ここが新しいプロンプト
                system_message = """
あなたは英語の採点官である。
以下の英作文について、次の7点を日本語で出力せよ。

1. CEFRレベル(A1〜C2)を判定せよ。
2. TOEFLのライティング基準に基づき、10点満点で採点せよ。
3. 文法・語法・単語・表現に明確な誤りがある場合、以下の順番で1つずつ丁寧に記述せよ。
   【誤りのある元の文(英語)】→【訂正文(英語)】→【誤りの理由(日本語で丁寧なである調で記述。ただし単語・例文レベルでは自然に英語を使用してよい)】
   - なぜその表現が間違いなのか。
   - どのようなニュアンスや意味の違いがあるか。
   - 英検やTOEFLにおいて減点対象になる理由を説明せよ。
   - 単なる表現の好みレベルの違い(減点対象外)の場合は、「参考」としてアドバイスのみ記載し、訂正はしないこと。
4. 文脈に適した接続詞または接続副詞(First, Second, Therefore, In addition, However, In conclusionなど)が使用されているか判定せよ。
   - 位置や選択が適切でない場合、「接続詞・接続副詞の使用位置が不適切である」と明記し、どこをどのように訂正すべきか具体的に示せ。
   - 接続詞の違い(e.g., AlsoとMoreover)についても意味・強さ・使用場面の違いを説明せよ。
5. 接続詞や接続副詞が不足している場合、適切な追加提案を行うこと。
6. 英文全体の論理展開(Introduction → Body → Conclusion)が適切かを評価し、必要に応じて改善案を示せ。
7. 100語程度の模範解答を英語で作成せよ。

※すべての説明は日本語の「丁寧なである調」で記述すること。
※訂正文および模範解答は英語で記載すること。
※誤りが見つからない場合でも「誤りは見つからなかった」と必ず明記すること。
※内容が十分に良い場合も「内容は十分に良い」と明記すること。
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
