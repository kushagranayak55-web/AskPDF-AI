# load pdf
# split into chunks
# create embeddings
# store into chroma

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()


def create_database(pdf_path):

    # load pdf
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(docs)

    # create embeddings
    embedding_model = MistralAIEmbeddings(
        model="mistral-embed"
    )

    # store into chroma
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="chroma_db"
    )

    print("Database Created Successfully")