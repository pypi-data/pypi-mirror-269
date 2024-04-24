import time

hdbscan_params = {
    # preprocessing part
    'preprocessing': {'words_range': (1, 500)},
    # name filter part
    'name_filter': {},
    # extracting keywords part
    'extract_keywords': {'llm_model': 'gpt-35-turbo', 'temperature': 0., 'batch_size': 300},
    # embedding part
    'embedding': {'model': 'bge', 'batch_size': 500, 'device': 'mps'},
    # hdbscan clustering part
    'hdbscan': {'reduced_dim': 5, 'n_neighbors': 10, 'min_cluster_percent': 0.02, 'topk': 5, 
                'llm_model': 'gpt-35-turbo', 'temperature': 0.5, 'batch_size': 300, 'verbose': True},
}

kmeans_params = {
    # preprocessing part
    'preprocessing': {'words_range': (1, 500)},
    # name filter part
    'name_filter': {},
    # embedding part
    'embedding': {'model': 'bge', 'batch_size': 500, 'device': 'mps'},
    # hdbscan clustering part
    'kmeans': {'n_clusters_list': [100, 30, 5], 'topk': 5, 'llm_model': 'gpt-35-turbo', 'temperature': 0.5,
               'batch_size': 300, 'embed_model': "bge", "device": "mps", "embed_batch_size": 500,
               'ngram_range': (1, 2), 'topk_keywords': 10},
}


def topic_modeling_by_hdbscan(data, text_col_name, params=hdbscan_params):
    tt1 = time.time()
    if text_col_name not in data.columns:
        raise ValueError("`text_col_name` should be in data.columns")
    data_df = data.rename(columns={text_col_name: 'input'})
    data_df = data_df.dropna(subset=["input"])
    data_df['input'] = data_df['input'].astype(str)
    print(f"#Original data size: {len(data_df)}")

    # preprocessing
    if 'preprocessing' in params:
        print("-"*30, "Preprocessing part", "-"*30)
        t1 = time.time()
        from topicgpt.preprocessing import MinMaxLengthFilter
        filter = MinMaxLengthFilter(words_range=params['preprocessing']['words_range'])
        data_df = filter.transform(data_df)
        t2 = time.time()
        print(f"#Data size after preprocessing: {len(data_df)}, processing_time: {t2-t1:0.1f} s")


    if 'name_filter' in params:
        print("-"*30, "Name_filter part", "-"*30)
        t1 = time.time()
        from topicgpt.preprocessing import NameFilter
        filter = NameFilter()
        data_df = filter.transform(data_df)
        t2 = time.time()
        print(f"#Data size after name_filter: {len(data_df)}, preprocessing_time: {t2-t1:0.1f} s")

    if 'extract_keywords' in params:
        print("-"*30, "Extracting keywords part", "-"*30)
        t1 = time.time()
        from topicgpt.feature_extraction import LlmKeywordsExtractor
        llm = LlmKeywordsExtractor(model_name=params['extract_keywords']['llm_model'], 
                                   temperature=params['extract_keywords']['temperature'], 
                                   batch_size=params['extract_keywords']['batch_size'])
        data_df = llm.transform(data=data_df)
        t2 = time.time()
        print(f"#Data size after extracting_filter: {len(data_df)}, preprocessing_time: {t2-t1:0.1f} s")
        
    if 'embedding' in params:
        print("-"*30, "Embeddding part", "-"*30)
        t1 = time.time()
        if params['embedding']['model'] == 'ada':
            from topicgpt.walmart_llm import AdaEmbedModel
            llm = AdaEmbedModel(batch_size=params['embedding']['batch_size'])
        elif params['embedding']['model'] == 'bge':
            from topicgpt.embedding import BGEEmbedModel
            llm = BGEEmbedModel(batch_size=params['embedding']['batch_size'], device=params['embedding']['device'])
            
        embeddings = llm.embed_documents(data_df['input'].tolist())
        data_df['embeddings'] = embeddings
        t2 = time.time()
        print(f"#Data size after embedding: {len(data_df)}, preprocessing_time: {t2-t1:0.1f} s")
        
    else:
        raise ValueError("`embedding` is a neccessary part of this pipeline.")

    if 'hdbscan' in params:
        print("-"*30, "HDBSCAN clustering part", "-"*30)
        t1 = time.time()
        from topicgpt.topic import HDBSCANTopicGenerator
        model = HDBSCANTopicGenerator(reduced_dim=params['hdbscan']['reduced_dim'], 
                                      n_neighbors=params['hdbscan']['n_neighbors'], 
                                      min_cluster_percent=params['hdbscan']['min_cluster_percent'], 
                                      topk=params['hdbscan']['topk'],
                                      model_name=params['hdbscan']['llm_model'], 
                                      temperature=params['hdbscan']['temperature'], 
                                      verbose=params['hdbscan']['verbose'])
        tree_root = model.predict(data_df)
        t2 = time.time()
        print(f"#Data size after hdbscan: {len(data_df)}, preprocessing_time: {t2-t1:0.1f} s")
    else:
        raise ValueError("`hdbscan` is a neccessary part of this pipeline.")

    tt2 = time.time()
    print(f"Total processing time: {tt2-tt1:0.1f} s")
    return tree_root


def topic_modeling_by_kmeans(data, text_col_name, params=kmeans_params):
    tt1 = time.time()
    if text_col_name not in data.columns:
        raise ValueError("`text_col_name` should be in data.columns")
    data_df = data.rename(columns={text_col_name: 'input'})
    data_df = data_df.dropna(subset=["input"])
    data_df['input'] = data_df['input'].astype(str)
    print(f"#Original data size: {len(data_df)}")

    # preprocessing
    if 'preprocessing' in params:
        print("-"*30, "Preprocessing part", "-"*30)
        t1 = time.time()
        from topicgpt.preprocessing import MinMaxLengthFilter
        filter = MinMaxLengthFilter(words_range=params['preprocessing']['words_range'])
        data_df = filter.transform(data_df)
        t2 = time.time()
        print(f"#Data size after preprocessing: {len(data_df)}, processing_time: {t2-t1:0.1f} s")


    if 'name_filter' in params:
        print("-"*30, "Name_filter part", "-"*30)
        t1 = time.time()
        from topicgpt.preprocessing import NameFilter
        filter = NameFilter()
        data_df = filter.transform(data_df)
        t2 = time.time()
        print(f"#Data size after name_filter: {len(data_df)}, preprocessing_time: {t2-t1:0.1f} s")

    if 'embedding' in params:
        print("-"*30, "Embeddding part", "-"*30)
        t1 = time.time()
        if params['embedding']['model'] == 'ada':
            from topicgpt.walmart_llm import AdaEmbedModel
            llm = AdaEmbedModel(batch_size=params['embedding']['batch_size'])
        elif params['embedding']['model'] == 'bge':
            from topicgpt.embedding import BGEEmbedModel
            llm = BGEEmbedModel(batch_size=params['embedding']['batch_size'], device=params['embedding']['device'])
            
        embeddings = llm.embed_documents(data_df['input'].tolist())
        data_df['embeddings'] = embeddings
        t2 = time.time()
        print(f"#Data size after embedding: {len(data_df)}, preprocessing_time: {t2-t1:0.1f} s")
        
    else:
        raise ValueError("`embedding` is a neccessary part of this pipeline.")

    if 'kmeans' in params:
        print("-"*30, "Kmeans Clustering part", "-"*30)
        t1 = time.time()
        from topicgpt.topic import KmeansTopicGenerator
        model = KmeansTopicGenerator(n_clusters_list=params['kmeans']['n_clusters_list'], 
                                     topk=params['kmeans']['topk'], 
                                     model_name=params['kmeans']['llm_model'],
                                     batch_size=params['kmeans']['batch_size'],
                                     temperature=params['kmeans']['temperature'], 
                                     embed_model=params['kmeans']['embed_model'],
                                     device=params['kmeans']['device'], 
                                     embed_batch_size=params['kmeans']['embed_batch_size'])
        clusters = []
        microclusters = model.generate_micro_clusters(data_df)

        from topicgpt.feature_extraction import TfidifKeywordsExtractor

        extractor = TfidifKeywordsExtractor()
        clusters.append(extractor.transform(microclusters))

        for idx, _ in enumerate(params['kmeans']['n_clusters_list'][1:], start=1):
            clusters.append(model.generate_higher_clusters(clusters[-1], level=idx))
        t2 = time.time()
        print(f"#Data size after hdbscan: {len(data_df)}, preprocessing_time: {t2-t1:0.1f} s")
    else:
        raise ValueError("`hdbscan` is a neccessary part of this pipeline.")

    tt2 = time.time()
    print(f"Total processing time: {tt2-tt1:0.1f} s")
    return clusters