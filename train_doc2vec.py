import os
import pickle
import gc

from tqdm import tqdm

from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument



parsed_quotes_path = "./parsed_quotes/"

corpus = []

model = None

for l in os.listdir(parsed_quotes_path):
	print(l)
	for f in tqdm(os.listdir(os.path.join(parsed_quotes_path, l))):

		c = pickle.load(open(os.path.join(parsed_quotes_path,l,f), "rb"))

		for d in c:
			d.update({"file":f.replace(".pkl", "")})
			d.update({"tokenized_text": word_tokenize(d["quote"], language = "portuguese")})
			#print(d['quote'])


		corpus += c


	documents = [TaggedDocument(d["tokenized_text"], [d["file"], d["speaker"]]) for d in corpus]
	
	print("DUMPING ...")
	pickle.dump(corpus, open(f'./corpus/corpus_{l}.pkl','wb'))
	print("TRAINING")
	
	if not model:
		model = Doc2Vec(documents, vector_size=500, window=20, min_count=5, workers=4)
	else:
		print(f"N epochs : {model.epochs}")
		model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)
	
	model.save("./models/doc2vec/political_doc2vec")
	
	corpus = []
	gc.collect()


