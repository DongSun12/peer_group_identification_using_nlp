#### The following 3 functions are forked from my teammate Max. The functions are used to analyze crwaled webpages
#### and return its business description section
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests

urls_save_path = './data//ticker2url.pickle'
doc_save_path = './data//scraped_docs.pickle'

def convert_attr_to_dict(attr):
	"""Convert HTML text attributes to python dict.

	Parameters
	----------
	attr : str
		Example: "font-family:Helvetica,sans-serif;font-size:11pt;font-weight:bold;"

	Returns
	-------
	dict
		Example {"font-family": "Helvetica, sans-serif", ...}
	"""

	result = dict()
	attr = attr.split(';')
	attrlist = [a.split(':') for a in attr]
	for pair in attrlist:
		if len(pair) == 2:
			key = pair[0]
			value = pair[1]
			result[key] = value

	return result

def get_10k_text(url):
	"""Scrape relevant text from a 10-k document in the SEC Edgar database.

	Parameters
	----------
	url : str
		URL pointing to the 10-k document in HTML format.

	Returns
	-------
	headers : list
		A list of the headers of the recorded sections.
	text : list
		A list of recorded sections from the relevant parts of the document.
	"""

	rawdoc = BeautifulSoup(requests.get(url).content, 'html.parser')

	headers = []
	text = []
	start_recording = False  # record headers between business & risk factors section
	for data in rawdoc.html.body:
		try:
			attributes = convert_attr_to_dict(data.find('font')['style'])
			is_header = attributes.get('font-weight') == 'bold'  # recognize bold text as header
			if is_header:
				if 'business' in data.text.lower():  # start of relevant section
					start_recording = True
				if 'risk factors' in data.text.lower():  # end of relevant section
					break
				if start_recording:
					headers.append(data.text)
			else:  # assume text is paragraph section
				if start_recording:  # record text
					text.append(data.text)
		except:  # cheeky too broad catch all -> we are going to filter out poorly scraped data later
			continue

	return headers, text


def scrape_edgar(urls):
    documents = {}
    section_headers = {}
    for company, url in tqdm(urls.items()):
    	try:
	        headers, doc = get_10k_text(url)
	        if doc:  # only keep company if scraping was successful
	            documents[company] = doc
	            section_headers[company] = headers
	            print(company)
	            for header in headers:  # correct missidentified headers
	                if len(header) > 100:
	                    documents[company].append(header)

     	except:
     		pass

    return documents



def main():

	urls = pd.read_pickle(urls_save_path)
	scrapped_documents = scrape_edgar(urls)
	pd.to_pickle(scrapped_documents, doc_save_path)


if __name__ == "__main__":

    main()



