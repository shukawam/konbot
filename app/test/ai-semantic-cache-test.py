import os, logging
from openai import OpenAI

logger = logging.getLogger(__name__)

GATEWAY_ENDPOINT = os.getenv("GATEWAY_ENDPOINT", "http://localhost:8000")

client = OpenAI(
    # Kong GatewayでAPIキーを差し込むためここでは、ダミーの値でOK
    api_key="use-kong-gateway-settings",
    base_url=f"{GATEWAY_ENDPOINT}/chat",
)


def exec(msg: str = None, max_tokens: int = 1024, temperature: float = 0.7):
    client = OpenAI(
        api_key="use-kong-gateway-settings", base_url=f"{GATEWAY_ENDPOINT}/chat"
    )
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": msg}],
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
    )
    for chunk in stream:
        print(chunk.choices[0].delta.content, end="", flush=True)


if __name__ == "__main__":
    query1 = "モダンなテクノロジーについて教えてください"
    print(f"{query1=}")
    exec(query1)
    print("\n")
    query2 = "最新の技術についてわかりやすく教えて"
    print(f"{query2=}")
    exec(query2)
