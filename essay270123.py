from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ログファイル名
LOG_FILE = "user_log.csv"

# Streamlit画面側は「です・ます調」で親しみやすく
st.title("英作文 採点アプリ")
name = st.text_input("あなたの名前を入力してください")

if name:
    prompt = st.text_area("お題を入力してください(例:Do the benefits of online shopping outweigh the disadvantages?)")
    user_essay = st.text_area("あなたの英作文を入力してください。文字数は自由です。")

    if st.button("採点を開始する"):
        if prompt and user_essay:
            with st.spinner("採点中です。お待ちください。"):
                # 最終改訂版プロンプト(完璧指示入り)
                system_message = """
あなたは英語の採点官である。
以下の英作文について、次の手順に厳密に従い、日本語で出力せよ。

1. CEFRレベル(A1〜C2)を判定せよ。
2. TOEFLのライティング基準に基づき、10点満点で採点せよ。
3. 文法・語法・単語・表現の誤りを、すべて1つずつ以下の順番でまとめよ。
   【誤りのある元の文(英語)】
   【訂正文(英語)】
   【なぜ間違いなのか(小学生でも理解できるやさしい日本語、丁寧なである調で説明せよ)】
   【なぜ訂正が必要なのか(誤解を招く、不自然になる、英語では使わない等を具体的に説明せよ)】
   【訂正するとどう良くなるのか(自然さ、明確さ、論理展開の向上について具体的に述べよ)】

4. ミスが1つでもあれば、すべて個別に記述せよ。まとめたり重複させたりしてはならない。

5. 接続詞や接続副詞について:
   - 使用が適切かを判定せよ。
   - 不適切であれば、どこがどう間違いか、なぜ直す必要があるか、どう直すと良くなるか、を具体的に説明せよ。
   - 使用が不足している場合は、どこにどの接続詞を追加すべきかを提案せよ。
   - AlsoとMoreover、solveとresolveなど、類似表現については意味・使い方・論理展開上の違いをやさしい日本語で詳しく説明せよ。

6. 英文全体の論理展開(Introduction → Body → Conclusion)が自然かどうかを評価し、必要に応じて改善案を示せ。

7. 減点対象かどうかを必ず判定し、減点対象なら「訂正」、減点対象外なら「参考アドバイス」と明記せよ。

8. 模範解答を140〜160語以内で英語で作成せよ。

9. 模範解答において修正した内容についても、【元文】→【訂正文】→【理由(なぜ直したのか)】→【直してどう良くなったか】の順で、すべて振り返り記述せよ。

※すべての説明文は日本語の「丁寧なである調」で書くこと。
※です・ます調は禁止する。
※誤りがない場合も「誤りは見つからなかった」と必ず記載すること。
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
                st.text_area("添削結果", result, height=750)

                # ログ保存
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_data = pd.DataFrame([[timestamp, name]], columns=["日時", "名前"])
                log_data.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)
        else:
            st.warning("お題と英作文の両方を入力してください。")
else:
    st.warning("最初にあなたの名前を入力してください。")
