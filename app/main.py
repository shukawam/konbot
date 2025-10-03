import os
import streamlit as st
from openai import OpenAI

plans = {
    "free": {
        "apikey": os.getenv("FREE_API_KEY", "free-key"),
        "model_name": "command-a-03-2025",
    },
    "paid": {
        "apikey": os.getenv("PAID_API_KEY", "paid-key"),
        "model_name": "gpt-4o-mini",
    },
}



def update_model_name() -> None:
    """プランに応じて利用モデルを変更するイベントハンドラ"""
    selected_plan = st.session_state.plan_key
    st.session_state.model_name = plans[selected_plan]["model_name"]


with st.sidebar.container():
    with st.sidebar:
        plan = st.sidebar.selectbox(
            label="Plan",
            options=["free", "paid"],
            key="plan_key",
            on_change=update_model_name,
            help="使用するプラン(使用するモデルとレート制限が異なります。free: 100tpm, paid: 4,000tpm)",
        )

        if "model_name" not in st.session_state:
            st.session_state.model_name = plans[plan]["model_name"]
        model_options = ["gpt-4o-mini", "command-a-03-2025"]
        default_index = model_options.index(st.session_state.model_name)

        model_name = st.sidebar.selectbox(
            label="Model Name",
            index=default_index,
            disabled=True,
            options=["gpt-4o-mini", "command-a-03-2025"],
            help="使用するモデルの名前（実際には、Kong Gatewayにて統一的なポリシーが設定されているため、設定が反映されることはありません。）",
        )
        max_tokens = st.sidebar.slider(
            label="Max Tokens",
            min_value=128,
            max_value=2048,
            value=1024,
            step=128,
            help="LLMが出力する最大のトークン長（実際には、Kong Gatewayにて統一的なポリシーが設定されているため、設定が反映されることはありません。）",
        )
        temperature = st.sidebar.slider(
            label="Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="モデルの出力のランダム性（実際には、Kong Gatewayにて統一的なポリシーが設定されているため、設定が反映されることはありません。）",
        )

st.title("Kong Bot 🦍")
st.caption(
    """
    OpenAI と Kong Gateway を用いた Chatbot アプリケーションです。
    Kong に関する何かを聞くとゴリラっぽく答えてくれます。
    """
)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("どうしましたか 🦍？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            if model_name == "gpt-4o-mini":
                provider = "openai"
            if model_name == "command-a-03-2025":
                provider = "cohere"
            GATEWAY_ENDPOINT = os.getenv("GATEWAY_ENDPOINT", f"http://localhost:8000")
            base_url = f"{GATEWAY_ENDPOINT}/{provider}/{model_name}"
            print(f"{GATEWAY_ENDPOINT=}")
            print(f"{base_url=}")
            if plan == "free":
                apikey = plans["free"]["apikey"]
            if plan == "paid":
                apikey = plans["paid"]["apikey"]
            print(f"{apikey=}")
            client = OpenAI(
                # Kong GatewayでAPIキーを差し込むためここでは、ダミーの値でOK
                api_key="use-kong-gateway-settings",
                base_url=base_url,
                default_headers={
                    "apikey": apikey,
                },
            )
            stream = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
            )
            for chunk in stream:
                full_response += chunk.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = f"ウホッ！エラーが発生したゴリ..."
            message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
