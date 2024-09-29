""" milvus_repository.py """

from langchain_core.documents import Document
from langchain_core.embeddings.embeddings import Embeddings

from pymilvus import MilvusClient

from simple_rag.database.milvus import milvus


def add_documents(
    embedding_model: Embeddings,
    zilliz_uri: str,
    zilliz_token: str,
    documents: list[Document],
) -> bool:
    """LangChain Document를 Milvus zilliz Cloud에 넣어주는 기능

    입력받은 LangChain Document를 google embedding model을 사용하여 embedding 후
    Milvus zilliz Cloud에 넣어준다.

    Parameters
    ----------

    embedding_model : Embeddings
        사용할 embedding model
    zilliz_uri : str
        등록된 zilliz uri
    zilliz_token : str
        등록된 zilliz toekn
    documents : list[Document]
        Python list로 감싼 LangChain Document를 받는 변수(인수/Arguments)

    Returns
    -------
    bool
        Ture: 함수가 정상적으로 동작하는 경우
        False: 함수가 정상적으로 동작하지 않는 경우
    """

    try:
        vector_db = milvus(embedding_model, zilliz_uri, zilliz_token)

        # Milvus zilliz Cloud에 Document 추가
        vector_db.add_documents(documents=documents)
        return True
    except:
        return False


def get_unique_sources(zilliz_uri: str, zilliz_token: str) -> list[str | None]:
    """고유한 source(파일 이름)을 반환하는 기능

    Parameters
    ----------
    zilliz_uri : str
        등록된 zilliz uri
    zilliz_token : str
        등록된 zilliz toekn

    Returns
    -------
    list[str | None]
        고유한 source(파일 이름)
    """

    # Milvus에 접근
    client = MilvusClient(
        uri=zilliz_uri,  # Zilliz "Public Endpoint"
        token=zilliz_token,  # Zilliz "Token"
    )

    # Data 조회
    results = client.query(
        collection_name="langchain_example",  # Data를 저장할 Collection 이름
        filter="pk > 0",  # 데이터 고유 아이디가 0 보다 큰(모든 데이터) 조회
        output_fields=["source"],  # 반환할 field
    )

    unique_sources = set()
    for result in results:
        source = result.get("source", None)
        unique_sources.add(source)

    return list(unique_sources)
