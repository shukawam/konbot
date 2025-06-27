import streamlit as st
from openai import OpenAI

with st.sidebar.container():
    with st.sidebar:
        model_name = st.sidebar.selectbox(
            label="Model Name",
            options=["gpt-4o-mini", "o4-mini", "gpt-4.1"],
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

client = OpenAI(
    api_key="use-kong-gateway-settings", base_url="http://localhost:8000/chat"
)

st.title("Kong Bot 🦍")
st.caption(
    """
    OpenAI と Kong Gateway を用いた Chatbot アプリケーションです。
    Kong に関する何かを聞くとゴリラっぽく答えてくれます。
    """
)
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("どうしましたか？"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
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
            full_response = "ウホッ！エラーが発生したゴリ..."
            message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
