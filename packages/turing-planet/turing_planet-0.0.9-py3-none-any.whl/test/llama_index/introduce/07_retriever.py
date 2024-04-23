from llama_index import VectorStoreIndex, get_response_synthesizer
from llama_index.indices.vector_store import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.vector_stores import MetadataFilters, MetadataFilter, FilterOperator

from introduce_base import llm, redis_store, service_context, vector_filter_key


def query():
    #  向量检索
    vector_index = VectorStoreIndex.from_vector_store(vector_store=redis_store,
                                                      service_context=service_context)

    # vector_retriever = vector_index.as_retriever(similarity_top_k=3)

    # 设置过滤条件
    filters = MetadataFilters(
        filters=[
            MetadataFilter(key=vector_filter_key, operator=FilterOperator.EQ, value="hf"),
        ]
    )
    vector_retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=3, filters=filters)

    response_synthesizer = get_response_synthesizer(
        service_context=service_context
    )

    query_engine = RetrieverQueryEngine(retriever=vector_retriever, response_synthesizer=response_synthesizer)

    question = "截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？ 简单介绍下。"
    response = query_engine.query(question)
    print(f"Q:{question}")
    print("A:" + response.response.replace("<ret>", "\n").replace("<end>", "\n"))
    print("---------------\n")


if __name__ == '__main__':
    query()
