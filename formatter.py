from bs4 import BeautifulSoup
import html2text
import requests
import urllib.request
import re
from html.parser import HTMLParser
from os import linesep
import pudb
#pudb.set_trace()

URL = 'https://www.sec.gov/Archives/edgar/data/1405073/0001193125-17-030376.txt'




def cleanhtml(raw_html):

    soup = BeautifulSoup(raw_html, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    return text.encode('ascii', errors='ignore')
# modify HTML.
def test_html(html):
    # convert HTML to text.
    h = html2text.html2text(html)
    y = h.encode('ascii', errors='ignore')
    return y

def main_task():
    #response = urllib.request.urlopen(URL)
    #content = response.read()
    content = open('test.html').read()
    #text = test_html(content.decode('utf-8'))
    text = test_html(content)
    with open('extracted.txt', 'w') as text_file:
        text_file.write(text.decode('utf-8'))

if __name__=='__main__':
    main_task()
