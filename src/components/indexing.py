import sys
sys.path.append('D:/Deep Learning/Diver')

from config.constants import *
from config.config import *
from config.utils import *

def indexer(*new_paths: str) -> None:
  '''Performs the indexing of the data in the vector store.'''

  paths = [path for path in new_paths if path not in DATA_INPUTS['DATA_FOLDERS']]
  
  if len(paths) == 0:
    logger.info('No new paths to index. Exiting...')
    return None
  else:
    logger.info(f'Indexing {len(paths)} new paths..')
  
  loader = WebBaseLoader(web_paths=DATA_INPUTS['URLS'].extend(paths))
  documents = loader.load()
  
  text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300,
    chunk_overlap=50
  )
  
  splits = text_splitter.split_documents(documents)
  
  Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory=DATA_PROCESSING['VECTOR_STORE']['path'],
    collection_metadata={
      'name': DATA_PROCESSING['VECTOR_STORE']['name'],
      'description': DATA_PROCESSING['VECTOR_STORE']['description']
    }
  )
  
  logger.info(f'Indexed {len(paths)} new paths successfully!')
  return None

if __name__ == '__main__':
  indexer()