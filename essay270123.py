from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ログファイル名
LOG_FILE = "user_log.csv"

# Streamlit画面(ここは「です・ます調」でOK)
st.title("英作文 採点アプリ")
name = st.text_input("あなたの名前を入力してください")

if name:
    prompt = st.text_area("お題を入力してください(例:Do the benefits of online shopping outweigh the disadvantages?)")
    user_essay = st.text_area("あなたの英作文を入力してください。文字数は自由です。")

    if st.button("採点を開始する"):
        if prompt and user_essay:
            with st.spinner("採点中です。お待ちください。"):
                # 超精密プロンプト+150語模範解答版
                system_message = """
あなたは英語の採点官である。
以下の英作文について、次の10点を日本語で出力せよ。

1. CEFRレベル(A1〜C2)を判定せよ。
2. TOEFLのライティング基準に基づき、10点満点で採点せよ。
3. 文法・語法・単語・表現に誤りがある場合、必ずすべて1つずつ、以下の順番でわかりやすく記述せよ。
   【誤りのある元の文(英語)】
   【訂正文(英語)】
   【なぜ間違いなのか(小学生でも理解できるやさしい日本語、である調で)】
   【なぜ訂正が必要なのか(誤解を招く、不自然になる、英語では使わない等)】
   【訂正するとどう良くなるのか(自然さ、明確さ、論理の流れがどう向上するか)】
4. ミスが1つでもあれば、必ず個別にすべて書くこと。省略禁止。
5. 文脈に適した接続詞または接続副詞(First, Second, Therefore, In addition, However, In conclusionなど)が使用されているかを判定せよ。
   - 不適切な箇所があれば、「ここが不適切である」と明記し、なぜ不適切か、どう直すべきか、直すとどう良くなるかを簡単な日本語で詳しく説明すること。
   - AlsoとMoreover、solveとresolveなど、類似表現についても意味・使い方・論理展開上の違いを具体的に説明すること。
6. 接続詞や接続副詞が不足している場合は、どこに何を追加すべきか提案せよ。
7. 英文全体の論理展開(Introduction → Body → Conclusion)が自然かを評価し、必要に応じて改善案を示せ。
8. 減点対象かどうかを判定し、減点対象なら「訂正」、減点対象外なら「参考アドバイス」と明記すること。
9. 約150語(140〜160語)の模範解答を英語で作成せよ。
10. 模範解答において修正した内容についても、必ずどの元文をどう直したか、理由と効果まで小学生でもわかる日本語で振り返り説明すること。

※すべての説明文は日本語の「である調」で統一し、です・ます調は禁止とする。
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
