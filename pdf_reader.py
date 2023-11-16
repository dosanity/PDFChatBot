# Imports
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA,  ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
import param
from flask import *  
import os
import openai
import sys
sys.path.append('../..')

# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv()) # read local .env file




import datetime
current_date = datetime.datetime.now().date()
if current_date < datetime.date(2023, 9, 2):
    llm_name = "gpt-3.5-turbo-0301"
else:
    llm_name = "gpt-3.5-turbo"

def load_db(file, api_key):
    os.environ['OPENAI_API_KEY'] = api_key
    # load documents
    loader = PyPDFLoader(file)
    documents = loader.load()
    # split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    # define embedding
    embeddings = OpenAIEmbeddings()
    # create vector database from data
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
    # retriever = db.as_retriever()
    
    prompt_template_doc = """

    Use the following pieces of context to answer the question at the end. {context}
    You can also look into chat history. {chat_history}
    If you still can't find the answer, please respond: "Please ask a question related to the document."

    Question: {question}
    Answer:
    """
    prompt_doc = PromptTemplate(
        template=prompt_template_doc,
        input_variables=["context", "question", "chat_history"],
    )
    # define retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    #Keeps a buffer of history and process it
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        return_messages=True
    )
    # create a chatbot chain. Memory is managed externally.
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name=llm_name, temperature=0), 
        chain_type="stuff", 
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt_doc},
        memory=memory
    )
    return qa 

def load_db_sum(file, api_key):
    os.environ['OPENAI_API_KEY'] = api_key
    # load documents
    loader = PyPDFLoader(file)
    documents = loader.load()
    # split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    # define embedding
    embeddings = OpenAIEmbeddings()
    # create vector database from data
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
    # retriever = db.as_retriever()
    
    # prompt_template_doc = """
    # Use chat history : {chat_history} to determine the condition you are to research if not blank

    # Use the following pieces of context to answer the question at the end.
    # {context}
    # If you still cant find the answer, just say that you don't know and don't try to make up an answer.
    # You can also look into chat history.
    # {chat_history}
    # Question: {question}
    # Answer:
    # """
    # prompt_doc = PromptTemplate(
    #     template=prompt_template_doc,
    #     input_variables=["context", "question", "chat_history"],
    # )
    # define retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    #Keeps a buffer of history and process it
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        return_messages=True
    )
    # create a chatbot chain. Memory is managed externally.
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name=llm_name, temperature=0), 
        chain_type="stuff", 
        retriever=retriever,
        # combine_docs_chain_kwargs={"prompt": prompt_doc},
        memory=memory
    )
    return qa 