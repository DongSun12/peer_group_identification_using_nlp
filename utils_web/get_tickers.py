import pandas as pd

"""
Download the ticker list from NASDAQ and save as csv.
Output filename: ./data/companyList.csv
"""

save_path = './data'

def get_and_save_tickers(save_path, save_name ='/companyList.csv'):
    
    url= "https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
    companyList = pd.read_csv(url)
    companyList.to_csv(save_path + save_name)
   

def main():

	get_tickers(save_path)


if __name__ == "__main__":

    main()