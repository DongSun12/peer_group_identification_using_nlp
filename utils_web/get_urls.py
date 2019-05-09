## This python files will run the 10-k file retreival functions to save links to a dictionary
## like {'Company ticker name': '10-k file url'}
import pandas as pd
import pickle
from urllib.request import urlopen
from bs4 import BeautifulSoup

companylist_path = './data/companylist.csv'
urls_save_path = './data//ticker2url.pickle'

def get_list(ticker):


	"""
	:param ticker: ticker of a listed company, for example "AAPL" for Apple
	:return: webpage link contains 10-K file
	"""
	

	base_url_part1 = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
	base_url_part2 = "&type=&dateb=&owner=&start="
	base_url_part3 = "&count=100&output=xml"
	href = []

	for page_number in range(0, 200, 100):

		base_url = base_url_part1 + ticker + base_url_part2 + str(page_number) + base_url_part3
		sec_page = urlopen(base_url)
		sec_soup = BeautifulSoup(sec_page)
		filings = sec_soup.findAll('filing')

		for filing in filings:
			report_year = int(filing.datefiled.get_text()[0:4])
			if (filing.type.get_text() == "10-K") & (report_year > 2017):
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


def main():

	all_data = pd.read_csv(companylist_path)
	all_syms = all_data['Symbol'] ## all ticker names
	all_links = {}
	for sym in all_syms:
	    res = get_list(sym)
	    if len(res) != 0:
	        tenk_html = get_10k_page(res[0])
	        all_links[sym] = tenk_html
	        print(sym, tenk_html)

	with open(urls_save_path, 'wb') as handle:
	    pickle.dump(all_links, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':

	main()
