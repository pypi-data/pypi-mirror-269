from test.llama_index.optimizing.base import build_summary_service_context, add_vector_index, query

INDEX_NAME = "hf_llamaindex_sm"

service_context = build_summary_service_context()

if __name__ == '__main__':
    add_vector_index(service_context=service_context, index_name=INDEX_NAME)

    query(service_context=service_context, index_name=INDEX_NAME)
