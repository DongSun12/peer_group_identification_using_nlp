import spacy
from gensim import corpora, models, similarities
import numpy as np
import re

nlp = spacy.load("en")

def clean_text(filling_list):

    """
    input:
    filling_list: a list of 10-k business descriptions crwaled from SEC websites

    return:
    text: a list of NOUN and PROPN tokens of texts, with special chars, long spaces and stopwords removed. This function
    also performs lemmatization.

    """
    text = ' '.join(filling_list).lower()
    text = re.sub(r"[^a-zA-Z.?!]", " ", text)
    text = re.sub(r' +', ' ', text)
    doc = nlp(text)

    # Use default stopwords as a baseline
    tokens = []
    for token in doc:

        if not token.is_stop and token.pos_ in {'NOUN' ,'PROPN'}:

            tokens.append(token.lemma_)

    return tokens


def get_tf_idf_simmat(docs):

    """
    :param docs: list of N list of tokens
    :return: simlarity matrix N*N
    """
    dictionary = corpora.Dictionary(docs)
    # compile corpus (vectors number of times each elements appears)
    raw_corpus = [dictionary.doc2bow(t) for t in docs]
    # similarity between corpuses
    tfidf = models.TfidfModel(raw_corpus)  # step 1 -- initialize a model
    corpus_tfidf = tfidf[raw_corpus]
    index = similarities.MatrixSimilarity(tfidf[raw_corpus])

    sims = index[corpus_tfidf]

    return sims


def get_recall_rate(sim_mat, all_industries, k=5):
    count = 0
    num = sim_mat.shape[0] - 34
    for i in range(num):

        true_industry = all_industries[i]
        no1sim = sim_mat[i, :]
        recalls_ind = no1sim.argsort()[-k - 1:][::-1][1:]
        # print(recalls_ind)
        recalls_industry = np.array(all_industries)[recalls_ind]
        # print(recalls_industry, true_industry)
        if true_industry in recalls_industry:
            count = count + 1
    print(count)
    return count / num




