import time
import random
import tiktoken
from ..base import TransformerMixin
from ..walmart_llm import ChatModel

class LlmSummaryExtractor(TransformerMixin):

    def __init__(self, output_len, model_name="gpt-35-turbo", temperature=0., batch_size=500):
        self.output_len = output_len
        self.model_name = model_name
        self.template = "Summarize following sentences within {output_len} words:\n{text}"
        self.model = ChatModel(model_name=model_name, temperature=temperature, batch_size=batch_size)
        self.encoding = tiktoken.encoding_for_model(model_name=model_name)
    
    def transform(self, texts, topk=5, iterations=100, **params):
        prompts = []
        for iter in range(iterations):
            input_text = ""
            for idx in range(topk):
                if (self.model_name == "gpt-35-turbo" and len(self.encoding.encode(input_text)) > 4000) or \
                   (self.model_name == "gpt-4" and len(self.encoding.encode(input_text)) > 7000):
                    break
                input_text += f"sentence {idx}: {random.choice(texts).strip()}\n"
            prompts.append(self.template.format(output_len=self.output_len, text=input_text))
        
        s1 = time.time()
        responses = []
        for prompt in prompts:
            try:
                responses.append(self.model.completion(prompt))
            except:
                continue
        s2 = time.time()
        print(f"Time: {s2 - s1:.02f}s")
        return responses