from bs4 import BeautifulSoup
import os
import sys
import io
from selenium import webdriver
import json
import re

def ref_scrap_to_json(publication):
    with open('./json/' + publication + '.json') as json_file:
        json_data = json.load(json_file)
        json_file.close()

    regex = re.compile(r'^\D+/(\d+)$')

    for entry in json_data:
        wd = webdriver.PhantomJS('/home/doyun/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
        url = 'http://ieeexplore.ieee.org/document/' + str(entry['ieee_id']) + '/?anchor=references'
        print(url)
        while True:
            try:
                wd.get(url)
            except RemoteDisconnected:
                print('RemoteDisconnected Happened')
                continue
            break
        html_page = wd.page_source
        soup = BeautifulSoup(html_page, 'html.parser')
        ref_str_list = soup.findAll("a", {"class": "stats-reference-link-viewArticle"})
        ref_list = [int(regex.search(ref_str.get('href')).group(1)) for ref_str in ref_str_list]
        entry['references'] = ref_list 
        wd.quit()

    with open('./json/' + publication + '_ref.json', 'w') as outfile:
        json.dump(json_data, outfile, sort_keys = True, indent = 4,)

if __name__ == '__main__':
    ref_scrap_to_json(sys.argv[1])  
