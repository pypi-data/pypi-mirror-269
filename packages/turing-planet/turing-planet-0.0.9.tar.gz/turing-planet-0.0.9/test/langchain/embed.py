import logging
import time
import uuid

from langchain.vectorstores.clickhouse import ClickhouseSettings, Clickhouse

from turing_planet.langchain.embeddings.sparkai import SparkAIEmbedding

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# config
config = ClickhouseSettings(host="172.31.128.153",
                            port=8123,
                            database="lc_test",
                            metric="dot",
                            table="test_clickhouse",
                            index_param=["'cosineDistance'", 100])

vector_store = Clickhouse(
    embedding=SparkAIEmbedding(),
    # embedding=SparkAIEmbedding(endpoint="172.31.101.142:9980"),
    config=config)


def clickhouse_add() -> None:
    vector_store.add_texts(
        texts=[
            "???????????5000??????????????????????????????????????????????????"]
    )
    vector_store.add_texts(
        texts=["?????????????????????"]
    )
    vector_store.add_texts(
        texts=["??????????"]
    )


def clickhouse_search() -> None:
    output = vector_store.similarity_search("????", k=1)
    print(output)


def insert_bulk_1024():
    config_1024 = ClickhouseSettings(host="172.31.128.153",
                                     port=8123,
                                     database="lc_test",
                                     metric="dot",
                                     table="test_clickhouse_100w",
                                     index_param=["'cosineDistance'", 100])

    vectorStore = Clickhouse(
        embedding=SparkAIEmbedding(endpoint="172.31.101.142:9980"),
        config=config_1024)

    for e in range(90000):
        vectorStore.add_texts(
            texts=[str(uuid.uuid4())]
        )


def search_1024():
    config_1024 = ClickhouseSettings(host="172.31.128.153",
                                     port=8123,
                                     database="lc_test",
                                     metric="dot",
                                     table="test_clickhouse_100w",
                                     index_param=["'cosineDistance'", 100])

    vectorStore = Clickhouse(
        embedding=SparkAIEmbedding(endpoint="172.31.101.142:9987"),
        config=config_1024)
    start = time.time()
    # output = vectorStore.similarity_search("????", k=1)
    loop = 100
    for e in range(loop):
        vectorStore.similarity_search(str(uuid.uuid4()), k=1)
    cost = time.time() - start
    print("cost", cost/loop)


if __name__ == '__main__':
    vector_store.drop()
    # clickhouse_add()
    # clickhouse_search()

    # insert_bulk_1024()
    # search_1024()
