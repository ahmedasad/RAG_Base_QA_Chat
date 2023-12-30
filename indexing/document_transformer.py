from langchain.text_splitter import CharacterTextSplitter

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