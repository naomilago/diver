from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.runnables.base import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from IPython.display import display, Markdown
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.constants import *
from config.config import *
from langchain import hub
from loguru import logger
from uuid import uuid4
from typing import *
import numpy as np
import requests
import tiktoken
import warnings
import json
import bs4
import os

warnings.filterwarnings('ignore')

verbose = True

def tokens_counter(text: str, encoding: str) -> int:
  '''Returns the number of tokens in a given text.'''
  
  encoding = tiktoken.get_encoding(encoding)
  
  return len(encoding.encode(text))

def similarity_calculator(vector_a: Sequence, vector_b: Sequence) -> float:
  '''Returns the calculated similarity between two vectors.'''

  dot_product = np.dot(vector_a, vector_b)
  norm_a = np.linalg.norm(vector_a)
  norm_b = np.linalg.norm(vector_b)
  
  return dot_product / (norm_a * norm_b)