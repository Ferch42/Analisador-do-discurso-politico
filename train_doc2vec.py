import os
import pickle

from tqdm import tqdm

from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

parsed_quotes_path = "./parsed_quotes/"

corpus = []

for l in os.listdir(parsed_quotes_path):
	print(l)
	for f in tqdm(os.listdir(os.path.join(parsed_quotes_path, l))):

		c = pickle.load(open(os.path.join(parsed_quotes_path,l,f), "rb"))

		if not c:
			continue

		for d in c:
			d.update({"file":f.replace(".pkl", "")})
			d.update({"tokenized_text": word_tokenize(d["quote"], language = "portuguese")})
		
		corpus += c


documents = [TaggedDocument(d["tokenized_text"], [d["file"], d["speaker"], i]) for i,d in enumerate(corpus)]
pickle.dump(corpus, open('corpus.pkl','wb'))

print("training")
model = Doc2Vec(documents, vector_size=500, window=20, min_count=5, workers=4)

model.save("political_doc2vec")