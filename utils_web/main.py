## This python files will run the 10-k file retreival functions to save links to a dictionary
## like {'Company ticker name': '10-k file url'}
import pandas as pd
from utils_web.sec_crawling import *
import pickle

all_data = pd.read_csv('\data\\companylist.csv')
all_syms = all_data['Symbol'] ## all ticker names
all_links = {}
for sym in all_syms:
    res = get_list(sym)
    if len(res) != 0:
        tenk_html = get_10k_page(res[0])
        all_links[sym] = tenk_html
        print(sym, tenk_html)

with open('\data\\ticker2url.pickle', 'wb') as handle:
    pickle.dump(all_links, handle, protocol=pickle.HIGHEST_PROTOCOL)
