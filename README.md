# Elasticsearch + FastAPI + Streamlit を使った検索アプリ

![elasticsearch-streamlit-demo-2023-11-26_15 55 52](https://github.com/nukano0522/elasticsearch-fastapi-streamlit-app/assets/30750233/7edaaa27-62b5-4bd7-89c5-9c68e8710b9a)


## 実行環境
- Ubuntu 20.04.6 LTS (Focal Fossa)
- Docker version 20.10.25
- docker-compose version 1.29.0

## 準備

``` bash
# Wikipediaのデータを使うため、ダウンロードしておく
wget -P ./backend/api/data https://dumps.wikimedia.org/other/cirrussearch/current/jawikinews-20240805-cirrussearch-general.json.gz 
curl -L -o ./backend/api/data/jawikinews-20240805-cirrussearch-content.json.gz https://dumps.wikimedia.org/other/cirrussearch/current/jawikinews-20240805-cirrussearch-content.json.gz
```

- docker-compose.ymlと同階層に.envファイルを用意
``` env
ELASTIC_PASSWORD = your_password
KIBANA_PASSWORD = your_password
ES_PORT = 9200
CLUSTER_NAME = test_cluster
LICENSE = trial
MEM_LIMIT = 3573741824
KIBANA_PORT = 5601
```

- コンテナ立ち上げる前に以下実行しておく（実行しないとメモリ不足エラーになる）
``` bash
sysctl -w vm.max_map_count=262144
```
（参考） https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html


## Usage
``` bash
# コンテナ立ち上げ
docker-compose up

# 証明書のコピー
# バックエンド（FastAPI）とelasticsearchの通信に証明書が必要
# Docker間通信で証明書を取得できるのかもしれないがうまくいかなかったので、elasticsearchのコンテナからコピーして使用
docker cp es01:/usr/share/elasticsearch/config/certs/ca/ca.crt ./backend/api

# 日本語埋め込みモデル
```bash
eland_import_hub_model \
--clear-previous \
--url "https://localhost:9200" \
--ca-certs "./backend/api/ca.crt" \
--es-username elastic \
--es-password elastic \
--hub-model-id cl-nagoya/sup-simcse-ja-base \
--task-type text_embedding \
--start
```

# --hub-model-id cl-tohoku/bert-base-japanese-v2 \

# FastAPI経由でインデックス作成
curl -X POST http://localhost:8002/es/create_index/bert-vector-index-01
curl -X POST http://localhost:8002/es/create_index/bert-vector-index-01/cl-tohoku__bert-base-japanese-v2
curl -X POST http://localhost:8002/es/create_index/simcse-vector-index-01/cl-nagoya__sup-simcse-ja-base

curl -X POST http://localhost:8002/es/create_index_async/bert-vector-index-01/cl-tohoku__bert-base-japanese-v2
curl -X POST http://localhost:8002/es/create_index_async/simcse-vector-index-01/cl-nagoya__sup-simcse-ja-base
```
- http://localhost:8501/ からStreamlitアプリにアクセス


## Screenshots

Include screenshots or demo videos of the project here.

![Screenshot](image URL)



## 参考資料
- https://techblog.zozo.com/entry/elasticsearch-mapping-config-for-japanese-search
- https://qiita.com/shin_hayata/items/41c07923dbf58f13eec4




