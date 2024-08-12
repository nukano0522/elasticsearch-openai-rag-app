import os, json
from search import search
from connector import connect_to_elasticsearch
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def rag(es, question: str):
    es_res = search(
        es,
        index_name="bert-vector-index-01",
        model_name="cl-tohoku__bert-base-japanese-v2",
        search_pattern="vector",
        search_word=question,
    )
    # print(es_res)

    # textの結果を格納
    text_results = []
    for res in es_res:
        text_results.append(res["text"])

    # print(text_results)
    # print(f"api_key: {api_key}")

    # 質問（QUESTION）と検索結果（text_results）の組み合わせをOpenAIの入力として、検索結果を元に回答を生成するようなプロンプトを作成
    prompt = f"""
    以下の質問に対して、検索結果を元に回答を生成してください。また足りない情報は適宜あなたが持っている知識を使って補ってください。
    出力はマークダウン形式でわかりやすいようにしてください。

    # 質問
    {question}

    # 検索結果
    ## 1. {text_results[0]}
    ## 2. {text_results[1]}
    ## 3. {text_results[2]}
    ## 4. {text_results[3]}
    ## 5. {text_results[4]}
    ## 6. {text_results[5]}
    ## 7. {text_results[6]}
    ## 8. {text_results[7]}
    ## 9. {text_results[8]}
    ## 10. {text_results[9]}

    # 回答
    """

    # print(prompt)

    client = OpenAI()

    print("OpenAI へのリクエストを送信中...")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o-mini",
        )
    except Exception as e:
        print(e)
        return "エラーが発生しました。"

    print("OpenAI からのレスポンスを受信しました。")
    # print(chat_completion.choices[0].message.content)

    return chat_completion.choices[0].message.content
