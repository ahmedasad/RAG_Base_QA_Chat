# Automate wrting SQA Test cases USING RAG


### What We implemented?
- **Objective**: We will used the Retrieval-Augmented Generation (RAG) to automate test cases writing by providing the  customised information / data regarding process of writing test case.
- **Skills Required**: Need to have knowledge of Python (as we are writing solution in Python), OpenAI models and LangChain libraries.
- **Innovative Techniques**: Will integrate retrieval mechanisms with generative models for enhanced AI capabilities.

## Demo Video:
https://github.com/ahmedasad/RAG_Base_QA_Chat/assets/20832655/64139378-f103-4f36-930e-d9739ee8fda3

### Pre-requisites:
  - **Retrieval-Augmented Generation (RAG)**: RAG is a technique for augmenting LLM knowledge with additional, often private or real-time, data.
      - **Components of RAG**:
          - **Retrieval**: Searchs/Extracts information from documents / datasets related to a given query/prompt.
          - **Generation**: Takes the retrieved info and uses it to generate a coherent (logical and well-organized) and contextually relevant response.

### Libraries and Tools used:
  - Python 3.12
  - openAI: we used the "gpt-3.5-turbo-1106"
  - Langchain: document_loaders, to load/read the docuemnts
  - Langchain: text_splitter, for making chunks of document
  - Langchain: OpenAIEmbedding, to create embeddings of chunks
  - Qdrant Vector DB: Used to store vectors
  - Selenium: Used to extract input fields related info from given Web page
  - streamlit for Chat UI
  - dotenv

### Phases / Steps of implementation:
Two major phases are:
    - Indexing: a pipeline for ingesting data from a source and indexing it. This usually happen offline.
    - Retrieval and generation: the actual RAG chain, which takes the user query at run time and retrieves the relevant data from the index, then passes that to the model.
    
**And it further divides into:**
  - **Document splitting**: First, will splitt docuemnt into small chunks.
  - **Embedding**: Then, will create embeddings of chunks and store in Vector DB.
  - **Info Retrieval**:
      - **Retrieve Data**: The retrieval system searches through it datasets/ documents to find info related to the query.
      - **Integration**: The retrieved info is then fed into the **generative model** along with the original query .
      - **Generation**: Generative Model uses both the **query/prompt** and **retrieved info**  to produce a detailed, informed response.

### Step 1:
  - Written divided file laoding, chunking operation, embedding and storing into different classes and will call them in main function in index.py.
    
```python
'''
    - Written This function, runs independently, use to load data and making chunks and creating embeddings
'''
from indexing.document_loader import FileLoader
from indexing.document_transformer import DocuemntSplitter
from indexing.database import RAGDatabase

def main():

    # Loading File
    file_loader = FileLoader('./data')
    docs = file_loader.load_pdf_files()
    
    # Making Chunks
    splitter = DocuemntSplitter(docs)
    chunks = splitter.create_chunks()

    # Loading embedded chunks into the DB
    db = RAGDatabase()
    db.load_documents_into_database(chunks)
    
main()
```

- File laoding class: Can load all documents in directory of both PDF and TXT.

```python
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader

'''
    - Class written to Load either PDF or Txt documents
    - It takes library and go through the whole library
'''
class FileLoader():
    def __init__(self,directory):
        self.directory = directory
        
    def load_text_file(self) -> TextLoader:
        docs = DirectoryLoader(self.directory, glob="**/*txt",loader_cls=TextLoader, show_progress = True)
        return docs.load()

    def load_pdf_files(self):
        docs = DirectoryLoader(self.directory, glob="**/*pdf",loader_cls=PyPDFLoader, show_progress = True) 
        return docs.load()
```

- Creating file chunks: It will split info in document into small chunks.

```python
from langchain.text_splitter import CharacterTextSplitter

'''
    - Class written to split any give document in chunk size of 1200 characters
'''
class DocuemntSplitter():
    def __init__(self, docuemnt):
        self.docuemnt = docuemnt
        self.text_split_rule = None
        
    def split_rule(self):
        self.text_split_rule = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=1200,
            length_function = len,
            chunk_overlap = 30
        )

    def create_chunks(self):
        self.split_rule()
        return self.text_split_rule.split_documents(self.docuemnt)
```

- Class written to store Create embeddings and store into DB, also perform operation of fetching info from database

```python
from qdrant_client import QdrantClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.qdrant import Qdrant
import config

'''
    - Class written to store embeddings into the DB 
    - and also provide functionality to fetch data from DB
'''
class RAGDatabase():

    def __init__(self):
        self.client = QdrantClient(host="localhost", port=6333)
        self.embedding_model = OpenAIEmbeddings(
            openai_api_key=config.OPENAI_API_KEY)
        self.table = None

    def load_documents_into_database(self, documents):
        print(config.DATABASE_NAME, config.DB_CONNECTION_URL)
        Qdrant.from_documents(documents, self.embedding_model,
                              collection_name=config.DATABASE_NAME, url=config.DB_CONNECTION_URL)

    def search_in_db(self,query):
        
        db = Qdrant(client=self.client, embeddings=self.embedding_model,
                    collection_name=config.DATABASE_NAME)
        return db.similarity_search_by_vector(embedding=self.embedding_model.embed_query(query))

```

### Step 2:
  - Retrieve Info and create Augmented response

```python

    # collecting relevant data from database
    def search_in_db(self,query):
        
        db = Qdrant(client=self.client, embeddings=self.embedding_model,
                    collection_name=config.DATABASE_NAME)
        return db.similarity_search_by_vector(embedding=self.embedding_model.embed_query(query))

    # will create augmented response using given info and LLM model
    def generate_optamised_response(self, prompt):

        comp = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": "You are an Software Quality Assuarance BOT"},
                      {"role": "user", "content": prompt}]
        )
        return comp.choices[0].message.content

    # get similar info from vector/Qdrant DB
    data_from_db = search_in_db(query)[0].page_content

    # Generate response on given query and retrieved info
    prompt =  f"Query: {query}. Context: {data_from_db}"

    response = generate_optamised_response(prompt)

```
