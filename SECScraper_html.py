#
#
#
#
import requests
import urllib
import urllib.request
import os
import html
import html2text
import re
from bs4 import BeautifulSoup
import pudb
pudb.set_trace()

#set global vars here
#file_loc = "E:\\sec"
file_loc = "/home/ytamang/Repo/sec"
URL_INDEX = "https://www.sec.gov/Archives/edgar/full-index/"

undesired_forms = ["3","4","5","1-E","2-E","24F-2","N-1A","N-2",
"N-3","N-4","N-5","N-6","N-6EI-1","N-6F","N-8A","N-8B-2","N-8B-4","N-8F",
"N-14","N-17D-1","N-17f-1","N-17f-2","N-18f-1","N-23c-3","N-27D-1","N-54A",
"N-54C","N-CEN","N-CR","N-CSR","N-MFP","N-PX","N-Q","N-SAR","ADV","ADV_E",
"ADV-H","ADV-NR","ADV-W","PF","BD","BD-N","BDW","SBSE-BD","TA-1","TA-2",
"TA-W"]


# download and save .txt file
def download_raw_text(url_rename):
    #os.makedirs(file_loc+"\\"+url_rename[2]+"\\"+url_rename[3],exist_ok=True)
    os.makedirs(file_loc+"/"+url_rename[2]+"/"+url_rename[3],exist_ok=True)
    #download_target = urllib.request.urlopen("https://www.sec.gov/Archives/"+url_rename[0]).readlines()
    download_target = requests.get("https://www.sec.gov/Archives/"+url_rename[0])
    f_text = ""
    #for line in download_target:
        #f_text = f_text + line.decode('iso8859_2')
        #soup=BeautifulSoup(line)
        #f_text = f_text + line.decode('iso8859_2')
    soup=BeautifulSoup(download_target.text, 'html.parser')
    #f_text=soup.get_text()
    #text1=soup.find_all(text=True)
    #text2=html2text.HTML2Text()
    text1=html2text.HTML2Text()
    text1.ignore_links = True
    f_text=text1.handle(soup.prettify())
        #f_text1 = html.unescape(f_text)
        #text_maker = html2text.HTML2Text()
        #f_text=text_maker.handle(f_text)
    #soup = BS(download_target, 'html.parser')
    #f_text=soup.findall(text=True)
    #for i in soup.stripped_strings:
        #f_text = repr(i)
    #f_text=soup.get_text()
    text_file = open(file_loc+"/"+url_rename[2]+"/"+url_rename[3]+"/"+url_rename[1]+".txt","w")
    #f_text1=BS(download_target)
    #f_text2=f_text1.get_text()
    #text_file.write(str(f_text.encode('ascii', errors='ignore')).replace("\\n", "\r\n\r\n").replace("\n", "\r\n"))
    text_file.write(str(f_text.encode('ascii', errors='ignore')).replace("\\n", "\r\n").replace("\n", "\r\n").replace("\\t", "\t"))
    #text_file.write(str(f_text.encode('ascii', errors='ignore')))
    #text_file.write(str((f_text.encode('ascii', errors='ignore')).join(f_text.splitlines()).replace("\\n", "\r\n").replace("\n", "\r\n").replace("\\t", "\t")))
    text_file.close()
    #print(url_rename[0])
    return(0)


# emit list of file paths
def extract_file_data(data_file):
    #read to end of file
    url_file_list = []
    for i in range(11,len(data_file)):
        #decode_line = html.unescape(data_file[i])
        decode_line = data_file[i].decode('iso8859_2')
        #decode_line=html2text.HTML2Text(decode_line)
        line_segments = decode_line.split("|")
        url = line_segments.pop().rstrip("\n")

        date = line_segments.pop()
        date = date.split("-")
        day = date.pop()
        month = date.pop()
        year = date.pop()
        form_type = line_segments.pop().replace("/",".")
        company_name = line_segments.pop()
        cik = line_segments.pop()
        file_name = year+month+day+"_"+form_type+"_"+"edgar_data_"+cik
        #gather only desired form types
        # can change to 'in' to only grab forms in list
        if(form_type in ["SC 13D","SC 13D.A"]):
        #if(form_type not in undesired_forms):
            url_file_list.append([url,file_name,year,form_type])
    return(url_file_list)


# emit list of files
def pull_index_files(start_year,end_year):
    idx_files = []
    for year in range(start_year,end_year):
        url = URL_INDEX + str(year) +"/"
        q_files = []
        for qtr in ["QTR1","QTR2","QTR3","QTR4"]:
            target_url = url + qtr + "/master.idx"
            #print(target_url)
            q_files.append(urllib.request.urlopen(target_url).readlines())
        idx_files.append(q_files)
    return(idx_files)


def main():
    #establish years desired
    start_year = int(input("Provide Start Year: "))
    end_year = int(input("Provide End Year (If only one year desired, provide that year.): "))
    for year in range(start_year, end_year+1):
            os.makedirs(file_loc+"/"+str(year), exist_ok=True)

    # gather desired IDX files
    idx_files = pull_index_files(start_year,end_year+1)
    #structured[[[url1.Q1.Y1,fn1],[url2.Q1.Y1,fn2],...][[url1.Q2.Y1,fn1],...],...[[url1.Q1.Y2,fn1]...]]

    # download files
    # by year
    for idx_year in idx_files:
        # by quarter
        for idx_quarter_file in idx_year :
            file_urls =extract_file_data(idx_quarter_file)
            i = 0
            for file_pair in file_urls:
                if i%1000 == 0:
                    print("Completed ",i," files.")
                    download_raw_text(file_pair)
                #download_raw_text(file_pair)
                i += 1


main()

##
