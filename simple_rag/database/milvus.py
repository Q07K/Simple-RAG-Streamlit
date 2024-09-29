from langchain_milvus import Milvus


def milvus(embedding_model, zilliz_uri, zilliz_token) -> Milvus:
    vector_db = Milvus(
        embedding_function=embedding_model,  # Embedding 모델
        collection_name="langchain_example",  # Data를 저장할 Collection 이름
        connection_args={
            "uri": zilliz_uri,  # Zilliz "Public Endpoint"
            "token": zilliz_token,  # Zilliz "Token"
        },
        auto_id=True,
    )

    return vector_db
