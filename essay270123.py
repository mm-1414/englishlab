from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ログファイル名
LOG_FILE = "user_log.csv"

# Streamlit側の画面は「です・ます調」でOK
st.title("英作文 採点アプリ")
name = st.text_input("あなたの名前を入力してください")

if name:
    prompt = st.text_area("お題を入力してください(例:Do the benefits of online shopping outweigh the disadvantages?)")
    user_essay = st.text_area("あなたの英作文を入力してください。文字数は自由です。")

    if st.button("採点を開始する"):
        if prompt and user_essay:
            with st.spinner("採点中です。お待ちください。"):
                # 決定版プロンプト
                system_message = """
あなたは英語の採点官である。
以下の英作文について、次の手順に厳密に従い、日本語で出力せよ。

1. CEFRレベル(A1〜C2)を判定せよ。
2. TOEFLのライティング基準に基づき、10点満点で採点せよ。
3. 文法・語法・単語・表現の誤りを、すべて漏れなく以下の順番でまとめよ。
   【誤りのある元の文(英語)】
   【訂正文(英語)】
   【なぜ間違いなのか(英文法、語法、意味、文脈の観点から、やさしい日本語で、丁寧なである調で具体的に説明せよ)】

- すべての誤りについて、必ず【訂正文】と【なぜ間違いか】のセットを付けること。
- 1つでも省略やまとめ書きをしてはならない。
- 小さなミス(冠詞、単数・複数、語順など)もすべて指摘し、必ず理由を書くこと。

4. 接続詞や接続副詞について:
   - 使用が適切かを判定せよ。
   - 不適切な場合は、どこがどう間違いか、なぜ直す必要があるかを具体的に説明せよ。
   - 類似表現(alsoとmoreover、solveとresolveなど)についても、意味・使い方・ニュアンスの違いをわかりやすく説明せよ。

5. 英文全体の論理展開(Introduction → Body → Conclusion)が自然かどうかを評価し、必要に応じて改善案を示せ。

6. 減点対象かどうかを判定し、減点対象なら「訂正」、減点対象外なら「参考アドバイス」と明記せよ。

7. 模範解答を140〜160語以内で英語で作成せよ。

8. 模範解答における修正についても、【元文】→【訂正文】→【なぜ間違いか】をすべて振り返り記述せよ。

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
