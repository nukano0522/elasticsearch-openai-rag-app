from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.client import IngestClient


import json, gzip
import re
import pandas as pd

DOC_NAME = "jawikinews-20240805-cirrussearch-content.json.gz"
IDX_LEN_MAX = 1000
INFEREENCE_PIPELINE_NAME = "bert-japanese-text-embeddings"
DEFAULT_INDEX_NAME = "vector-test-index-01"


def get_index_info(es):
    """インデックス一覧情報の取得
    Args:
        index_name (str): インデックス名
    Returns:
    """
    # インデックス一覧の取得
    indices = es.cat.indices(index="*", h="index").splitlines()
    # インデックスの表示
    indices_list = []
    for index in indices:
        if re.match(r"^[^.].*", index):
            indices_list.append(index)

    res = []
    for index in indices_list:
        doc_count = es.count(index=index)
        res.append({"index": index, "doc_count": doc_count["count"]})

    return res


def get_inference_pipeline(es, embedding_model):
    """インデックスの作成
    Args:
        es (Elasticsearch): Elasticsearchの接続情報
        index_name (str, optional): インデックス名. Defaults to "DEFAULT_INDEX_NAME".
    """
    if embedding_model == "cl-tohoku__bert-base-japanese-v2":
        INFEREENCE_PIPELINE_NAME = "bert-japanese-text-embeddings"
    elif embedding_model == "cl-nagoya__sup-simcse-ja-base":
        INFEREENCE_PIPELINE_NAME = "sup-simcse-japanese-text-embeddings"
    else:
        raise ValueError("Invalid model name.")

    # パイプラインが存在しない場合は作成
    if not IngestClient(es).get_pipeline(id=INFEREENCE_PIPELINE_NAME, ignore=404):
        with open("./config/inference_pipeline.json", "r") as f:
            inference_pipeline_data = f.read()
        replace_dict = {
            "{MODEL_ID}": embedding_model,
        }
        for key, value in replace_dict.items():
            inference_pipeline_data = inference_pipeline_data.replace(key, value)
        inference_pipeline_config = json.loads(inference_pipeline_data)

        IngestClient(es).put_pipeline(
            id=INFEREENCE_PIPELINE_NAME, body=inference_pipeline_config
        )
        print(f"Created pipeline {INFEREENCE_PIPELINE_NAME}")

    return INFEREENCE_PIPELINE_NAME


def get_data():
    with gzip.open(f"./data/{DOC_NAME}") as f:
        docs = []
        for line in f:
            json_line = json.loads(line)
            if "index" not in json_line:
                doc = json_line
                docs.append(doc)
    return docs


def create_index(es, index_name, embedding_model):
    """インデックスの作成
    Args:
        es (Elasticsearch): Elasticsearchの接続情報
        index_name (str, optional): インデックス名. Defaults to "DEFAULT_INDEX_NAME".
    """

    es.indices.delete(index=index_name, ignore=[404])
    print(f"Deleted index {index_name}")

    with open("./config/index_vector_01.json", "r") as f:
        mapping = json.load(f)

    es.indices.create(index=index_name, body=mapping)
    print(f"Created index {index_name}")

    INFEREENCE_PIPELINE = get_inference_pipeline(es, embedding_model)
    print(f"Using pipeline {INFEREENCE_PIPELINE}")

    def bulk_insert(docs):
        for doc in docs:
            yield {
                "_op_type": "index",
                "_index": index_name,
                "_source": {"title": doc["title"], "text": doc["text"]},
                "pipeline": INFEREENCE_PIPELINE,
            }

    docs = get_data()
    print(f"Read {len(docs)} documents.")
    bulk(es, bulk_insert(docs), chunk_size=50, request_timeout=600)


def create_index_async(es, index_name, embedding_model):
    """インデックスの作成
    Args:
        es (Elasticsearch): Elasticsearchの接続情報
        index_name (str, optional): インデックス名. Defaults to "DEFAULT_INDEX_NAME".
    """

    es.indices.delete(index=index_name, ignore=[404])
    print(f"Deleted index {index_name}")

    with open("./config/index_vector_01.json", "r") as f:
        mapping = json.load(f)

    es.indices.create(index=index_name, body=mapping)
    print(f"Created index {index_name}")

    INFEREENCE_PIPELINE = get_inference_pipeline(es, embedding_model)
    print(f"Using pipeline {INFEREENCE_PIPELINE}")

    async def gendata(docs):
        for doc in docs:
            yield {
                "_op_type": "index",
                "_index": index_name,
                "_source": {"title": doc["title"], "text": doc["text"]},
                "pipeline": INFEREENCE_PIPELINE,
            }

    from elasticsearch.helpers import async_bulk

    async def main(docs):
        await async_bulk(es, gendata(docs), chunk_size=50, request_timeout=600)

    docs = get_data()
    print(f"Read {len(docs)} documents.")

    # イベントループを取得
    import asyncio

    # loop = asyncio.get_event_loop()
    # # 並列に実行して終るまで待つ
    # loop.run_until_complete(main(docs))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(docs))
