# Elasticsearch + FastAPI + Streamlit を使った検索アプリ

## 準備

```bash
# Wikipediaのデータを使うため、ダウンロードしておく
- ubuntu: 
    - wget -P ./backend/api/data https://dumps.wikimedia.org/other/cirrussearch/current/jawikibooks-20240812-cirrussearch-general.json.gz 
- windows: 
    - curl -L -o ./backend/api/data/jawikinews-20240805-cirrussearch-content.json.gz https://dumps.wikimedia.org/other/cirrussearch/current/jawikibooks-20240812-cirrussearch-general.json.gz 
```

- docker-compose.ymlと同階層に.envファイルを用意

```env
ELASTIC_PASSWORD = your_password
KIBANA_PASSWORD = your_password
ES_PORT = 9200
CLUSTER_NAME = test_cluster
LICENSE = trial
MEM_LIMIT = 3573741824
KIBANA_PORT = 5601
OPENAI_API_KEY = xxxx
```

- コンテナ立ち上げる前に以下実行しておく（実行しないとメモリ不足エラーになる）

``` bash
sysctl -w vm.max_map_count=262144
```

（参考） https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html

## Usage

- コンテナ立ち上げ

```bash
docker compose up --build
```

- embeddingモデルをElasticSearchにインポートする

```bash
./import_model.sh <hub-model-id>
```

- API経由でインデックス作成

```bash
curl -X POST http://localhost:8002/es/create_index/bert-vector-index-01/cl-tohoku__bert-base-japanese-v2
```

- http://localhost:8501/ からStreamlitアプリにアクセス


## 参考資料

- https://techblog.zozo.com/entry/elasticsearch-mapping-config-for-japanese-search

- https://qiita.com/shin_hayata/items/41c07923dbf58f13eec4