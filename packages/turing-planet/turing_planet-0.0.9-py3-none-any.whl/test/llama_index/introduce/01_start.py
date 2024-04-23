import logging

from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex

from turing_planet.llama_index.embeddings.sparkai import SparkAIEmbedding
from turing_planet.llama_index.llms.sparkai import SparkAI

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
endpoint = "172.31.164.103:9980"

if __name__ == '__main__':
    # 使用自定义embedding和llm
    embed_model = SparkAIEmbedding(endpoint=endpoint, domain="emb_v1")
    llm = SparkAI(endpoint=endpoint)
    service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)

    # 加载数据
    documents = SimpleDirectoryReader("../data").load_data(show_progress=True)

    # 创建索引
    index = VectorStoreIndex.from_documents(documents=documents, service_context=service_context)

    # 创建查询引擎
    query_engine = index.as_query_engine(similarity_top_k=3)

    # 执行查询
    response = query_engine.query("截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？")
    print(response)
