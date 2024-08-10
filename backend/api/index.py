from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.client import IngestClient


import os, pickle, time, json, gzip
import asyncio
import re
import pandas as pd

DOC_NAME = "jawikinews-20240805-cirrussearch-content.json.gz"
IDX_LEN_MAX = 1000
BERT_INFEREENCE_PIPELINE = "japanese-text-embeddings"
DEFAULT_INDEX_NAME = "vector-test-index-01"

def get_index_info(es):
    """ インデックス一覧情報の取得
    Args:
        index_name (str): インデックス名
    Returns:
    """
    # インデックス一覧の取得
    indices = es.cat.indices(index="*", h='index').splitlines()
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


def create_index(es, index_name=DEFAULT_INDEX_NAME):
    """ インデックスの作成
    Args:
        es (Elasticsearch): Elasticsearchの接続情報
        index_name (str, optional): インデックス名. Defaults to "DEFAULT_INDEX_NAME".
    """
    
    es.indices.delete(index=index_name, ignore=[404])
    print(f"Deleted index {index_name}")
        
    with open("./config/index_vector_01.json", "r") as f:
        mapping = json.load(f)

    # with open("./config/bert_inference_pipeline.json", "r") as f:
    #     bert_infer_pipeline_config = json.load(f)

    # IngestClient(es).put_pipeline(id=BERT_INFEREENCE_PIPELINE, body=bert_infer_pipeline_config)

    es.indices.create(index=index_name, body=mapping)
    print(f"Created index {index_name}")

    def bulk_insert(docs):
        for doc in docs:
            yield {
                "_op_type": "index",
                "_index": index_name,
                "_source": {
                    "title": doc["title"],
                    "text": doc["text"]
                },
                "pipeline": BERT_INFEREENCE_PIPELINE
            }
    docs = []
    with gzip.open(f"./data/{DOC_NAME}") as f:
        for line in f:
            json_line = json.loads(line)
            if "index" not in json_line:
                doc = json_line
                docs.append(doc)

    print(f"Read {len(docs)} documents.")
        
    batch_size = 100  # 1回に500件ずつ処理
    docs = docs[0:IDX_LEN_MAX]
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        bulk(es, bulk_insert(batch), request_timeout=60)
        print(f"Batch {i//batch_size + 1} inserted.")
    index_count = es.count(index=index_name)
    print(f"Indexed {index_count['count']} documents.")