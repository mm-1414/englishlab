from openai import OpenAI
import streamlit as st

# APIキーの入力
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def grade_essay_with_cefr_and_model(prompt, user_essay):
    system_message = """
あなたは英語の採点官です。
以下の英作文について、次の4点を日本語で出力してください。

1. CEFRレベル(A1〜C2)を判定してください。
2. TOEFLのライティング基準に基づいて10点満点で採点してください。
3. 文法や内容のどこが良くなかったかを「です・ます調」でやさしく解説してください。
4. 100語程度の模範解答を英語で示してください。
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"{prompt}\n\n{user_essay}"}
        ]
    )

    return response.choices[0].message.content

# Streamlit UI
st.title("英作文 採点アプリ")

prompt = st.text_area("お題(例:Do the benefits of online shopping outweigh the disadvantages?)")
user_essay = st.text_area("あなたの英作文を入力してください")

if st.button("採点する"):
    if prompt and user_essay:
        with st.spinner("採点中..."):
            result = grade_essay_with_cefr_and_model(prompt, user_essay)
            st.success("採点が完了しました!")
            st.write(result)
    else:
        st.warning("お題と英作文の両方を入力してください。")
