import pickle
import numpy as np
from sklearn.cluster import KMeans
from gensim.models.doc2vec import Doc2Vec
from sklearn.metrics import silhouette_samples, silhouette_score

corpus = pickle.load(open('corpus.pkl', 'rb'))

model = Doc2Vec.load("political_doc2vec")

