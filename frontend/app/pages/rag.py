import streamlit as st
import requests
import pandas as pd


def rag():
    # 質問フォームの作成
    with st.form(key="my_form"):
        question = st.text_input(label="質問を入力してください", value="日本の首都は？")
        submit_button = st.form_submit_button(label="Submit")

    # サブミットボタンが押されたときの処理
    if submit_button:
        # ここでバックエンドのデータ処理を行う
        res = requests.get(f"http://backend:8002/rag/{question}")
        # data = res.json()
        # df = pd.json_normalize(data)
        # print(res)

        st.markdown(repr(res.text))


def main():
    rag()


if __name__ == "__main__":
    main()
