import logging

from dotenv import load_dotenv
from llama_index import StorageContext, ServiceContext
from llama_index.storage.docstore import MongoDocumentStore
from llama_index.storage.index_store import MongoIndexStore
from llama_index.vector_stores import RedisVectorStore

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI

# 加载环境变量
load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为DEBUG，可以根据需要修改
    format="%(asctime)s - %(levelname)s - %(message)s",
)

vector_filter_key = "location"

redis_store = RedisVectorStore(index_name=f"llamaindex-introduce",
                               index_prefix=f"llamaindex-introduce_vector",
                               redis_url="redis://172.31.128.153:6379",
                               overwrite=True,
                               metadata_fields=[vector_filter_key])

mongo_doc_store = MongoDocumentStore.from_uri(uri="mongodb://root:Mgadmin_1234@172.31.164.103:30006",
                                              db_name="llamaindex-introduce")

mongo_index_store = MongoIndexStore.from_uri(uri="mongodb://root:Mgadmin_1234@172.31.164.103:30006",
                                             db_name="llamaindex-introduce")

storage_context = StorageContext.from_defaults(vector_store=redis_store, docstore=mongo_doc_store,
                                               index_store=mongo_index_store)

embed_model = SparkAIEmbedding(domain="emb_v1")

llm = SparkAI()

service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)
