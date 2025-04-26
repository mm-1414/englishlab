import streamlit as st
import openai

# OpenAI APIキーはSecretsから取得する
openai.api_key = st.secrets["openai_api_key"]

def grade_essay_with_cefr_and_model(prompt, user_essay):
    system_message = """
あなたは英語の採点官です。
以下の英作文について、次の4点を日本語で出力してください。

1. CEFRレベル(A1〜C2)を判定してください。
2. TOEFLのライティング基準に基づいて10点満点で採点してください。
3. 文法や内容のどこが良くなかったかを「です・ます調」でやさしく解説してください。
4. 100語程度の模範解答(Model Answer)を提示してください。
   模範解答は生徒が参考にできるよう、語彙・文法ともに中〜上級レベルで丁寧に書いてください。

出力フォーマット:
CEFRレベル: A1〜C2のいずれか
TOEFLスコア: 0〜10の整数
解説: 
アドバイス: 
模範解答: 
"""

    user_input = f"【お題】{prompt}\n【生徒のエッセイ】{user_essay}"

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )

    return response['choices'][0]['message']['content']

# Streamlitアプリ本体
def main():
    st.title("自由英作文 採点アプリ(TOEFL + CEFR + 模範解答付き)")

    prompt = st.text_input("【お題】を入力してください")
    essay = st.text_area("【生徒のエッセイ】を150語程度で入力してください", height=300)

    if st.button("採点する"):
        if prompt and essay:
            with st.spinner("採点中です..."):
                result = grade_essay_with_cefr_and_model(prompt, essay)
            st.success("採点完了!")
            st.write("### 【採点結果】")
            st.write(result)
        else:
            st.warning("お題とエッセイの両方を入力してください。")

if __name__ == "__main__":
    main()
