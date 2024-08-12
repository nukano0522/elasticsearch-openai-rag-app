import json


def search(
    es, index_name: str, model_name: str, search_pattern: str, search_word: str, size=30
):

    def create_query(search_word):
        """クエリの作成
        Args:
            search_word (str): 検索クエリ
        Returns:
            dict: クエリ
        """
        if search_pattern == "vector":
            query_file = "vector_search_02.json"
        elif search_pattern == "hybrid":
            query_file = "hybrid_search_01.json"

        with open(f"./query/{query_file}", "r") as f:
            query_data = f.read()

        replace_dict = {
            "{WORD}": search_word,
            "{MODEL_ID}": model_name,
        }
        for key, value in replace_dict.items():
            query_data = query_data.replace(key, value)

        query = json.loads(query_data)

        return query

    script_query = create_query(search_word)
    print(script_query)

    response = es.search(index=index_name, body=script_query)

    result = []

    # 結果の表示
    for hit in response["hits"]["hits"]:
        title = hit["_source"]["title"]
        text = hit["_source"]["text"][:500]
        score = hit["_score"]
        result.append({"title": title, "text": text, "score": score})

    return result
