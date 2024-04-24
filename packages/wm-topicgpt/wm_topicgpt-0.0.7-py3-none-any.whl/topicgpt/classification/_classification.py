import re
from ..base import GeneratorMixin
from ..walmart_llm import ChatModel


class Classifier(GeneratorMixin):

    def __init__(self, model_name="gpt-35-turbo", temperature=0., batch_size=300):
        self.model_name = model_name
        self.model = ChatModel(model_name=model_name, temperature=temperature, batch_size=batch_size)

        self.template1 = """You are a ChatGPT user. Your task is to write a prompt asking a question about a topic. You are given some requirements, some examples and one topic below.
    
Here are some requirements you must follow:
1. Your output MUST be less than 100 words.
2. Your output MUST be related about the provided topic.
3. Only output the Topic.
    
Here are some good examples for your reference:
Topic: Acknowledging and forwarding applicant's email
Prompt: I want to thank the applicant for the interest.Would like to express to him that his email will be forwarded to the store manager at 2201.
    
Topic: Listing areas of development
Prompt: now i need to list areas of development
    
Topic: Steps to become a community partner in a health program
Prompt: Use this information to create an agreement form.2.Complete the Community Partnership Questionnaire: Fill out and submit the Community Partnership Questionnaire.This questionnaire will help gather important information about your organization and its capabilities.3.Be a Certified 501(c)(3) Organization: Ensure that your organization is a certified 501(c)(3) nonprofit organization.This certification is necessary to participate in the program as a community partner.4.Register your organization on the FH platform to receive live referrals: Register your organization on the FH platform to receive live referrals.This platform will connect you with individuals (CareSource Members) who have health-related social needs and require assistance.5.Connect individuals to resources to address their health-related social needs: As a community partner, you should be prepared to connect individuals to resources that can address their health-related social needs.
    
Topic: {topic}
Prompt:"""

        self.template2 = """You are a good editor. The following will give you some requirements, a topic list, some examples and a prompt. Your task is to judge which category this prompt belongs to according to the following requirements.

Here are some requirements you must follow:
1. Only output the number of the topic to which the prompt belongs.

Here is the topic list for your reference:
{topics}

Here are some good examples for your reference:
{examples}

Prompt: {prompt}
Topic:"""

    def predict(self, data, topics):
        topic_str = ""
        topic_list = [topic+" - "+desc for topic, desc in topics.items()]
        for i, key in enumerate(topic_list, 1):
            topic_str += (f"[{i}] {key}\n")
        
        prompts1 = [self.template1.format(topic=topic) for topic in topics]
        examples = self.model.batch_completion(prompts1)
        

        topic_examples_str = ""
        for topic, example in zip(topic_list, examples):
            topic_examples_str += f"Prompt: {example[0]}\nTopic: [{topic_list.index(topic)+1}]\n\n"

        prompts = [self.template2.format(prompt=text, topics=topic_str, examples=topic_examples_str) for text in data['input'].tolist()]
        classified_texts = self.model.batch_completion(prompts)

        topic_sz = len(topics)
        data['label'] = [extract_number(text, topic_sz) for text in classified_texts]

        return data

def extract_number(sentence, size):
    pattern = r'\d+'
    match = re.search(pattern, sentence)
    if match:
        num = int(match.group())
        if num in list(range(1, size+1)):
            return int(match.group())
    return 0