import redis
from langchain_community.document_loaders import TextLoader
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_openai.embeddings.base import OpenAIEmbeddings

REDIS_URL = "redis://localhost:6379"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

def main():
    redis_client = redis.from_url(REDIS_URL)
    loader = TextLoader("./docs/kong-rocket.txt")
    docs = loader.load_and_split()  # Use default text splitter
    config = RedisConfig(
        redis_url=REDIS_URL,
    )
    vs = RedisVectorStore(embeddings, config)
    vs.add_documents(docs)


if __name__ == "__main__":
    main()
