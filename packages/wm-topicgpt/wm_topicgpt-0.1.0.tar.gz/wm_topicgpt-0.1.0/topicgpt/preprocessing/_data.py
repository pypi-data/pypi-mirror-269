import re
import sys
import math
import asyncio
import pandas as pd
from tqdm import tqdm
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.ai.textanalytics import PiiEntityCategory
from azure.core.credentials import AzureKeyCredential
from .. import config
from ..base import TransformerMixin


class MinMaxLengthFilter(TransformerMixin):

    def __init__(self, words_range=(0, -1)):
        self.words_range = words_range
        
    def transform(self, data):
        min_words = self.words_range[0]
        max_words = self.words_range[1] if self.words_range[1] != -1 else sys.maxsize

        if isinstance(data, list):
            rt_data = []
            for idx in range(len(data)):
                words = str(data[idx]).strip().split()
                if min_words <= len(words) <= max_words:
                    rt_data.append(data[idx])
                return rt_data
        elif isinstance(data, pd.DataFrame):
            if 'input' not in data.columns:
                raise ValueError(f"Must include `input` column in data.")
            def select_row(row):
                length = len(str(row['input']).strip().split())
                return (length >= min_words) and (length <= max_words)
            rt_data = data[data.apply(select_row, axis=1)]
            rt_data = rt_data.reset_index(drop=True)
            return rt_data
        else:
            raise ValueError("data should be in the type of `list` or `pd.DataFrame`")


class NameFilter(TransformerMixin):

    batch_size = 5

    def __init__(self):
        if config.azure_key is None:
            raise ValueError("Please set up `config.azure_key`!")
        if config.azure_endpoint is None:
            raise ValueError("Please set up `config.azure_endpoint`!")

    async def _name_filter(self, texts):
        client = TextAnalyticsClient(
            endpoint=config.azure_endpoint,
            credential=AzureKeyCredential(config.azure_key),
        )
        async with client:
            response = await client.recognize_pii_entities(documents=texts, language="en", categories_filter = [PiiEntityCategory.PERSON], verify_ssl=False)
            filtered_texts = [re.sub(r'[*]+', 'PersonName', doc.redacted_text) if not doc.is_error else "" for doc in response]
        await client.close()
        return filtered_texts

    def transform(self, data):
        if 'input' not in data.columns:
            raise ValueError(f"Must include `input` column in data.")
        texts = data['input'].tolist()

        rt_texts = []
        num_batch = math.ceil(len(texts) / self.batch_size)
        for idx in tqdm(range(0, len(texts), self.batch_size), total=num_batch):
            rt_texts.extend(asyncio.run(self._name_filter(texts[idx: idx+self.batch_size])))
    
        data['input'] = rt_texts
        return data[data['input'] != ""]