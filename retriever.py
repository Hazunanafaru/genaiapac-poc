import os
from file_management import UPLOAD_DIRECTORY
from langchain.embeddings import GPT4AllEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader

#https://python.langchain.com/docs/integrations/text_embedding/gpt4all

def doc_indexer(filename):
    directory = os.path.join(UPLOAD_DIRECTORY, filename)
    loader = PyPDFLoader(directory)
    pages = loader.load_and_split()
    embeddings = GPT4AllEmbeddings()
    db = FAISS.from_documents(pages, embeddings)
    return db

def doc_retriever(db, query):
    pages = db.similarity_search(query)
    docs = []
    for i in range(len(pages)):
        no_hal = pages[i].metadata["page"]
        isi = pages[i].page_content
        a = f"""Nomor Halaman: {no_hal}
        \n\n
        Isi:\n
        {isi}
        """
        docs.append(a)
    return "\n\n".join(docs)