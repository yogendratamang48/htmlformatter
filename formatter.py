from bs4 import BeautifulSoup, ModifyHTML
import html2text
import requests
import urllib.request
import re
from html.parser import HTMLParser
from os import linesep
import pudb
pudb.set_trace()

URL = 'https://www.sec.gov/Archives/edgar/data/1405073/0001193125-17-030376.txt'




def cleanhtml(raw_html):

    soup = BeautifulSoup(raw_html, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    return text.encode('ascii', errors='ignore')
# modify HTML.
def test_html():
    html = open("test.html").read()
    html = ModifyHTML(html, "html5lib") #BeautifulSoup.
    html.shift_links() #rewrite links as in requirements, above.
    html.remove_images() #remove images as in requirements.
    html = html.raw() #back to string.
     
    # convert HTML to text.
    h2t = HTMLToText()
    plain = h2t.text(html, is_raw=True)
    print(plain)
def main_task():
    response = urllib.request.urlopen(URL)
    content = response.read()
    text = cleanhtml(content.decode('utf-8'))
    text = HtmlTool.to_nice_text(text)
    with open('extracted.txt', 'w') as text_file:
        text_file.write(text)

if __name__=='__main__':
    test_html()
