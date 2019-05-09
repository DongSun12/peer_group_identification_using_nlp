import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter


companyList_path = './data/companyList.csv'
urls_save_path = './data/ticker2url.pickle'
cleaned_docs_path = './data/cleaned_docs.pkl'
nclusters = 100 # number of industry clusters
topk = 10 #top k frequent words for each industry clusters



all_links = pd.read_pickle(urls_save_path)
all_cleaned_text = pd.read_pickle(cleaned_docs_path)
company_list = pd.read_csv(companyList_path)

def identity_tokenizer(text):
    return text

def main():

	#Build TF-IDF matrix
	tfidf = TfidfVectorizer(tokenizer=identity_tokenizer, stop_words='english', lowercase=False)
	tfidf.fit(all_cleaned_text)
	tf_idf_matrix = tfidf.transform(all_cleaned_text)

	#clustering algo
	print('Fitting k means model..')
	np.random.seed(42)
	kMeans = KMeans(nclusters, init='k-means++')
	kMeans.fit(tf_idf_matrix)

	# Get top 5 clusters with most companies
	predictions = kMeans.predict(tf_idf_matrix)
	pred_counts = Counter(predictions)
	top5_clusters = sorted(pred_counts, key=pred_counts.get, reverse=True)[:5]

	# Get the most frequent words in top5 clusters
	cluster2texts = {}
	for i, cluster_id in enumerate(top5_clusters):
	    top_company_texts = []
	    topcompany_list = np.where(predictions == top5_clusters[i])[0]
	    for topcompany_id in topcompany_list:
	        top_company_texts = top_company_texts + all_cleaned_text[topcompany_id]
	    
	    word_counts = Counter(top_company_texts)
	    cluster2texts[cluster_id] = sorted(word_counts, key=word_counts.get, reverse=True)[0:10]
	    
	for k,v in cluster2texts.items():

		print('For cluster number {}'.format(k), 'the top 10 most seen words are:',v)


if __name__ == '__main__':
	main()










