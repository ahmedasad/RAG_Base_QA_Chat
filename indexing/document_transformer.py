from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocuemntSplitter():
    def __init__(self, docuemnt):
        self.docuemnt = docuemnt
        self.text_split_rule = None
        
    def split_rule(self):
        self.text_split_rule = RecursiveCharacterTextSplitter(
            chunk_size=450,
            chunk_overlap = 10
        )

    def create_chunks(self):
        self.split_rule()
        return self.text_split_rule.split_documents(self.docuemnt)