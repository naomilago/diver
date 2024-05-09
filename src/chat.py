from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.runnables.base import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from IPython.display import display, Markdown
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain import hub
from uuid import uuid4
import streamlit as st
import requests
import warnings
import time
import json
import bs4
import os

warnings.filterwarnings('ignore')

keys = json.load(open('../keys.json'))

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = f'RAG'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = keys['LANGSMITH_API_KEY']

hf_embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

loader = WebBaseLoader(
  web_paths=('https://lilianweng.github.io/posts/2019-11-10-self-supervised/',),
  bs_kwargs=dict(
    parse_only=bs4.SoupStrainer(
      class_=('post-content', 'post-title', 'post-header')
    )
  )
)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter()
splits = text_splitter.split_documents(docs)

vector_store = Chroma.from_documents(documents=splits, embedding=hf_embeddings)

retriever = vector_store.as_retriever()

template = '''
You are a reference in academic communication, focusing on all kind of target audience. You always start your answers saying "I am Honey, honey."
Everyone listen and understand what you have to say, so you always answer with a great markdown syntax and in a very assertive, clear, and concise language. Use your knowledge to answer the following:

{question}
'''

prompt = PromptTemplate(template=template, input_variables=['question'])

llm = ChatGoogleGenerativeAI(
  google_api_key=keys['GEMINI_API_KEY'],
  model='gemini-1.5-pro-latest',
  temperature=0
)

docs_formatter = lambda docs: str.join('\n\n', (_.page_content for _ in docs))

chain = RunnableSequence((
  {'context': retriever | docs_formatter, 'question': RunnablePassthrough()}
  | prompt
  | llm
  | StrOutputParser()
))

with st.sidebar:
  "Hi there! 👋"
  "This is a simple chatbot that uses the Google Generative AI model to answer your questions."
  "Feel free to ask anything! 🤖"

st.title("💬 Chatbot")

if "messages" not in st.session_state:
  st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
  st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
  st.session_state.messages.append({"role": "user", "content": prompt})
  st.chat_message("user").write(prompt)
  time.sleep(2)
  response = chain.invoke(prompt)
  st.session_state.messages.append({"role": "assistant", "content": response})
  st.chat_message("assistant").write(response)