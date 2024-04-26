from typing import Optional, List

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, ServiceContext, Settings
from llama_index.core.extractors import QuestionsAnsweredExtractor, SummaryExtractor
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TransformComponent
from llama_index.vector_stores.redis import RedisVectorStore
from redis import Redis
from redisvl.schema import IndexSchema

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI

load_dotenv()


def build_vector_store(index_name: str, dims: int = 1024, overwrite=False) -> RedisVectorStore:
    redis_index_schema = IndexSchema.from_dict(
        {
            # customize basic index specs
            "index": {
                "name": index_name,
                "prefix": f"{index_name}_vector",
                "key_separator": ":",
            },
            # customize fields that are indexed
            "fields": [
                {"name": "id", "type": "tag"},
                {"name": "doc_id", "type": "tag"},
                {"name": "text", "type": "text"},
                {"name": "vector", "type": "vector",
                 "attrs": {"dims": dims, "algorithm": "flat", "distance_metric": "cosine", }},
            ],
        }
    )

    redis_client = Redis.from_url("redis://172.31.128.153:6379")
    return RedisVectorStore(schema=redis_index_schema, redis_client=redis_client, overwrite=overwrite)
