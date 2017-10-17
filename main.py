# -*- encoding: utf-8 -*-

from glob import glob
from pymongo import MongoClient
from gensim import models
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def fillMongo(db):
	"""
	gets the mongodb connection and fills the database.
	"""

	for index, file in enumerate(glob('./**/*.txt',recursive=True)):
		db.deneme.insert_one(
			{
			"id"		: index + 1,
			"filename"  : file,
			"class"		: file.split("/")[-2],
			"text"		: open(file, encoding="iso-8859-9").read().strip()
			})

def mongoDocumentsSplitted( db ):
	splitted_records = []
	for record in db["deneme"].find():
		splitted_records.extend( record["text"].split() )
	return splitted_records


def mongoDocuments2Sentences( db ):
	sentences = []
	for record in db["deneme"].find():
		sentence = models.doc2vec.LabeledSentence( words = record["text"].split(), tags = record["class"] )
		sentences.append(sentence)
	return sentences

def main():
	"""
	Main application execution. 
	"""
	db = MongoClient('localhost', 27017).test
	fillMongo(db)
	sentences = mongoDocumentsSplitted(db)
	w2v_model = models.Word2Vec(sentences, workers=4)
	w2v_model.save("word2vec.bin")

	d2v_model = models.Doc2Vec( mongoDocuments2Sentences( db ), workers=4 )
	d2v_model.save("doc2vec.bin")

	random_records = db.deneme.aggregate( [ { "$sample": {"size": 10} } ] )

	infer_vectors= []
	vectors=[]
	for record in random_records:
		vectors.append(record["text"])
		infer_vectors.append(np.array(d2v_model.infer_vector(record['text'].split(), alpha=0.025, min_alpha=0.025, steps=20)).reshape(-1, 1))

	for i in range(len(infer_vectors)-1):
		print("vector1: ", vectors[i])
		print("vector2: ", vectors[i+1])
		print("cosine: ", cosine_similarity(infer_vectors[i], infer_vectors[i+1]))  # Print out = ~0.00795774



if __name__ == "__main__":
	main()
