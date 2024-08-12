from fastapi import FastAPI
from connector import connect_to_elasticsearch, connect_to_async_elasticsearch
from index import create_index, create_index_async, get_index_info
from search import search_keyword

DEFAULT_INDEX_NAME = "vector-test-index-01"
DEFAULT_MODEL_NAME = "cl-tohoku__bert-base-japanese-v2"

app = FastAPI()
es = connect_to_elasticsearch()


# test
@app.get("/")
def read_root():
    return {"Hello": "World"}


# インデックス情報
@app.get("/es/index/info")
def get_index_info_route(index_name: str = DEFAULT_INDEX_NAME):
    return get_index_info(es)


# インデックス作成
@app.post("/es/create_index/{index_name}/{embedding_model}")
def create_index_route(index_name: str, embedding_model: str):
    create_index(es, index_name, embedding_model)
    return {"message": "index created."}


# 非同期インデックス作成
@app.post("/es/create_index_async/{index_name}/{embedding_model}")
def create_index_async_route(index_name: str, embedding_model: str):
    es_a = connect_to_async_elasticsearch()
    create_index_async(es_a, index_name, embedding_model)
    return {"message": "index created."}


# クエリを指定して検索
@app.get("/search/{index_name}/{model_name}/{search_word}")
def search_keyword_route(
    index_name: str = DEFAULT_INDEX_NAME,
    model_name: str = DEFAULT_MODEL_NAME,
    search_word: str = "日本",
):
    return search_keyword(es, index_name, model_name, search_word)
