from langchain_google_genai import GoogleGenerativeAIEmbeddings


def google_model(
    google_api_key: str,
    model_name: str,
) -> GoogleGenerativeAIEmbeddings:
    """Google에서 지원하는 Embedding Model을 사용하기 위한 기능

    Parameters
    ----------
    google_api_key : str
        발급받은 Google API-KEY
    model_name : str
        사용할 Embedding Model 이름

    Returns
    -------
    GoogleGenerativeAIEmbeddings
        생성된 vector
    """
    embedding = GoogleGenerativeAIEmbeddings(
        model=f"models/{model_name}",  # 사용할 Embedding Model
        google_api_key=google_api_key,  # Google API-KEY
    )

    return embedding
