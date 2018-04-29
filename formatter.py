
import requests
import urllib.request
import re
from html.parser import HTMLParser
from os import linesep
from bs4 import BeautifulSoup
import pudb
import pandas as pd
import subprocess
pudb.set_trace()

URL = 'https://www.sec.gov/Archives/edgar/data/1405073/0001193125-17-030376.txt'
ARCHIVE = 'https://www.sec.gov/Archives/'
CMD = 'w3m -dump '

SKIP_ROWS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]
FORM_TYPES = ["SC 13D","SC 13D.A"] 
URL_INDEX = "https://www.sec.gov/Archives/edgar/full-index/"

def save_to_text(file_name, txt_filename):
    '''
    save to text file
    '''
    global CMD
    file_name = file_name.split('.')[0]
    file_to_read = str(file_name+".html")
    file_to_save = str(file_name+".txt")
    cmd_to_read = CMD + str(file_name+".html") + str('>'+txt_filename)
    cmd_to_remove = "rm " + str(file_name+".html")
    ps = subprocess.Popen(cmd_to_read,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    ps = subprocess.Popen(cmd_to_remove,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    # Remove HTML File

def download_target(url=None, txt_filename=None):
    if url is None:
        url = URL
    print("Downloading")
    if txt_filename is not None:
        txt_filename = txt_filename
    download_target = requests.get(url)
    print("Writing text file")
    filename = url.split('/')[-1].split('.')[0]+".html"
    with open(filename, 'w') as test_file:
        filtered = download_target.text
        if '<HTML>' not in filtered and '<html>' not in filtered:
            filtered = filtered.replace('<TEXT>', '<PRE>')
            filtered = filtered.replace('</TEXT>', '</PRE>')
        test_file.write(filtered)
    save_to_text(filename, txt_filename)



def parse_idx_file(url):
    '''
    download idx file from url, parses and downloads inner url
    '''
    # Download idx file
    remove_idx_file()
    print("Downloading Index File ...")
    idx_file = requests.get(url)
    with open('master.idx', 'w') as test_file:
        test_file.write(idx_file.text)
    print("Download and Write Complete")
    df = pd.read_csv('master.idx', skiprows=SKIP_ROWS, sep='|')
    df = df[df['Form Type'].isin(FORM_TYPES)]
    df['file_url'] = df['Filename'].apply(lambda x: "{}{}".format(ARCHIVE, x))
    for idx, row in df.iterrows():
        filename = row['Date Filed'].replace('-','')
        filename += '_'
        filename += str(row['Form Type'])
        filename += '_edgar_data_'
        filename += str(row['CIK'])
        filename += '.txt'
        download_target(url=row['file_url'], txt_filename=filename)
    # Remove IDX File
    remove_idx_file

def remove_idx_file():
    cmd_to_remove = 'rm master.idx'
    ps = subprocess.Popen(cmd_to_remove,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]

def pull_index_files(start_year,end_year):
    for year in range(start_year,end_year):
        url = URL_INDEX + str(year) +"/"
        for qtr in ["QTR1","QTR2","QTR3","QTR4"]:
            target_url = url + qtr + "/master.idx"
            # Reads all 
            parse_idx_file(target_url)
            #print(target_url)

def main_task():
    #response = urllib.request.urlopen(URL)
    #content = response.read()
    #establish years desired
    start_year = int(input("Provide Start Year: "))
    end_year = int(input("Provide End Year (If only one year desired, provide that year.): "))
    pull_index_files(start_year, end_year+1)

if __name__=='__main__':
    main_task()
