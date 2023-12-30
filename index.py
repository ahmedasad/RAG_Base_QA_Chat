import config
from generation.augmented_generation import AugmentedGeneration
from form_extarction.form_field_extraction import web_page_attributes
from indexing.document_loader import FileLoader
from indexing.document_transformer import DocuemntSplitter
from indexing.database import RAGDatabase
from openai import OpenAI
# - Augmented Generation


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
            data_from_db = self.dataBase.search_in_table(query)[0].page_content
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


# def main():

    # client = OpenAI(api_key= config.OPENAI_API_KEY)
    # file_loader = FileLoader('./data')
    # docs = file_loader.load_pdf_files()
    # splitter = DocuemntSplitter(docs)
    # chunks = splitter.create_chunks()

    # print("Document Chunks: \n",chunks)
    # print("creating table and inserting into table:\n")
    # db = RAGDatabase()

    # db.load_documents_into_database(chunks)
    # data = db.search_in_table()
    # for item in data:
    #     print(item.page_content)
    # ag = AugmentedGeneration()
    # ag.format_context(data)

#     # print(improved_response)



# main()
