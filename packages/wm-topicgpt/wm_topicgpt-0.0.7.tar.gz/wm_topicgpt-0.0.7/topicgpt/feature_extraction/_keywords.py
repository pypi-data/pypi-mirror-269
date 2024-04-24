import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from ..base import TransformerMixin
from ..walmart_llm import ChatModel


class TfidifKeywordsExtractor(TransformerMixin):

    def __init__(self, ngram_range=(1, 2), topk=10):
        self.ngram_range = ngram_range
        self.topk = topk

    def transform(self, clusters):
        # build corpus
        n_classes = len(clusters)
        corpus = [""] * n_classes
        for idx, cluster in enumerate(clusters):
            corpus[idx] += (" ".join(cluster.data['input'].tolist()))

        vectorizer = TfidfVectorizer(ngram_range=self.ngram_range, stop_words='english')
        tfidf = vectorizer.fit_transform(corpus)

        # extract keywords
        feature_names = vectorizer.get_feature_names_out()
        for idx in range(n_classes):
            tfidf_values = tfidf[idx].toarray().flatten()
            sorted_indices = tfidf_values.argsort()[::-1]
            top_keywords_indices = sorted_indices[:self.topk]
            top_keywords = [feature_names[idx] for idx in top_keywords_indices]
            clusters[idx].keywords = ", ".join(top_keywords)
        return clusters


class LlmKeywordsExtractor(TransformerMixin):

    def __init__(self, topk=10, model_name="gpt-35-turbo", temperature=0., batch_size=300):
        self.topk = topk
        self.template = """You will be given a text. This will be enclosed in triple backticks.

Please give me the keywords that are present in this text and separate them with commas.
Make sure you to only return the keywords and say nothing else. For example, don't say: 
"Here are the keywords present in the text". And give at most {topk} keywords.

Text: ```The website mentions that it only takes a couple of days to deliver but I still have not received mine.```
Keywords: deliver, a couple of days, received, website

Text: ```Machine learning (ML) is a field of study in artificial intelligence concerned with the development and study of statistical algorithms that can learn from data and generalize to unseen data, and thus perform tasks without explicit instructions```
Kywords: machine learning, artificial intelligence, statistical algorithms, data, tasks, instructions

Text: ```{text}```
Keywords:
"""
        self.model = ChatModel(model_name=model_name, temperature=temperature, batch_size=batch_size)
    
    def transform(self, data, **params):
        
        def remove_extra_keywords(keywords):
            return [",".join(str(text).strip().split(",")[:self.topk]) for text in keywords]

        if isinstance(data, pd.DataFrame):
            if 'input' not in data.columns:
                raise ValueError(f"Must include `input` column in data.")
            prompts = [self.template.format(topk=self.topk, text=text) for text in data['input'].tolist()]
            keywords = self.model.batch_completion(prompts)
            data['keywords'] = remove_extra_keywords(keywords)
            rt_data = data[data['keywords'] != ''].reset_index(drop=True)
            return rt_data
        elif isinstance(data, list):
            prompts = [self.template.format(topk=self.topk, text=text) for text in data]
            keywords = self.model.batch_completion(prompts)
            return remove_extra_keywords(keywords)
        else:
            raise ValueError("data should be in the type of `list` or `pd.DataFrame`")