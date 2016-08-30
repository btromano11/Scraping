from urllib2 import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup

#Get Website
def get_website(url):
    try:
        html = urlopen(url)
    except (URLError,HTTPError) as e:
        print e
        return None
    try:
        bsObj = BeautifulSoup(html,'html.parser')
    except AttributeError as e:
        print e
        return None
    return bsObj

