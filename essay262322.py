from openai import OpenAI
import streamlit as st

# APIキーの設定
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def grade_essay_with_cefr_and_model(prompt, user_essay):
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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"{prompt}\n\n{user_essay}"}
        ]
    )

    return response.choices[0].message.content

# Streamlit画面の設計
st.title("英作文 採点アプリ")

prompt = st.text_area("お題(例:Do the benefits of online shopping outweigh the disadvantages?)")
user_essay = st.text_area("あなたの英作文を入力してください")

if st.button("採点する"):
    if prompt and user_essay:
        with st.spinner("採点中..."):
            result = grade_essay_with_cefr_and_model(prompt, user_essay)
            st.success("採点が完了しました！")
            st.text_area("添削結果", result, height=500)
    else:
        st.warning("お題と英作文の両方を入力してください。")
