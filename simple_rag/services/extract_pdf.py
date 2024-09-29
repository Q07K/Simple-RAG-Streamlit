from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


def pdf_extractor(path: str) -> list[Document]:
    """PDF에서 TEXT를 추출하는 함수

    Parameters
    ----------
    path : str
        PDF 주소

    Returns
    -------
    list[Document]
        Python list로 감싼 LangChain Document
    """
    pages = []
    loader = PyPDFLoader(file_path=path)
    for page in loader.load():
        pages.append(page)
    return pages
