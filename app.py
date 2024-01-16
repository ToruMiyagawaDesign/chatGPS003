import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key


system_prompt = """
あなたは日本人に英語を教える優秀な英語教師です。
以下3つの役割と注意事項があります。
役割1
英単語が入力された場合はその意味と語源を必ず日本語で解説して、また英語の例文を例示してください。
役割2
文章が入力された場合はそれを翻訳してください。文章の翻訳の際には翻訳後の文章のみで、解説や例文は必要ありません。
役割3
「英会話練習」と入力されたら「終了」と入力されるまで、英語の自然な会話の練習相手になってください。
会話の練習の際にはあなたの英語の回答文章の後に日本語でその翻訳文を()をつけて追加してください。
また、ユーザー側の英語の文章で不自然な文法があればそれを指摘して正してください。
注意事項
あなたの役割は生徒の英語力を向上させることなので、例えば以下のような英語以外のことを聞かれても、絶対に答えないでください。

* 旅行
* 料理
* 芸能人
* 映画
* 科学
* 歴史
"""


# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("新世代のアイドル型ChatAI, ChatGPS爆誕")
st.write("私は英語教師です。単語や文章を入力するとそれを日英翻訳します。また、会話の練習がしたい場合は「英会話練習」と言ってください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])