from bs4 import BeautifulSoup
from pyshorteners import Shortener
import urllib.parse, requests, logging

# Log file & Config options
logging.basicConfig(filename='autoTrader.log', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# TODO: Create script to email file contents of car listings
# TODO: Figure out & fix Tinyurl HTTP timeout issue

url = 'An Autotrader URL'
res = requests.get(url,  headers={'User-Agent': 'Mozilla/5.0'})
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')

# Find all links to vehicles
links = soup.select('#j_id_1_bj-j_id_1_2tv-search-results-main-panel > div > a')
# Find price for each vehicle
prices = soup.select('.price.atcui-clearfix > h4 > span')
# Find titles for each vehicle
titles = soup.select('span.atcui-truncate.ymm > span')
titleDescrip = soup.select('span.trim')

# OPEN FILE
autotraderFile = open('carlisting.txt', 'w')

# Shorten URLs using pyshorteners module via TinyURL
def tinyurlShort(self):
    # Determine if URL is absolute or relative
    tof = bool(urllib.parse.urlparse(self).netloc)
    if tof is True:
        return(self)
    else:
        self = (urllib.parse.urljoin('http://www.autotrader.com/', self))
    autotraderFile.write(self + '\n')

    # Catch: Timeout for server to respond
    try:
        requests.get(self, timeout=10.0)
        shortener = Shortener('TinyurlShortener')
        autotraderFile.write((shortener.short(self)) + '\n\n')
    except Exception as e:
        autotraderFile.write('ERROR: Check the log.' + '\n\n')
        logging.error(str(e) + '\n')

# For loop and zip the lists together
for a, b, c, d in zip(titles, titleDescrip, prices, links):
    a = a.getText()
    b = b.getText()
    c = c.getText()
    autotraderFile.write(' '.join(((a, b,) + (' - ',) + (c,))) + '\n')
    tinyurlShort(d['href'])

# Close File
autotraderFile.close()
