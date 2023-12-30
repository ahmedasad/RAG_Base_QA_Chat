from typing import Text
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

