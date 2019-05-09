import spacy
import re

nlp = spacy.load("en")

scrapped_documents_path = './data//scraped_docs.pickle'
cleaned_documents_save_path = './data//cleaned_docs.pickle'
tickers_save_path = './data//all_tickers.pickle'



"""
The script cleans scrapped documents and save
"""
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


def main():

    cleaned_docs = []
    all_tickers = []
    scrapped_docs = pd.read_pickle(scrapped_documents_path)

    for ticker, doc in scrapped_docs.items():

        all_tickers.append(ticker)
        cleaned_doc = clean_text(doc)
        cleaned_docs.append(cleaned_doc)
    
    pd.to_pickle(cleaned_doc, cleaned_documents_save_path)
    pd.to_pickle(all_tickers, tickers_save_path)


if __name__ == "__main__":

    main()








