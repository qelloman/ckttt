import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import io
import bibtexparser
import re
import json
from paper import Paper

json_data = []

def bibtex_entry_to_table(bibtex_entry):
    myPaper = Paper(bibtex_entry)
    id = myPaper.getId()
    if not (myPaper.isPaper()):
        print('No author or keywords')
        return

    # Reference check
    wd = webdriver.PhantomJS('/home/doyun/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    url = 'http://ieeexplore.ieee.org/document/' + str(id) + '/?anchor=references'
    print(url)
    while True:
        try:
            wd.get(url)
        except http.client.RemoteDisconnected:
            print('RemoteDisconnected Happened')
            continue
        break
    html_page = wd.page_source
    soup = BeautifulSoup(html_page, 'html.parser')
    ref_dom_list = soup.findAll("a", {"class": "stats-reference-link-viewArticle"})
    regex = re.compile(r'^\D+/(\d+)$')
    refs = [int(regex.search(ref_dom.get('href')).group(1)) for ref_dom in ref_dom_list]
    for ref in refs:
        json_data.append({'id': int(id), 'ref_id': ref}) 
        print('id = {}, ref_id = {}'.format(id, ref))
    
    wd.quit()
   
    return
        

def ref_scrap_to_json(publication):
    with open('./bibtex/'+ publication + '.bibtex') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    for bibtex_entry in bib_database.entries:
        bibtex_entry_to_table(bibtex_entry)

    with open('./json/'+ publication + '_refonly.json', 'w') as json_file:
        json.dump(json_data, json_file, sort_keys=True, indent=4,)

if __name__ == '__main__':
    ref_scrap_to_json(sys.argv[1])  

