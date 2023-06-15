# cse256-aup-project
For SP23 CSE 256 final project. Group Members: Katherin Izhikevich, Kyeling Ong, Siwei (David) Huang, and Jieru (Riley) Bai.

## Getting started
1. Create a virtual environment by running `python -m venv .venv`
2. Install dependencies with `pip install -r requirements.txt`

## Code
### Code for data collection
'code/data-collection/data.py' contains all necessary functions for data collection, and is divided into 4 parts, corresponding to the steps in the Data section below. Examples on how to use each function in data.py and provided in the runnable notebook 'data-example-usage.ipynb'.

### Code for data analysis
The 'code/analysis/' directory is divided into three types of analysis:
1. Longitudinal analysis: analyzing how AUPs within a company changed over the decade 2013-2023
2. Statistical methods: using Latent Dirichlet Allocation (LDA), Latent Semantic Indexing (LSI), and K-Means to perform topic modeling and clustering of AUPs
3. Theme extraction: using GPT-3 to summarize documents and extract common disallows


## Data
### Collection process
The following workflow was used for collecting the data:
1. Automatically download the most up-to-date CrUX list ('current.csv') and get the urls of websites in the CrUX list.
2. Get the urls of AUPs and store them 'data/aup-urls'   
a. For the first 10k CrUX urls, run a google search on each url and perform token matching on the original vs search result urls to find an AUP that is relevant to the original website (if one exists, which is often not the case). The urls of the AUPs are split into files by CrUX rank.      
b. To supplement, also run a google search with the query "acceptable use policy site.com" and collect as many relevant AUP urls as possible. (This method collected 222 AUP urls.)   

3. Use the Wayback CDX API to query the historical versions of a given AUP url and get a list of urls containing every historical snapshot. TODO: the code functionality is writte in 'code/data.py' (see part 3 of the file), but the snapshot urls haven't been collected yet.
4. Scrape the content of the urls using beautifulsoup (html) or pypdf2 (pdfs).
   
AUPs sourced from the first 10k CrUX websites are denoted by a 4-digit index number corresponding to their position in the CrUX list. AUPs sourced from open Google Search results (first 222 relevant results) are given a 3-digit number corresponding to their position in 'data/urls/googlesearch-aups.txt'.   

### Removed data
Errors from urls that could not be scraped are written to 'data/removed_data/log.txt'. Urls that were scraped but removed from the dataset for a variety of reasons are recorded in 'data/removed_data/removed_reasons.csv'.

### Final data
The final data is contained in 'data/final_data/' separated into three folders based on source.
