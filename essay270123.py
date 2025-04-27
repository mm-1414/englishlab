from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ログファイル名
LOG_FILE = "user_log.csv"

# Streamlit画面側は「です・ます調」で優しく
st.title("英作文 採点アプリ")
name = st.text_input("あなたの名前を入力してください")

if name:
    prompt = st.text_area("お題を入力してください(例:Do the benefits of online shopping outweigh the disadvantages?)")
    user_essay = st.text_area("あなたの英作文を入力してください。文字数は自由です。")

    if st.button("採点を開始する"):
        if prompt and user_essay:
            with st.spinner("採点中です。お待ちください。"):
                # 超精密版プロンプト
                system_message = """
あなたは英語の採点官である。
以下の英作文について、次の9点を日本語で出力せよ。

1. CEFRレベル(A1〜C2)を判定せよ。
2. TOEFLのライティング基準に基づき、10点満点で採点せよ。
3. 文法・語法・単語・表現に明確な誤りがある場合、必ずすべて1つずつ、以下の順番で記述せよ。
   【誤りのある元の文(英語)】
   【訂正文(英語)】
   【なぜ間違いなのか(具体的な間違いの理由、英語のルールに基づき、丁寧なである調で書く)】
   【なぜ訂正が必要なのか(文脈・文法・意味・論理展開においてどのように不自然・誤解を生むかを説明する)】
   【訂正するとどう良くなるか(英語としての自然さ・明確さ・論理性がどう向上するかを丁寧に述べる)】

4. 文脈に適した接続詞または接続副詞(First, Second, Therefore, In addition, However, In conclusionなど)が使用されているかを判定せよ。
   - 位置や選択が適切でない場合、「接続詞・接続副詞の使用位置が不適切である」と明記し、訂正文と理由を示すこと。
   - AlsoとMoreover、solveとresolveなど類似表現については意味・使い方・論理展開上の違いを具体的に説明すること。

5. 接続詞や接続副詞が不足している場合は、どこに何を追加すべきか提案せよ。

6. 英文全体の論理展開(Introduction → Body → Conclusion)が自然かを評価し、必要に応じて改善案を提示せよ。

7. 減点対象かどうかを判定し、減点対象なら「訂正」、減点対象外なら「参考アドバイス」と明記すること。

8. 100語程度の模範解答を英語で作成せよ。

9. 模範解答において修正した内容についても、どの元文をどう直したか、必ず個別に振り返り、理由・効果まで丁寧に記述せよ。

※すべての説明文は丁寧な日本語の「である調」で統一し、です・ます調は禁止とする。
※誤りが見つからない場合でも「誤りは見つからなかった」と必ず記載すること。
※内容が十分に良い場合も「内容は十分に良い」と必ず記載すること。
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
                st.text_area("添削結果", result, height=700)

                # ログ保存
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_data = pd.DataFrame([[timestamp, name]], columns=["日時", "名前"])
                log_data.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)
        else:
            st.warning("お題と英作文の両方を入力してください。")
else:
    st.warning("最初にあなたの名前を入力してください。")
