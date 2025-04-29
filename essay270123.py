from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ログファイル名
LOG_FILE = "user_log.csv"

st.title("英作文 採点アプリ")

# 名前入力
name = st.text_input("あなたの名前を入力してください(必須)")

if not name:
    st.warning("名前を入力してください。")
else:
    # セッションステートの初期化(最初だけ)
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""
    if "user_essay" not in st.session_state:
        st.session_state.user_essay = ""

    # 問題文の入力とクリアボタン
    st.subheader("問題文の入力")
    st.session_state.prompt = st.text_area(
        "お題を入力してください(例: Do the benefits of online shopping outweigh the disadvantages?)",
        value=st.session_state.prompt,
        key="prompt"
    )

    if st.button("問題文をクリアする"):
        st.session_state.prompt = ""

    # 英作文の入力とクリアボタン
    st.subheader("あなたの英作文")
    st.session_state.user_essay = st.text_area(
        "あなたの英作文を入力してください。文字数は自由です。",
        value=st.session_state.user_essay,
        key="user_essay"
    )

    if st.button("あなたの英作文をクリアする"):
        st.session_state.user_essay = ""

    # 採点ボタン
    if st.button("採点を開始する"):
        if st.session_state.prompt and st.session_state.user_essay:
            with st.spinner("採点中です。お待ちください。"):
                system_message = """
あなたは英語の採点官である。
以下の英作文について、次の手順に厳密に従い、日本語で出力せよ。

1. CEFRレベル(A1〜C2)を判定せよ。
2. TOEFLのライティング基準に基づき、10点満点で採点せよ。
3. 文法・語法・単語・表現の誤りを、すべて漏れなく以下の順番でまとめよ。
   【誤りのある元の文(英語)】
   【訂正文(英語)】
   【なぜ間違いなのか(英文法、語法、意味、文脈の観点から、やさしい日本語で、丁寧なである調で具体的に説明せよ)】
- TOEFLの採点基準に照らして減点対象となる誤りのみ指摘すること。
- 減点対象外の表現の違いは「参考アドバイス」としてまとめること。

4. 接続詞や接続副詞の適切性を判定し、必要なら改善案を提示せよ。
5. 英文全体の論理展開が自然か評価し、必要に応じてアドバイスを加えよ。
6. 模範解答を140〜160語以内で英語で作成せよ。

※説明はすべて日本語の「丁寧なである調」で行う。
"""

                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": f"{st.session_state.prompt}\n\n{st.session_state.user_essay}"}
                    ]
                )
                result = response.choices[0].message.content

            # 採点完了後の表示
            st.success("採点が完了しました。")

            st.subheader("あなたの解答")
            st.text_area("あなたの英文", value=st.session_state.user_essay, height=150, disabled=True)

            st.subheader("問題(お題)")
            st.text_area("問題文", value=st.session_state.prompt, height=150, disabled=True)

            st.subheader("添削結果")
            st.text_area("添削結果", value=result, height=750, disabled=True)

            # ダウンロードするか選択
            save_choice = st.radio(
                "添削結果をダウンロードしますか?(「いいえ」を選ぶとデータは消えます)",
                ("はい", "いいえ")
            )

            if save_choice == "はい":
                download_text = f"""【名前】
{name}

【お題】
{st.session_state.prompt}

【あなたの解答】
{st.session_state.user_essay}

【添削結果】
{result}
"""

                st.download_button(
                    label="添削結果をダウンロードする",
                    data=download_text,
                    file_name=f"{name}_writing_result.txt",
                    mime="text/plain"
                )
            else:
                st.warning("このまま画面を閉じると、データは消えてしまいます。")

            # ダウンロードの有無に関わらず案内
            st.info("別の問題を解きたい場合は、この画面を更新してください。(画面を下に引っ張る、またはぐるっとした矢印ボタンを押してください)")

            # ログ保存(名前だけ)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_data = pd.DataFrame([[timestamp, name]], columns=["日時", "名前"])
            log_data.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)

        else:
            st.warning("お題と英作文の両方を入力してください。")
