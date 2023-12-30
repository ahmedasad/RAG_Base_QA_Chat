import config
from generation.augmented_generation import AugmentedGeneration
from form_extarction.form_field_extraction import web_page_attributes
from indexing.document_loader import FileLoader
from indexing.document_transformer import DocuemntSplitter
from indexing.database import RAGDatabase
from openai import OpenAI
# - Augmented Generation

'''
    - Class written to perform different operations on given query/prompts
    - we are using some synonym key words to filter the URL and some test cases words, so we can search on DB
    - for contextual relevant info
'''
class Main():
    li = ["qa","test","automation", "test case", "login"]
        
    def __init__(self):
        self.generative_model = AugmentedGeneration()
        self.dataBase = RAGDatabase()

    # To check if the query contains url
    def fetch_url_query(self, query):
        url = ''
        for item in query.split():
            if 'http' in item:
                url = item
                print(url)
                break
        if url != '':
            elements = web_page_attributes(url)
            if len(elements) > 0:
                return ', '.join(elements)
            
        return 0

    def process_user_query(self, query):
        
        # fetch if there is any URL in user content/query
        get_url_elements = self.fetch_url_query(query)
        
        isit = False
        for item in Main.li:
            if item in query:
                isit = True
                break

        if isit:
            # get similar info from vector/Qdrant DB
            data_from_db = self.dataBase.search_in_db(query)[0].page_content
            print("QUERY::::", data_from_db)
            
            
            if get_url_elements != 0:
                # Create a prompt when no URL is give in user query/prompt  
                prompt = f"query: {query}\n\nContext: {data_from_db}\n\n Ids of fields on webpage: {get_url_elements}"
            else:
                # Create a prompt when URL is give in user query/prompt 
                prompt =  f"Query: {query}. Context: {data_from_db}"
        
        # if query/promt doesn't ask questions related to system
        else: prompt = f"Greet user and Give a very very limited but nice response regarding {query}, and also tell the user that you are precisely focused on Software Quality Assurance and you don't cater any other query. Though, right now, you can only help on 'Login webpage's' test cases and to utilise this functionality user need to provide a login page URL, and in the end, inform user that in near future you will be able help on webpage testing."
        
        response = self.generative_model.generate_optamised_response(prompt)
        return response



'''
    - Written This function, runs independently, use to load data and making chunks and creating embeddings
'''

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
