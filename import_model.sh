#!/bin/bash

# embeddingモデル
# cl-tohoku/bert-base-japanese-v2
# cl-nagoya/sup-simcse-ja-base
# ヘルプメッセージの表示
show_help() {
  echo "Usage: $0 [-h] <hub-model-id>"
  echo ""
  echo "Options:"
  echo "  -h                Show this help message and exit"
  echo ""
  echo "Arguments:"
  echo "  hub-model-id      The ID of the model to import from the huggingface-hub"
}

# 引数が指定されているか確認
if [ "$1" == "-h" ]; then
  show_help
  exit 0
fi

if [ -z "$1" ]; then
  echo "Error: hub-model-id is required"
  show_help
  exit 1
fi

python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt

# 引数を変数に格納
HUB_MODEL_ID=$1

# コマンドの実行
eland_import_hub_model \
  --clear-previous \
  --url "https://localhost:9200" \
  --ca-certs "./backend/api/certs/ca.crt" \
  --es-username elastic \
  --es-password elastic \
  --hub-model-id "$HUB_MODEL_ID" \
  --task-type text_embedding \
  --start

