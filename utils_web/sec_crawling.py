from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests




def get_list(ticker):

	"""
	:param ticker: ticker of a listed company, for example "APPL" for Apple
	:return: webpage link contains 10-K file
	"""

	base_url_part1 = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
	base_url_part2 = "&type=&dateb=&owner=&start="
	base_url_part3 = "&count=100&output=xml"
	href = []

	for page_number in range(0, 2000, 100):

		base_url = base_url_part1 + ticker + base_url_part2 + str(page_number) + base_url_part3
		sec_page = urlopen(base_url)
		sec_soup = BeautifulSoup(sec_page)
		filings = sec_soup.findAll('filing')

		for filing in filings:
			report_year = int(filing.datefiled.get_text()[0:4])
			if (filing.type.get_text() == "10-K") & (report_year > 2015):
				# print(filing.filinghref.get_text())
				href.append(filing.filinghref.get_text())

	return href


def get_10k_page(link):

	"""
	:param link: webpage link contains 10-K file, get from get_list function
	:return: 10-K file link
	"""

	report_page = urlopen(link)
	report_soup = BeautifulSoup(report_page)
	xbrl_file = report_soup.findAll('tr')

	for item in xbrl_file:

		try:

			if item.findAll('td')[3].get_text() == '10-K':
				# print(item.findAll('td')[2].find('a')['href'])
				target_url = 'https://www.sec.gov/' + item.findAll('td')[2].find('a')['href']
				break
		except:
			pass

	return target_url


#### The following 3 functions are forked from my teammate Max. The functions are used to analyze crwaled webpages
#### and return its business description section
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
        headers, doc = get_10k_text(url)
        if doc:  # only keep company if scraping was successful
            documents[company] = doc
            section_headers[company] = headers
            print(company)
            for header in headers:  # correct missidentified headers
                if len(header) > 100:
                    documents[company].append(header)
    return documents