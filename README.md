# Peer Group Identification Using NLP
Group Project for 'Text-Based Nonobvious Peer Group Identification'

## Overview

In this project, we will use web crawling and text parsing algorithms to construct a database of business descriptions from 10-K annual filings from the SEC Edgar website. We will use textual analysis on extracted business sections to identify peer groups that share non-obvious economic links.

## Proposed Methodology

1. Data Collection

    1.1 Download a ticker list contains the details of public companies
    
    1.2 Get all the urls of 10-K fills from SEC Edgar website linked to the tickers 

    1.3 Crawl the business description sections 10-K annual filings from the urls obtained using BeautifulSoup
    
    1.4 Download prices for the company obtained
    
2. Text Modelling
    
    2.1 Unify word format: Remove special characters, punctuations & stop words, perform lemmatization & tokenization etc.
    
    2.2 In our case keep only nouns and pronouns because we are investigating company products and activities
    
    2.3 Perform clustering on the text representation of company profiles, some suggested clustering methods are:
    
        2.3.1 K-means over tf-idf transformed matrix
        
        2.3.2 Spectral clustering over cosine similarity matrix of tf-idf matrix
        
        2.3.2 LDA over raw bag-of-words matrix
        
    2.4 Investigate into the advantages of text clustering models over traditional SIC/NASDAQ industry classification rules. For example:
    
        2.4.1 Can the text clustering models capture within-industry heterogeneity?
        
        2.4.2 Can the text clustering models capture product and industry change?
        
        2.4.3 Can the text clustering models capture cross-industry relatedness?

3. Test Text-based Industry Momentum

        3.1 Construct industry momentum factors using the text-based industry clusters in Step 2
        
        3.2 Test the following hypothesis:
            
            3.2.1 Industry momentum arises from underreaction to shocks to groups of peer ﬁrms with less–visible economic links.
            
            3.2.2 Past returns of less visible industry peers are stronger than the past returns of highly visible peers in simultaneous regressions predicting future returns. 
            Momentum proﬁts from less visible peer shocks should also be economically larger than shocks to highly visible peers.


## Current Progress

### 1. Data collection

#### 1.1 Download the ticker list from [NASDAQ](http://www.nasdaq.com/screening/companies-by-industry.aspx)
```bash
$ ./utils_web/get_tickers.py
```
#### 1.2 Get all the urls of 10-K fills from SEC Edgar website linked to the tickers
At this moment, we only get urls in year 2018. An example of 10-k file will be [APPLE](https://www.sec.gov/Archives/edgar/data/320193/000119312515356351/d17062d10k.htm)
```bash
$ ./utils_web/get_urls.py
```
#### 1.3 Crawl the business description sections 10-K annual filings from the urls obtained using BeautifulSoup
Code made from my teammate Max at https://github.com/maxlamberti At this moment, the crawler can not cover all companies in the list.
```bash
$ ./utils_web/get_business_desc.py
```
#### 1.4 TBD

### 2. Text Modelling

#### 2.1&2 Unify word format: Remove special characters, punctuations & stop words, perform lemmatization & tokenization etc.
```bash
$ ./utils_nlp/text_processing.py
```
#### 2.3 Perform K Means clustering on the tf-idf representation of company profiles
```bash
$ ./utils_nlp/kmeans_industry_clustering.py
```
We can select top 5 largest clusters and print the most frequent words. Some sample results are:
```
For cluster number 31 the top 10 most seen words are: ['product', 'drug', 'fda', 'trial', 'patent', 'approval', 'patient', 'development', 'state', 'study']
For cluster number 74 the top 10 most seen words are: ['bank', 'capital', 'company', 'loan', 'institution', 'banking', 'act', 'asset', 'risk', 'regulation']
For cluster number 37 the top 10 most seen words are: ['customer', 'service', 'product', 'solution', 'software', 'datum', 'business', 'technology', 'market', 'application']
For cluster number 40 the top 10 most seen words are: ['loan', 'bank', 'company', 'asset', 'interest', 'december', 'capital', 'rate', 'year', 'security']
For cluster number 50 the top 10 most seen words are: ['company', 'product', 'year', 'customer', 'stock', 'sale', 'tax', 'share', 'revenue', 'december']

We can see the top cluster seems to be a medical company group. 
```
Because currently we have only ~600 companies in our dataset and the cluster number is large (100), we are not able to perform
a systematic investigation to evaluate how the text clustering algorithm works. The topic priority is to improve the performance
of web parsing algorithms - For example including more human intervention for html file parsing. 


## References:

1. Hoberg, G. & Phillips, G. M. Text-based industry momentum (2017) 
2. Hoberg, G. & Phillips, G. M. Text-based network industries and endogenous product differentiation (2016)



      




    
      
    
    
 
