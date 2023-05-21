import requests
import os
import gzip
import pandas as pd
import random
from googlesearch import search
from tqdm import tqdm
import csv 
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from io import BytesIO
from Crypto.Cipher import AES

random.seed(0)


### PART 1: Initial Data Collection ###

# download crux dataset (if needed) and read into a dataframe
def get_dataset(fname='current.csv'):
  os.chdir('../data')
  if not os.path.isfile(fname):
    print('downloading data...')
    url = 'https://raw.githubusercontent.com/zakird/crux-top-lists/main/data/global/current.csv.gz'
    response = requests.get(url)

    # write download contents to 'current.csv.gz'
    gzip.open(f'{fname}.gz', 'wb').write(response.content)
    # unzip to get 'current.csv'
    os.system(f'gzip -d {fname}.gz')

  try:
    df = pd.read_csv(fname, compression='gzip')
  except:
    df = pd.read_csv(fname)
  
  os.chdir('../code')
  return df

# returns a new dataframe of only websites with specified rank
def rank_filter(df, rank):
  return df[df['rank'] == rank]

# extract a random sample of n urls
def get_sample(df, n, save=None):
  N = len(df) # population size
  n = 100     # sample size
  sample_idxs = random.sample(range(N), n)
  sample_urls = [df['origin'].iloc[i] for i in sample_idxs]

  # if save parameter is provided, save urls to specified output file
  if save:
    open(save, 'w').write('\n'.join(sample_urls))
  return sample_urls


### PART 2: Searching for AUPs ###

# try removing trivial components of url
# for simplicity, any component consisting of 3 or fewer characters
def nontrivial_cmp(orig_url, aup_url): # condition function can only take one argument
  len3 = lambda s : len(s) > 3
  len3_and_orig = lambda s: len3(s) and s in orig_parts

  orig_parts = list(filter(len3, orig_url.replace('https://', '').split('.')))
  aup_parts = list(filter(len3_and_orig, aup_url.replace('https://', '').split('.')))
  return bool(aup_parts) and ('aup' in aup_url or 'acceptable-use-policy' in aup_url)

# take top google search results and see if any contain an aup
# search-width: n
def get_search_results(url, n=5):
  search_str = f'{url} acceptable use policy'
  wt = random.uniform(30, 60)
  for result in search(search_str, num=n, stop=n, pause=wt): # NOTE removing pause may lead to 429 Too Many Requests
    if nontrivial_cmp(url, result):
      return result
  return None

# get aup's in the bucket specified by a given rank
# don't worry about duplicates here, remove them later in a dataframe
def get_aups_in_bucket(partial_df, batch=None):
  aups = []
  rank = partial_df.iloc[0]['rank']
  fname = f"../data/urls/aups-rank{rank}{'-batch' + str(batch) if batch else ''}.csv"

  # create a new file to store aup urls
  with open(fname, 'w') as f:
    w = csv.writer(f)
    w.writerow(['index', 'aup'])

  for i in tqdm(range(len(partial_df))):
    row = partial_df.iloc[i]
    idx = row['index']
    url = row['origin']
       
    # run google search for relevant aup
    result = get_search_results(url)
    if result:
      aups.append((idx, result))
    
    # print progress update and write to file after every 1000 searches
    if (i+1) % 1000 == 0:
      print(f' found {len(aups)} new aups')
      with open(fname, 'a') as f:
        w = csv.writer(f)
        w.writerows(aups)
      aups = []


### PART 3: Longitudinal Data ###

# query the Wayback Availability JSON API
# limitation: only returns a single snapshot (most recent or closest to query timestamp)
def query_wayback(url):
  query = f'https://archive.org/wayback/available?url={url}'
  response = requests.get(query)
  return response.json()

# query the Wayback CDX Server API
# this provides more complex support, including returning all available snapshots
def query_cdx(url):
  query = f'http://web.archive.org/cdx/search/cdx?url={url}&fl=timestamp,digest,length,original&output=json'
  response = requests.get(query)
  return response.json()

# get urls of all wayback machine snapshots from a current url
def get_snapshots(url):
  cdx = query_cdx(url)[1:] # skip header

  # c[0] is timestamp and c[3] is original url
  snapshots = [f'http://web.archive.org/web/{c[0]}/{c[3]}' for c in cdx]
  timestamps = [c[0] for c in cdx]
  return snapshots, timestamps


### PART 4: Scraping Content from URLs ###

def get_aup_content(aup_url, index, timestamp='current'):
  response = requests.get(aup_url)
  padded_index = str(index).zfill(6)
  text = ""

  # if not response.ok:
  #   print(f'get request failed with status code {response.status_code} on {aup_url}')
  
  # if AUP is a webpage, remove extraneous html elements and get text from remaining elements
  if 'text/html' in response.headers['Content-Type']:
    soup = BeautifulSoup(response.content)
    elems_to_rm = ['style', 'script', 'head', 'title', 'nav', 'heater', 'footer', 'button', 'a']
    for s in soup(elems_to_rm):
      s.extract()
    text = soup.get_text()

  # if AUP is a pdf, read bytes in as pdf and get text from each page of pdf
  elif 'pdf' in response.headers['Content-Type']:
    pdf_bytes = BytesIO(response.content)
    pdf = PdfReader(pdf_bytes)
    for page in pdf.pages:
      text += page.extract_text()
    
  else:
    print(f"urecognized content type {response.headers['Content-Type']} for {aup_url}")
    # TODO return error

  # strip leading/trailing space and drop blank lines
  lines = (line.strip() for line in text.splitlines())
  cleantext = '\n'.join(line for line in lines if line)

  # write to file
  fname = f'../data/aups/{padded_index}-{timestamp}.txt'
  open(fname, 'w').write(cleantext)
  # try:
  #   open(fname, 'w').write(cleantext)
  # except:
  #   print(f'unable to scrape contents of {aup_url}')


if '__name__' == '__main__':
  pass