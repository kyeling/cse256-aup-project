# cse256-aup-project

## Getting started
1. Create a virtual environment by running `python -m venv .venv`
2. Install dependencies with `pip install -r requirements.txt`

## Code
'code/data.py' contains all necessary functions for data collection, and is divided into 4 parts, corresponding to the steps in the Data section below. 
An online version of 'data.ipynb', compatible with/runnable in Google Colab, can be found [here](https://colab.research.google.com/drive/1CoU7CcV2cPcENGuJ1oREnwWlt1cM2XKt?usp=sharing).

## Data
The following workflow was used for collecting the data:
1. Automatically download the most up-to-date CrUX list ('current.csv') and get the urls of websites in the CrUX list.
2. Get the urls of AUPs and store them 'data/aup-urls'
    a. For the first 10k CrUX urls, run a google search on each url and perform token matching on the original vs search result urls to find an AUP that is relevant to the original website (if one exists, which is often not the case). The urls of the AUPs are split into files by CrUX rank.   
    b. To supplement, also run a google search with the query "acceptable use policy site.com" and collect as many relevant AUP urls as possible. (This method collected 222 AUP urls.)
3. Use the Wayback CDX API to query the historical versions of a given AUP url and get a list of urls containing every historical snapshot. TODO: the code functionality is writte in 'code/data.py' (see part 3 of the file), but the snapshot urls haven't been collected yet.
4. Scrape the content of the urls using beautifulsoup (html) or pypdf2 (pdfs).
   
AUPs sourced from the first 10k CrUX websites are denoted by a 4-digit index number corresponding to their position in the CrUX list. AUPs sourced from open Google Search results (first 222 relevant results) are given a 3-digit number corresponding to their position in 'data/urls/googlesearch-aups.txt'

### Current Stats
116 unique urls collected through CrUX and 222 unique urls collected through Google Search (but there is overlap between these two sets)   
91 crux AUP files and 40 Google Search AUP files