from langchain_community.document_loaders import TextLoader
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_openai.embeddings.base import OpenAIEmbeddings

REDIS_URL = "redis://localhost:6379"
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


def main():
    config = RedisConfig(
        index_name="kongdocs",
        redis_url=REDIS_URL,
    )
    vs = RedisVectorStore(embeddings, config)
    result = vs.similarity_search("Kong AI Gatewayはなに？", k=2)
    for doc in result:
        print(f"Content: {doc.page_content[:100]}...")


if __name__ == "__main__":
    main()
