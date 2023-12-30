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

    def search_in_table(self,query):
        
        db = Qdrant(client=self.client, embeddings=self.embedding_model,
                    collection_name=config.DATABASE_NAME)
        return db.similarity_search_by_vector(embedding=self.embedding_model.embed_query(query))

