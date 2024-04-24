import numpy as np
from collections import deque
from umap import UMAP
from sklearn.cluster import HDBSCAN
from sklearn.metrics.pairwise import pairwise_distances
from ..base import GeneratorMixin
from ._cluster_base import Cluster
from ..topic import TopicGenerator
    

class HDBSCANTopicGenerator(GeneratorMixin):

    def __init__(self, reduced_dim, n_neighbors, min_cluster_percent, topk=5, 
                 model_name="gpt-35-turbo", temperature=0.5, verbose=True):
        self.reduced_dim = reduced_dim
        self.n_neighbors = n_neighbors
        self.min_cluster_percent = min_cluster_percent
        self.topk = topk
        self.verbose = verbose
        self.nodes = 1
        self.topic_generator = TopicGenerator(model_name, temperature)

    def _dfs_build_clusters(self, root, n_neighbors, tier):
        if self.verbose:
            print("\t" * tier, "tier:", tier, "#data:", len(root.data), "n_neighbors:", n_neighbors)

        reducer = UMAP(n_neighbors=5, n_components=self.reduced_dim, metric='cosine')
        reduced_embeddings = reducer.fit_transform(np.array(root.data['embeddings'].tolist(), dtype=np.float32))
        
        cluster = HDBSCAN(min_cluster_size=self.min_cluster_size, min_samples=self.n_neighbors, n_jobs=-1)
        cluster.fit(reduced_embeddings)
        root.data['label'] = cluster.labels_
        
        for label in sorted(set(cluster.labels_)):
            cluster_data = root.data[root.data['label'] == label].reset_index(drop=True)
            if self.verbose:
                print("\t" * tier, "cluster label:", label, "#data:", len(cluster_data))

            if len(cluster_data) <= self.min_cluster_size:
                root.children.append(Cluster(data=cluster_data))
            else:
                next_neighbors = min(int(n_neighbors // 2), len(cluster_data))
                if next_neighbors < 2:
                    root.children.append(Cluster(data=cluster_data))
                else:
                    sub_root = self._dfs_build_clusters(Cluster(data=cluster_data), next_neighbors, tier+1)
                    root.children.append(sub_root.children[0] if len(sub_root.children) == 1 else sub_root)
        return root.children[0] if len(root.children) == 1 else root

    def build_cluster_tree(self, data):
        self.min_cluster_size = int(self.min_cluster_percent * len(data))
        root = Cluster(data=data)
        root = self._dfs_build_clusters(root, self.n_neighbors, tier=0)
        return root
        
    def _tree_traversal(self, root):
        if root.size is None:
            root.size = len(root.data)
        if root.percent is None:
            root.percent = 1.

        if root.centroid is None:
            root.centroid = np.mean(np.array(root.data['embeddings'].tolist(), dtype=np.float32), axis=0)
        dists = pairwise_distances(np.array([root.centroid], dtype=np.float32), np.array(root.data['embeddings'].tolist(), dtype=np.float32))[0]
        root.within_cluster_dist = np.mean(dists)
        root.closest = np.argsort(dists)[:self.topk]
        response = self.topic_generator.transform(root)
        root.topic = eval(response)['topic']
        root.description = eval(response)['description']

        for child in root.children:
            child.size = len(child.data)
            child.percent = round(child.size / root.size, 3)
            self._tree_traversal(child)

    def fill_cluster_tree(self, root):
        self._tree_traversal(root)

    def plot_cluster_tree(self, root, last=True, header=''):
        elbow = "└────"
        pipe = "│  "
        tee = "├────"
        blank = "   "
        print(f"{header}{elbow if last else tee} {root.topic} - {root.description} ({root.size} | {root.percent*100:.1f}%)")
        
        child_size = len(root.children)
        self.nodes += child_size
        if child_size > 0:
            for i, c in enumerate(root.children):
                self.plot_cluster_tree(c, header=header + (blank if last else pipe), last=i == child_size - 1)

    def predict(self, data):
        root = self.build_cluster_tree(data)
        self.fill_cluster_tree(root)
        if self.verbose:
            self.plot_cluster_tree(root)
        return root
    
    # def save_to_csv(self, root, save_file="topics.csv"):
    #     results = root.data.copy(deep=True)
        
    #     queue = deque([])
    #     queue.append(root)
    #     level = -1
    #     while queue:
    #         level += 1
    #         level_size = len(queue)
    #         for _ in range(level_size):
    #             node = queue.popleft()

    #             for item in node.data:
    #                 topic_name = "Topic-" + str(level)
    #                 desc_name = "Description-" + str(level)
    #                 condition = results['unique_request_id'] == item['unique_request_id']
    #                 results.loc[condition, topic_name] = item.topic
    #                 results.loc[condition, desc_name] = item.description

    #             for node in node.children:
    #                 queue.append(node)
    #     results = results.drop(columns=['Topic-0', 'Description-0'])
    #     results.to_csv(save_file, index=False)