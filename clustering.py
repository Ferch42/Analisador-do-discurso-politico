import pickle
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from gensim.models.doc2vec import Doc2Vec
from sklearn.metrics import silhouette_score
from tqdm import tqdm

corpus = pickle.load(open('./corpus/corpus_L18.pkl', 'rb'))

model = Doc2Vec.load("./models/doc2vec/political_doc2vec")


features_vector = np.array([model.infer_vector(d["tokenized_text"]) for d in tqdm(corpus)])


n_clusters = range(2,20)

silhouetes = []


for c in n_clusters:

	print("CLUSTERING ", c)
	average_silhouette_score = np.mean([silhouette_score(features_vector, KMeans(n_clusters = c).fit_predict(features_vector)) for _ in tqdm(range(10))])
	silhouetes.append(average_silhouette_score)

plt.plot(n_clusters, silhouetes)
plt.show()
print(silhouetes)




