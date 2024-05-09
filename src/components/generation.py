import sys
sys.path.append('D:/Deep Learning/Diver')

from config.constants import *
from config.config import *
from config.utils import *

def generator(question: str, langchain_api_key: str, google_api_key: str) -> str:
  '''Generates a response to the user's input, based on context, using the Gemini model.'''
  
  os.environ['LANGCHAIN_TRACING_V2'] = 'true'
  os.environ['LANGCHAIN_PROJECT'] = f'Diver - an AI chatbot for Naomi Lago\'s blog'
  os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
  os.environ['LANGCHAIN_API_KEY'] = langchain_api_key
  
  prompt = ChatPromptTemplate.from_template(DATA_PROCESSING['PROMPT_TEMPLATE'])
  hf_embeddings = HuggingFaceEmbeddings(model_name=DATA_PROCESSING['EMBEDDING_MODEL'])
  
  vector_store = Chroma(
    persist_directory=DATA_PROCESSING['VECTOR_STORE']['path'],
    collection_metadata=DATA_PROCESSING['VECTOR_STORE'],
    embedding_function=hf_embeddings
  )
  
  retriever = vector_store.as_retriever(search_kwargs={'k': 2})
  
  llm = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model=DATA_PROCESSING['LLM_MODEL'],
    max_output_tokens=1000,
    temperature=0.75
  )
  
  chain = RunnableSequence(
    {'context': retriever, 'question': RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
  )
  
  return chain.invoke(question)

if __name__ == '__main__':
  generator('What is the latest trend in Natural Language Processing?', langchain_api_key=settings.LANGSMITH_API_KEY, google_api_key=settings.GEMINI_API_KEY)