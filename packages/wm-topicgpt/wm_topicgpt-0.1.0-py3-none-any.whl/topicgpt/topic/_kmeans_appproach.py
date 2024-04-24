import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances
from ..base import GeneratorMixin
from ..topic import Cluster, TopicGenerator
from ..walmart_llm import AdaEmbedModel
from ..embedding import BGEEmbedModel


class KmeansTopicGenerator(GeneratorMixin):

    def __init__(self, n_clusters_list = [], topk=5, batch_size=100, model_name="gpt-35-turbo", 
                 temperature=0.5, embed_model="bge", device="mps", embed_batch_size=300):
        self.n_clusters_list = n_clusters_list
        self.topk = topk
        self.batch_size = batch_size,
        self.topic_generator = TopicGenerator(model_name, temperature, batch_size=batch_size)
        if embed_model == "ada":
            self.embed_model = AdaEmbedModel(batch_size=embed_batch_size)
        elif embed_model == "bge":
            self.embed_model = BGEEmbedModel(batch_size=embed_batch_size, device=device)
        
    def generate_micro_clusters(self, data): 
        kmeans = KMeans(n_clusters=self.n_clusters_list[0], random_state=42, n_init="auto")
        kmeans.fit(np.array(data['embeddings'].tolist(), dtype=np.float32))
        data['label'] = kmeans.labels_
        # generate micro clusters
        clusters = []
        for label in sorted(set(kmeans.labels_)):
            cluster_data = data[data['label'] == label].reset_index(drop=True)
            
            cluster = Cluster(data=cluster_data)
            cluster.centroid = kmeans.cluster_centers_[label]
            cluster.size = len(cluster.data)
            
            dists = pairwise_distances(np.array([cluster.centroid], dtype=np.float32), np.array(cluster.data['embeddings'].tolist(), dtype=np.float32))[0]
            cluster.within_cluster_dist = np.mean(dists)
            cluster.closest = np.argsort(dists)[:self.topk]

            clusters.append(cluster)

        # generate topic and description
        responses = self.topic_generator._generate_batch_topics_and_descriptions_for_clusters(clusters)
        for cluster, response in zip(clusters, responses):
            cluster.topic = eval(response)['topic']
            cluster.description = eval(response)['description']
        return clusters
    
    def generate_higher_clusters(self, clusters, level):
        prompts = []
        for cluster in clusters:
            prompts.append(f"Topic: {cluster.topic}\nDescription: {cluster.description}")
        embeddings = self.embed_model.embed_documents(prompts)
        
        kmeans = KMeans(n_clusters=self.n_clusters_list[level], random_state=42, n_init="auto")
        kmeans.fit(np.array(embeddings, dtype=np.float32))

        higher_clusters = [Cluster() for _ in range(self.n_clusters_list[level])]
        for idx, label in enumerate(kmeans.labels_):
            higher_clusters[label].children.append(clusters[idx])
            
        for cluster in higher_clusters:
            cluster.size = sum([child.size for child in cluster.children])
            for child in cluster.children:
                child.percent = round(child.size / cluster.size, 3)
            
            cluster.keywords = []
            for child in cluster.children:
                cluster.keywords.extend(child.keywords)

        responses = self.topic_generator._generate_batch_topics_and_descriptions_for_higher_clusters(higher_clusters)
        for cluster, response in zip(higher_clusters, responses):
            cluster.topic = eval(response)['topic']
            cluster.description = eval(response)['description']
        return higher_clusters
    
    def predict(self, texts, embeddings, **params):
        clusters = []
        micro_clusters = self.generate_micro_clusters(texts, embeddings)
        clusters.append(micro_clusters)
        for idx in enumerate(self.n_clusters_list[1:], start=1):
            higher_clusters = self.generate_higher_clusters(clusters[-1], level=idx)
            clusters.append(higher_clusters)
        return clusters