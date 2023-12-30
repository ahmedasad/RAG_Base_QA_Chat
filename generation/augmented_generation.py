from langchain.llms import OpenAI

import config

class AugmentedGeneration():
    def __init__(self):
        self.llm = OpenAI(api_key=config.OPENAI_API_KEY)
    
    def format_context(self,documents):
        formatted_context =  '\n'.join([doc.page_content for doc in documents])
        return formatted_context

    def generate_optamised_response(self, prompt):
        # prompt = f"I have a query: '{query}' and have certain knowledge on it: {response}."
        return self.llm.generate(prompts=[prompt]).generations[0][0].text