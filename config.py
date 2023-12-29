from os import getenv
from dotenv import load_dotenv
from dotenv.main import find_dotenv
import os
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DATABASE_NAME= os.getenv("QDRANT_CONNECTION_NAME")
DB_CONNECTION_URL=os.getenv("QDRANT_URL")
DOC_TYPE = 'pdf'

