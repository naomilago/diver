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