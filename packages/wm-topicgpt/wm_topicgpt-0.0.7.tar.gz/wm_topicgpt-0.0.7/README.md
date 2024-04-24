# TopicGPT package

## How to install this package?
```python
pip install wm_topicgpt==0.0.7
```

## How to use this package?

### Step 1: Set up global parameters
```python
from topicgpt import config

# For NameFilter
config.azure_key = ""
config.azure_endpoint = ""

# For GPT3.5 or GPT4 or Ada-002
config.consumer_id = ""
config.private_key_path = ""
config.mso_llm_env = ""
```

### Step 2: Load your dataset
Load your data, must be 'pandas.DataFrame' format.
```python
import pandas as pd

data_df = pd.read_csv("dataset.csv")
```

### Step 3: Run the code

```python

# Setting up some params for this approach. If you don't need some parts, just drop that part.
params = {
    # preprocessing part
    'preprocessing': {'words_range': (1, 500)},
    # name filter part
    'name_filter': {},
    # extracting keywords part
    'extract_keywords': {'llm_model': 'gpt-35-turbo', 'temperature': 0., 'batch_size': 300},
    # embedding part (must have)
    'embedding': {'model': 'bge', 'batch_size': 500, 'device': 'mps'},
    # hdbscan clustering part (must have)
    'hdbscan': {'reduced_dim': 5, 'n_neighbors': 10, 'min_cluster_percent': 0.02, 'topk': 5,
                'llm_model': 'gpt-35-turbo', 'temperature': 0.5, 'verbose': True},
}

from topicgpt.pipeline import topic_modeling_by_hdbscan

# data_df: your pd.DataFrame dataset
# text_col_name: the column name of texts in the data_df
# params: some parameters for this approach
root = topic_modeling_by_hdbscan(data=data_df, text_col_name='userInput', params=params)
```


<!-- ```python
from topicgpt.preprocessing import MinMaxLengthFilter

filter = MinMaxLengthFilter(words_range=(1, 1000))
texts = filter.transform(data)
```

To protect the privacy, this function replaces the names in the texts with word "PersonName".
```python
from topicgpt.preprocessing import NameFilter

filter = NameFilter()
texts = filter.transform(texts)
```

### Step 4: Embedding the texts
You may choose one of them to embed your texts.
```python
# Option 1: use OpenAI model
from topicgpt.walmart_llm import AdaEmbedModel
llm = AdaEmbedModel(batch_size=500)
embedding = llm.embed_documents(texts)

# Option 2: use BGE model
from topicgpt.embedding import BGEEmbedModel
# llm = BGEEmbedModel(batch_size=500, device="cpu")
llm = BGEEmbedModel(batch_size=500, device="mps")
embedding = llm.embed_documents(texts)
```

### Step 5: Build topics from texts
This function is used to generate topic taxonomy from the texts.
```python
from topicgpt.topic import HDBSCANTopicGenerator
model = HDBSCANTopicGenerator(reduced_dim=10, n_neighbors=10, min_cluster_percent=0.02, topk=5)
root = model.predict(texts, embedding)
``` -->
