import config

# - Retrieval

# - Augmented Generation

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
 
    # print(improved_response)

main()
