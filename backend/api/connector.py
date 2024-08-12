from elasticsearch import Elasticsearch
from elasticsearch import AsyncElasticsearch
import os, time

CERTS_DIR = "./certs"


def connect_to_elasticsearch():
    # Elasticsearchのコンテナが立ち上がるまで接続試行する
    conn = False
    try_num = 0
    while not conn:
        try:
            es = Elasticsearch(
                "https://es01:9200",
                ca_certs=f"{CERTS_DIR}/ca.crt",
                basic_auth=("elastic", os.environ["ELASTIC_PASSWORD"]),
            )
            es_info = es.info()
            conn = True
        except:
            print("try connecting to elasticsearch...")
            try_num += 1
            time.sleep(3)
            if try_num >= 10:
                print("connection failed.")
                break
    print("Connection to Elasticsearch is complete.")
    print(f"es-info: {es.info()}")
    return es


def connect_to_async_elasticsearch():
    es_a = AsyncElasticsearch(
        "https://es01:9200",
        ca_certs=f"{CERTS_DIR}/ca.crt",
        basic_auth=("elastic", os.environ["ELASTIC_PASSWORD"]),
    )

    return es_a
