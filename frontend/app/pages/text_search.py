import streamlit as st
import requests
import pandas as pd


def keyword_search():

    # フォームの作成
    with st.form(key="my_form"):
        model_name = st.selectbox(
            "モデルを選択してください",
            ("cl-tohoku__bert-base-japanese-v2", "cl-nagoya__sup-simcse-ja-base"),
        )
        text_input = st.text_input(label="検索キーワードを入力してください")
        submit_button = st.form_submit_button(label="Submit")

    # モデルによってインデックス名を変更
    if model_name == "cl-tohoku__bert-base-japanese-v2":
        INDEX_NAME = "bert-vector-index-01"
    elif model_name == "cl-nagoya__sup-simcse-ja-base":
        INDEX_NAME = "simcse-vector-index-01"

    # サブミットボタンが押されたときの処理
    if submit_button:
        # ここでバックエンドのデータ処理を行う
        res = requests.get(
            f"http://backend:8002/search/{INDEX_NAME}/{model_name}/{text_input}"
        )
        # st.write(res.json())
        data = res.json()
        df = pd.json_normalize(data)

        st.table(df)


def main():
    keyword_search()


if __name__ == "__main__":
    main()
