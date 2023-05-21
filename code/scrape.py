from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# import chromedriver_binary

options = Options()
options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

search_str = 'acceptable use policy'
driver.get(f"https://www.google.com/search?q={search_str}")

soup = BeautifulSoup(driver.page_source, 'html.parser')

search = soup.find_all('div', class_="yuRUbf")
for h in search:
    print(h.a.get('href'))

