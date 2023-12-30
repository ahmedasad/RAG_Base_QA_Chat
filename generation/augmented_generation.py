
from openai import OpenAI

import config

class AugmentedGeneration():
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    def format_context(self,documents):
        formatted_context =  '\n'.join([doc.page_content for doc in documents])
        return formatted_context

    def generate_optamised_response(self, prompt, response=None):
        # prompt = f"I have a query: '{query}' and have certain knowledge on it: {response}."
        
        comp = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": prompt}]
        )
        return comp.choices[0].message.content