

from typing import List, Dict
from langchain.docstore.document import Document
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document 

from tempfile import _TemporaryFileWrapper

from langchain.chains import RetrievalQA,  ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

llm_name = "gpt-3.5-turbo"

def pretty_print_docs(docs: List[Document]) -> None:
    return f"\n{'-' * 100}\n".join([f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)])


from dotenv import load_dotenv
load_dotenv()
# COHERE_API_KEY = os.getenv("COHERE_API_KEY")

def load_db(file, query: str, chain_type="stuff", k=2):
    # load documents
    loader = PyPDFLoader(file)
    documents = loader.load()
    # split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    # define embedding
    embeddings = CohereEmbeddings()
    # create vector database from data
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
     # create vector database from data
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
    # define retriever
    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": k})
    # create a chatbot chain. Memory is managed externally.
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name=llm_name, temperature=0), 
        chain_type=chain_type, 
        retriever=retriever, 
        return_source_documents=True,
        return_generated_question=True,
    )

    result = qa({"question": query, "chat_history": []})

    return [[query, result['answer']]]