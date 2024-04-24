import tiktoken
from ..base import TransformerMixin
from ..walmart_llm import ChatModel
from ..topic import Cluster


class TopicGenerator(TransformerMixin):

    def __init__(self, model_name="gpt-35-turbo", temperature=0.5, batch_size=100):
        self.model_name = model_name
        self.model = ChatModel(model_name=model_name, temperature=temperature, batch_size=batch_size)
        self.encoding = tiktoken.encoding_for_model(model_name=model_name)

    def _generate_topic_and_description_for_cluster(self, cluster):
        prefix = """You are a good editor. Given some requirements and sentences, you need to summarize the main topic of those sentences and give a simple description of this topic according to those requirements. 
        Here are some requirements you MUST follow:
        1. The topic should be less than 10 words.
        2. The description should be less than 30 words.

        Here are the sentences you need to consider all:
        {user_input}
        """
        
        suffix = """The output should be in the json format:
        {"topic": <summarize the main topic of those sentences>, "description": <output a discription for this topic>}
        """
        user_input = ""
        for i, text in enumerate([cluster.data['input'][idx] for idx in cluster.closest], start=1):
            if (self.model_name == "gpt-35-turbo" and len(self.encoding.encode(user_input)) > 3000) or \
               (self.model_name == "gpt-4" and len(self.encoding.encode(user_input)) > 7000):
                break
            user_input += f"sentence {i}: {str(text).strip()}\n"
        prompt = prefix.format(user_input=user_input) + suffix
        try:
            return self.model.retry_json_completeion(prompt, keys=['topic', 'description'])
        except Exception as e:
            print(f"Exception: {e}")
            return "{'topic': 'OpenAI policy violation', 'description': ''}"

    def _generate_batch_topics_and_descriptions_for_clusters(self, clusters):
        prefix = """Provide a concise topic and a corresponding description of the triple backquoted sentences.
```{user_input}```
"""
        suffix = """
The output should be in the json format:
{"topic": <summarize the topic of those sentences>, "description": <output a discription for this topic at most 50 words>}"""

        prompts = []
        for cluster in clusters:
            user_input = ""
            for i, text in enumerate([cluster.data['input'][idx] for idx in cluster.closest], start=1):
                if (self.model_name == "gpt-35-turbo" and len(self.encoding.encode(user_input)) > 3000) or \
                   (self.model_name == "gpt-4" and len(self.encoding.encode(user_input)) > 7000):
                    break
                user_input += f"sentence {i}: {str(text).strip()}\n"
                # user_input += f"""sentence {i}: ""{str(text).strip()}"""""
            prompts.append(prefix.format(user_input=user_input)+suffix)
        
        responses = self.model.batch_completion(prompts) 
        for idx, (prompt, response) in enumerate(zip(prompts, responses)):
            try:
                topic = eval(response)['topic']
                description = eval(response)['description']
            except Exception as e:
                try:
                    responses[idx] = self.model.retry_json_completeion(prompt, keys=['topic', 'description'])
                except:
                    responses[idx] = "{'topic': 'OpenAI policy violation or Not JSON format', 'description': 'violation'}"
        return responses

    def _generate_batch_topics_and_descriptions_for_higher_clusters(self, clusters):
        prefix = """You're a good editor. Given several subtopics, descriptions and keywords, your task is to summarize a topic that try to encompass most subtopics and provide a description of that topic according to following requirments.

        Here are some requirements that you must adhere to:
        1. The topic MUST be less than 10 words.
        2. The description MUST be less than 50 words.
        3. DON'T output person's name.

        Here are the subtopics, descriptions and keywords:
        """
        suffix = """Output the topic and description in the json format as below:
        {"topic": [output summarized topic here], "description": [output detailed description here]}"""

        prompts = []
        for cluster in clusters:
            lower_topics_str = ""
            for child in cluster.children:
                lower_topics_str += f"Subtopic: {child.topic}\n"
                lower_topics_str += f"Description: {child.description}\n"    
            prompts.append(prefix + lower_topics_str + suffix)
        
        responses = self.model.batch_completion(prompts) 
        for idx, (prompt, response) in enumerate(zip(prompts, responses)):
            try:
                topic = eval(response)['topic']
                description = eval(response)['description']
            except Exception as e:
                try:
                    responses[idx] = self.model.retry_json_completeion(prompt, keys=['topic', 'description'])
                except:
                    responses[idx] = "{'topic': 'OpenAI policy violation or Not JSON format', 'description': 'violation'}"
        return responses

    def transform(self, obj):
        if isinstance(obj, list):
            return self._generate_batch_topics_and_descriptions_for_clusters(obj)
        elif isinstance(obj, Cluster):
            return self._generate_topic_and_description_for_cluster(obj)
    
