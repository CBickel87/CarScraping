from bs4 import BeautifulSoup
from pyshorteners import Shortener
import urllib.parse, requests, logging, emailListing

# Log file & Config options
logging.basicConfig(filename='autoTrader.log', level=logging.WARNING, format=' %(asctime)s - %(levelname)s - %(message)s\n', datefmt='%m/%d/%Y %I:%M:%S %p')

# TODO: Setup VPS and use crontab to run script daily

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
# Mileage
mileage = soup.select('span.mileage > span')

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

    # Shorten URL or catch exceptions
    try:
        shortener = Shortener('TinyurlShortener', timeout=9000)
        autotraderFile.write((shortener.short(self)) + '\n\n')
    except Exception as err:
        autotraderFile.write('ERROR: Check the log.' + '\n\n')
        logging.error(str(err) + '\n')

# For loop and zip the lists together
for a, b, c, d, e in zip(titles, titleDescrip, mileage, prices, links):
    a = a.getText()
    b = b.getText()
    c = c.getText()
    d = d.getText()
    autotraderFile.write(' '.join(((a, b,) + (' - ',) + (c, ' miles') + (' - ',) + (d,))) + '\n')
    tinyurlShort(e['href'])

# Close the listings file
autotraderFile.close()

# Email the listings
emailListing.opener('carlisting.txt')
