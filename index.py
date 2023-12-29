from dotenv import load_dotenv
import os
from langchain import document_loaders
from langchain.llms import OpenAI
os.environ["OPENAI_API_KEY"] = "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"


from retrieval.document_loader import FileLoader
from retrieval.database import RAGDatabase
from retrieval.document_transformer import DocuemntSplitter
import config
from generation.augmented_generation import AugmentedGeneration


def setup_model():
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    llm = OpenAI(api_key=api_key)
    return llm

# - Retrieval
        # Currently running a contextual retrieval
def fetch_response_from_data_source(query: str, data_source):
    
    query = query.lower()
    best_match = None
    best_match_score = 0
    for key, content in data_source.items():
        match_score = sum(word in content.lower() for word in query.split())
        print(f"Match Score: {match_score} for key: {key} ")    
        if match_score > best_match_score:
            best_match_score = match_score
            best_match = content
            
    print("Best Match: ", best_match)
    return best_match if best_match else "No relevant knowledge on it"


# - Augmented Generation
def generate_optamised_response(query, response, llm):
    prompt = f"I have a query: '{query}' and have certain knowledge on it: {response}."
    return llm.generate(prompts=[prompt], max_tokens=1500).generations[0][0].text


def main():
    
    
    
    # file_loader = FileLoader('./data')
    # docs = file_loader.load_text_file()
    # splitter = DocuemntSplitter(docs)
    # chunks = splitter.create_chunks()
    
    # print("Document Chunks: \n",chunks)
    # print("creating table and inserting into table:\n")
    db = RAGDatabase()
    
    # db.load_documents_into_database(chunks)
    data = db.search_in_table()
    for item in data:
        print(item.page_content)
    ag = AugmentedGeneration()
    ag.format_context(data)
    
    
    # llm = setup_model()

    # data_source = {
    #     "selenium introduction": "test framework refers to a suite of tools that are widely used in the testing community when it comes to cross-browser testing. test framework cannot automate desktop applications; it can only be used in browsers. It is considered to be one of the most preferred tool suites for automation testing of web applications as it provides support for popular web browsers which makes it very powerful.",
    #     "selenium webdriver": "test framework WebDriver is a web framework that permits you to execute cross-browser tests. This tool is used for automating web-based application testing to verify that it performs expectedly.",
    # }

    # query = "what selenium?"
    
    # retrieve_response = fetch_response_from_data_source(query, data_source)
 
    # improved_response = generate_optamised_response(query, retrieve_response, llm)
 
    # print(improved_response)

main()
