import pickle
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from gensim.models.doc2vec import Doc2Vec
from sklearn.metrics import silhouette_score
from tqdm import tqdm
from sklearn.metrics.pairwise import euclidean_distances


corpus = pickle.load(open('./corpus/corpus_L18.pkl', 'rb'))

model = Doc2Vec.load("./models/doc2vec/political_doc2vec")


features_vector = np.array([model.infer_vector(d["tokenized_text"]) for d in tqdm(corpus)])

n_clusters = 20

kmeans = KMeans(n_clusters = n_clusters)
labels = kmeans.fit_predict(features_vector)

cluster_centers = kmeans.cluster_centers_

for cluster in range(n_clusters):

	cluster_data = []
	for i in range(len(corpus)):

		if labels[i] == cluster:

			cluster_data.append({
				'feature_vector': features_vector[i],
				'text': corpus[i]
				})

	print(len(cluster_data))
	cluster_center = cluster_centers[cluster]

	cluster_distances = euclidean_distances([d['feature_vector'] for d in cluster_data], [cluster_center])
	sorted_data = np.argsort(cluster_distances.flatten())
	most_similar = [cluster_data[order] for order in sorted_data]

	print("-----------------------------------------------------------\n"*10)
	print(f"PRINTING THE MOST SIMILAR DOCUMENTS FOR CLUSTER {cluster+1}")

	for j in range(min(10, len(most_similar))):

		print(f"Document {j} : {most_similar[j]['text']['quote']}")
		print("++++++++++++++++++++++++++++++++++++++++++++++++++")



		






