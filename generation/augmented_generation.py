from openai import OpenAI
from qdrant_client.http import models

import config


class AugmentedGeneration():
    def __init__(self):
        self.client = OpenAI(
            api_key="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")

    def format_context(self, documents):
        formatted_context = '\n'.join([doc.page_content for doc in documents])
        return formatted_context

    def generate_optamised_response(self, prompt):
        comp = self.client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[{"role": "user", "content": prompt}]
        )
        return comp.choices[0].message.content

    #    return self.llm.generate(prompts=[prompt]).generations
